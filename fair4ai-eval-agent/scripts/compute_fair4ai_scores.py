#!/usr/bin/env python
"""Compute reproducible FAIR4AI scores from a FAIR4AI evaluation JSON.

The FAIR4AI-Bio checklist rates each item `meets | partial | does not meet | N/A`
(see RATING_RUBRIC.md). This script turns those ratings into quantitative,
traceable, reproducible scores in the range 0-1, where 1 is "most FAIR4AI".

It produces TWO complementary assessments:

  1. Traditional FAIR -- Findable / Accessible / Interoperable / Reusable, keyed
     off each response's `fair_category` (the checklist `FAIR category` column).
  2. AI-FAIR -- four categories keyed off each response's `ai_fair_criteria` (the
     checklist `AI FAIR Criteria: Structural | Scientific | Provenance | Governance`
     column; older evaluations use the field name `criteria`) and, for backward
     compatibility, the Governance section:
        - ml_ready          = the structural facet score
        - ai_ready_for_task = mean(structural, scientific) facet scores
        - traceable         = mean(provenance, structural) facet scores
        - care_compliance   = the governance score (items whose criteria value
                              includes "Governance", OR -- for older evaluations
                              produced before Governance became a Criteria facet
                              -- whose section/Broad category is "Governance")

Scoring rules (see RATING_RUBRIC.md and the fair4ai-scoring skill):
  - Per-item score:  meets -> 1.0 | partial -> 0.5 | does not meet -> 0.0
                     N/A -> excluded (does not count).
  - Traditional FAIR: per-dimension score = mean of contributing item scores; an
    item mapped to several dimensions counts in each. Overall FAIR = equal-weight
    mean of the (up to four) non-null dimension scores.
  - AI-FAIR: first compute four facet base scores (structural, scientific,
    provenance, governance) as means of contributing item scores. Then the four
    AI-FAIR categories are equal-weight means of their (non-null) facet
    components, and overall AI-FAIR is the equal-weight mean of the (non-null)
    four categories.
  - Any dimension/facet with zero scored items (all N/A) is reported as null and
    OMITTED from every mean that would include it, so equal weighting is not
    skewed.

Determinism: given the same input JSON, the output numbers are identical
(re-running is idempotent). No third-party dependencies (stdlib only).

Usage:
    python scripts/compute_fair4ai_scores.py <eval.json>          # write scores back
    python scripts/compute_fair4ai_scores.py <eval.json> --dry-run # print only
    python scripts/compute_fair4ai_scores.py --selftest            # run internal checks
"""
import argparse
import json
import sys

# Traditional-FAIR dimensions, in fixed display order.
FAIR_DIMS = ["findable", "accessible", "interoperable", "reusable"]

# Normalized FAIR-category token -> canonical dimension key.
# Tokens are matched case-insensitively after stripping non-alphanumerics.
# Any token that is not one of the four FAIR dimensions is reported as unknown.
# (The deprecated "AI-ready" token was removed from the checklist; AI-readiness is
# now measured only by the AI-FAIR assessment via the criteria facets, so a stray
# "AI-ready" now surfaces loudly as an unknown token rather than being swallowed.)
_FAIR_ALIASES = {
    "findable": "findable",
    "accessible": "accessible",
    "interoperable": "interoperable",
    "reusable": "reusable",
}

# AI-FAIR facet base scores derived from the `criteria` column, in fixed order.
# These three feed ml_ready / ai_ready_for_task / traceable. Governance is a fourth
# recognized `criteria` token but is NOT listed here: it feeds only care_compliance
# (via _criteria_has_governance / the Governance section), so the three-facet math is
# unchanged. A Governance-tagged item keeps whatever structural/scientific/provenance
# tokens it also carries and still feeds those facets too.
CRITERIA_FACETS = ["structural", "scientific", "provenance"]

# status string (normalized) -> numeric score, or None if excluded.
# The four canonical statuses match RATING_RUBRIC.md and the agent exactly:
# meets | partial | does not meet | N/A.
_STATUS_SCORE = {
    "meets": 1.0,
    "partial": 0.5,
    "doesnotmeet": 0.0,
    "na": None,
    "n/a": None,
}


def _norm(s):
    """Lowercase and keep only alphanumerics, for robust token matching."""
    return "".join(ch for ch in str(s).lower() if ch.isalnum())


def _norm_status(s):
    return "".join(ch for ch in str(s).lower() if ch.isalnum() or ch == "/")


def parse_fair_categories(raw):
    """Parse a pipe-separated FAIR category string into canonical FAIR dims.

    Returns (keys, unknown_tokens). Blank/None -> ([], []). Any token that is not
    one of the four FAIR dimensions is returned as unknown.
    """
    if not raw or not str(raw).strip():
        return [], []
    keys, unknown = [], []
    for token in str(raw).split("|"):
        token = token.strip()
        if not token:
            continue
        n = _norm(token)
        if n in _FAIR_ALIASES:
            key = _FAIR_ALIASES[n]
            if key and key not in keys:
                keys.append(key)
        else:
            unknown.append(token)
    return keys, unknown


def parse_criteria(raw):
    """Parse a Criteria string into canonical facet keys via substring matching.

    Robust to the checklist's variants (casing, trailing `?`, parentheticals, and
    ` | `, `/`, `+`, or comma separators, e.g. "Structural | Scientific" (the current
    checklist convention), "Structural/Scientific", "scientific + structural",
    "Provenance, could be scientific", "structural (only needed for NLP)"). Facet
    words are matched as substrings, so any of these separators resolves correctly.
    Returns (facets, unknown_tokens); a non-blank value that matches no facet is
    reported as unknown.

    "Governance" is a recognized token (it routes to care_compliance via
    _criteria_has_governance, not to the three scoring facets), so a value that
    contains only "Governance" is NOT reported as unknown.
    """
    if not raw or not str(raw).strip():
        return [], []
    text = str(raw).lower()
    facets = [f for f in CRITERIA_FACETS if f in text]
    unknown = []
    if not facets and "governance" not in text and any(ch.isalnum() for ch in text):
        unknown.append(str(raw).strip())
    return facets, unknown


def _criteria_has_governance(criteria):
    """True when a response's `criteria` value includes the Governance token."""
    return "governance" in _norm(criteria)


def _is_governance(section):
    """True when a response's section (checklist Broad category) is Governance.

    Retained as a backward-compatible fallback for evaluations produced before
    Governance became a `criteria` facet; new evaluations detect it from `criteria`.
    """
    return "governance" in _norm(section)


def _new_bucket():
    return {"sum": 0.0, "n_scored": 0, "meets": 0, "partial": 0,
            "does_not_meet": 0, "na": 0}


def _add(bucket, value):
    """Fold one per-item score into an accumulator bucket (value None => N/A)."""
    if value is None:
        bucket["na"] += 1
        return
    bucket["sum"] += value
    bucket["n_scored"] += 1
    if value == 1.0:
        bucket["meets"] += 1
    elif value == 0.5:
        bucket["partial"] += 1
    else:
        bucket["does_not_meet"] += 1


def _score(bucket):
    """Mean of scored items in a bucket, or None if nothing scored."""
    n = bucket["n_scored"]
    return (bucket["sum"] / n) if n else None


def _mean_non_null(values):
    """Equal-weight mean of the non-null values, or None if all are null."""
    vals = [v for v in values if v is not None]
    return (sum(vals) / len(vals)) if vals else None


def _r3(x):
    return round(x, 3) if x is not None else None


def _counts(bucket):
    return {
        "n_scored": bucket["n_scored"],
        "meets": bucket["meets"],
        "partial": bucket["partial"],
        "does_not_meet": bucket["does_not_meet"],
        "na": bucket["na"],
    }


def score_document(doc):
    """Compute the two-assessment FAIR4AI scores from a loaded evaluation document.

    Returns (scores, warnings) where scores is suitable for
    `summary.fair4ai_scores`:
      {
        "traditional_fair": { <dim>: float|None, ..., "overall": float|None,
                              "details": { <dim>: {counts} } },
        "ai_fair": { "ml_ready": .., "ai_ready_for_task": .., "traceable": ..,
                     "care_compliance": .., "overall": ..,
                     "components": { <facet>: {"score":.., counts}, "governance": {..} } }
      }
    """
    fair = {d: _new_bucket() for d in FAIR_DIMS}
    facet = {f: _new_bucket() for f in CRITERIA_FACETS}
    gov = _new_bucket()
    warnings = []
    unmapped_scoreable = 0

    responses = doc.get("responses", []) if isinstance(doc, dict) else []
    if not isinstance(responses, list):
        warnings.append("'responses' is not a list; no items scored")
        responses = []

    for i, resp in enumerate(responses):
        if not isinstance(resp, dict):
            warnings.append(f"response[{i}]: not a JSON object (skipped)")
            continue
        status_key = _norm_status(resp.get("status", ""))
        value = _STATUS_SCORE.get(status_key, "unknown")
        if value == "unknown":
            warnings.append(f"response[{i}]: unrecognized status {resp.get('status')!r} (excluded)")
            continue

        fair_keys, fair_unknown = parse_fair_categories(resp.get("fair_category", ""))
        for tok in fair_unknown:
            warnings.append(f"response[{i}]: unknown FAIR category token {tok!r} (ignored)")
        # `ai_fair_criteria` is the current field name; `criteria` is accepted as a
        # backward-compatible fallback for evaluations produced before the rename.
        crit_raw = resp.get("ai_fair_criteria") or resp.get("criteria", "")
        facets, crit_unknown = parse_criteria(crit_raw)
        for tok in crit_unknown:
            warnings.append(f"response[{i}]: unrecognized criteria value {tok!r} (ignored)")
        # Governance is primarily an `ai_fair_criteria` facet now; fall back to the
        # Governance section so evaluations produced before that change still score
        # care_compliance. The union adds each qualifying item to the gov bucket once.
        is_gov = _criteria_has_governance(crit_raw) or _is_governance(resp.get("section", ""))

        if not (fair_keys or facets or is_gov):
            # An item that maps to no FAIR dimension, no criteria facet, and is not
            # Governance contributes to nothing. N/A items like this are expected;
            # a *scoreable* one is a data problem worth flagging.
            if value is not None:
                unmapped_scoreable += 1
            continue

        for d in fair_keys:
            _add(fair[d], value)
        for f in facets:
            _add(facet[f], value)
        if is_gov:
            _add(gov, value)

    if unmapped_scoreable:
        warnings.append(f"{unmapped_scoreable} scoreable response(s) mapped to no FAIR dimension, "
                        f"no criteria facet, and no Governance section, and were excluded from "
                        f"all assessments")

    # --- Traditional FAIR ---
    fair_scores = {d: _score(fair[d]) for d in FAIR_DIMS}
    fair_overall = _mean_non_null([fair_scores[d] for d in FAIR_DIMS])
    traditional_fair = {d: _r3(fair_scores[d]) for d in FAIR_DIMS}
    traditional_fair["overall"] = _r3(fair_overall)
    traditional_fair["details"] = {d: _counts(fair[d]) for d in FAIR_DIMS}

    # --- AI-FAIR ---
    s = _score(facet["structural"])
    sci = _score(facet["scientific"])
    prov = _score(facet["provenance"])
    g = _score(gov)

    ml_ready = _mean_non_null([s])
    ai_ready_for_task = _mean_non_null([s, sci])
    traceable = _mean_non_null([prov, s])
    care_compliance = _mean_non_null([g])
    ai_overall = _mean_non_null([ml_ready, ai_ready_for_task, traceable, care_compliance])

    ai_fair = {
        "ml_ready": _r3(ml_ready),
        "ai_ready_for_task": _r3(ai_ready_for_task),
        "traceable": _r3(traceable),
        "care_compliance": _r3(care_compliance),
        "overall": _r3(ai_overall),
        "components": {
            "structural": {"score": _r3(s), **_counts(facet["structural"])},
            "scientific": {"score": _r3(sci), **_counts(facet["scientific"])},
            "provenance": {"score": _r3(prov), **_counts(facet["provenance"])},
            "governance": {"score": _r3(g), **_counts(gov)},
        },
    }

    return {"traditional_fair": traditional_fair, "ai_fair": ai_fair}, warnings


def _fmt(x):
    return "  n/a" if x is None else f"{x:.3f}"


def format_report(scores):
    lines = []
    tf = scores["traditional_fair"]
    lines.append("Traditional FAIR:")
    for d in FAIR_DIMS:
        det = tf["details"][d]
        lines.append(
            f"  {d:<16} {_fmt(tf[d])}   "
            f"(scored {det['n_scored']}: {det['meets']} meets / "
            f"{det['partial']} partial / {det['does_not_meet']} does-not-meet; "
            f"{det['na']} N/A)"
        )
    lines.append(f"  {'OVERALL FAIR':<16} {_fmt(tf['overall'])}   "
                 f"(equal-weight mean of scored dimensions)")

    af = scores["ai_fair"]
    comp = af["components"]
    lines.append("AI-FAIR:")
    lines.append(f"  {'ml_ready':<18} {_fmt(af['ml_ready'])}   (structural)")
    lines.append(f"  {'ai_ready_for_task':<18} {_fmt(af['ai_ready_for_task'])}   (structural + scientific)")
    lines.append(f"  {'traceable':<18} {_fmt(af['traceable'])}   (provenance + structural)")
    lines.append(f"  {'care_compliance':<18} {_fmt(af['care_compliance'])}   (governance)")
    lines.append(f"  {'OVERALL AI-FAIR':<18} {_fmt(af['overall'])}   (equal-weight mean of the four)")
    lines.append("  facet base scores:")
    for f in CRITERIA_FACETS + ["governance"]:
        c = comp[f]
        lines.append(
            f"    {f:<14} {_fmt(c['score'])}   "
            f"(scored {c['n_scored']}: {c['meets']} meets / {c['partial']} partial / "
            f"{c['does_not_meet']} does-not-meet; {c['na']} N/A)"
        )
    return "\n".join(lines)


def selftest():
    """Internal correctness checks for the scoring math. Exits non-zero on failure."""
    # Helper omits None from a mean.
    assert _mean_non_null([0.8, None]) == 0.8, "mean must omit None components"
    assert _mean_non_null([None, None]) is None, "all-None mean must be None"

    doc = {
        "responses": [
            {"status": "meets", "fair_category": "Findable", "criteria": "Structural", "section": "General Information"},
            {"status": "partial", "fair_category": "Findable", "criteria": "Structural", "section": "General Information"},
            {"status": "does not meet", "fair_category": "Findable | Reusable", "criteria": "Scientific", "section": "Guidance"},
            {"status": "meets", "fair_category": "Accessible | Reusable", "criteria": "Provenance/Structural", "section": "Data Access"},
            {"status": "partial", "fair_category": "Reusable", "criteria": "Provenance", "section": "Provenance"},
            {"status": "N/A", "fair_category": "Interoperable", "criteria": "Structural", "section": "Data structure"},
            {"status": "meets", "fair_category": "NotADimension", "criteria": "Scientific", "section": "Guidance"},  # unknown FAIR token: warned + contributes nothing to FAIR
            {"status": "meets", "fair_category": "Reusable", "criteria": "Provenance", "section": "Governance"},
            {"status": "partial", "fair_category": "Reusable", "criteria": "Provenance", "section": "Governance"},
            {"status": "meets", "fair_category": "", "criteria": "", "section": "General Information"},  # unmapped scoreable
        ]
    }
    scores, warnings = score_document(doc)
    # A non-dimension FAIR token (e.g. the removed "AI-ready") is reported, not swallowed.
    assert any("unknown FAIR category token" in w and "NotADimension" in w for w in warnings), warnings
    tf = scores["traditional_fair"]
    assert tf["findable"] == round((1 + 0.5 + 0) / 3, 3) == 0.5, tf["findable"]
    assert tf["accessible"] == 1.0, tf["accessible"]
    assert tf["interoperable"] is None, tf["interoperable"]                 # all N/A
    assert tf["reusable"] == round((0 + 1 + 0.5 + 1 + 0.5) / 5, 3) == 0.6, tf["reusable"]
    assert tf["overall"] == round((0.5 + 1.0 + 0.6) / 3, 3) == 0.7, tf["overall"]
    assert tf["details"]["findable"] == {"n_scored": 3, "meets": 1, "partial": 1,
                                         "does_not_meet": 1, "na": 0}
    assert tf["details"]["interoperable"]["na"] == 1

    af = scores["ai_fair"]
    comp = af["components"]
    assert comp["structural"]["score"] == round(2.5 / 3, 3) == 0.833, comp["structural"]
    assert comp["scientific"]["score"] == 0.5, comp["scientific"]           # (0 + 1)/2
    assert comp["provenance"]["score"] == 0.75, comp["provenance"]          # (1+0.5+1+0.5)/4
    assert comp["governance"]["score"] == 0.75, comp["governance"]          # (1+0.5)/2
    assert comp["structural"]["na"] == 1                                    # response[5] N/A
    assert af["ml_ready"] == 0.833, af["ml_ready"]
    assert af["ai_ready_for_task"] == round((2.5 / 3 + 0.5) / 2, 3) == 0.667, af["ai_ready_for_task"]
    assert af["traceable"] == round((0.75 + 2.5 / 3) / 2, 3) == 0.792, af["traceable"]
    assert af["care_compliance"] == 0.75, af["care_compliance"]
    exp_ai = round((2.5 / 3 + (2.5 / 3 + 0.5) / 2 + (0.75 + 2.5 / 3) / 2 + 0.75) / 4, 3)
    assert af["overall"] == exp_ai == 0.76, (af["overall"], exp_ai)

    # a null facet is omitted: with scientific removed, ai_ready_for_task == ml_ready
    doc2 = {"responses": [
        {"status": "meets", "fair_category": "", "criteria": "Structural", "section": "x"},
    ]}
    s2, _ = score_document(doc2)
    assert s2["ai_fair"]["ml_ready"] == 1.0
    assert s2["ai_fair"]["ai_ready_for_task"] == 1.0, "scientific null must drop out of the mean"
    assert s2["ai_fair"]["care_compliance"] is None                          # no governance items

    # governance detected from the `criteria` facet (new schema), not just the section;
    # a Governance-tagged item still feeds its other facets (here: provenance).
    doc3 = {"responses": [
        {"status": "meets", "fair_category": "", "criteria": "Provenance/Governance", "section": "Provenance"},
        {"status": "does not meet", "fair_category": "", "criteria": "Governance", "section": "Data Access"},
    ]}
    s3, w3 = score_document(doc3)
    assert s3["ai_fair"]["care_compliance"] == 0.5, s3["ai_fair"]["care_compliance"]        # (1 + 0)/2
    assert s3["ai_fair"]["components"]["governance"]["n_scored"] == 2, s3["ai_fair"]["components"]["governance"]
    assert s3["ai_fair"]["components"]["provenance"]["n_scored"] == 1, "Provenance/Governance must still feed provenance"
    assert not any("unrecognized criteria" in w for w in w3), w3   # 'Governance' must not warn as unknown
    assert not any("excluded from all assessments" in w for w in w3), w3  # governance-only item is mapped

    # new schema: the field is `ai_fair_criteria` with a ` | ` separator and NO `section`.
    # Governance must be detected from the criteria value alone (no section fallback),
    # and a ` | `-joined value must feed every facet it lists.
    doc4 = {"responses": [
        {"status": "meets", "fair_category": "Reusable",
         "ai_fair_criteria": "Provenance | Governance"},
        {"status": "partial", "fair_category": "Accessible | Reusable",
         "ai_fair_criteria": "Scientific | Provenance | Governance"},
    ]}
    s4, w4 = score_document(doc4)
    assert s4["ai_fair"]["care_compliance"] == 0.75, s4["ai_fair"]["care_compliance"]   # (1 + 0.5)/2
    assert s4["ai_fair"]["components"]["provenance"]["n_scored"] == 2, s4["ai_fair"]["components"]["provenance"]
    assert s4["ai_fair"]["components"]["scientific"]["n_scored"] == 1, "` | ` value must feed scientific"
    assert not any("unrecognized criteria" in w for w in w4), w4
    assert not any("excluded from all assessments" in w for w in w4), w4

    # idempotency
    scores_again, _ = score_document(doc)
    assert scores == scores_again, "non-deterministic output"

    # the fully-unmapped scoreable item must be flagged
    assert any("excluded from all assessments" in w for w in warnings), warnings

    print("selftest: PASS")
    print(format_report(scores))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compute reproducible FAIR4AI scores (0-1).")
    ap.add_argument("eval_json", nargs="?", help="path to a FAIR4AI evaluation JSON")
    ap.add_argument("--dry-run", action="store_true",
                    help="print scores without writing them back into the file")
    ap.add_argument("--selftest", action="store_true", help="run internal correctness checks")
    args = ap.parse_args(argv)

    if args.selftest:
        selftest()
        return 0
    if not args.eval_json:
        ap.error("eval_json is required unless --selftest is given")

    try:
        with open(args.eval_json, encoding="utf-8") as f:
            doc = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.eval_json}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in {args.eval_json}: {e}", file=sys.stderr)
        return 1
    if not isinstance(doc, dict):
        print(f"ERROR: {args.eval_json} does not contain a JSON object", file=sys.stderr)
        return 1

    scores, warnings = score_document(doc)

    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)

    print(f"FAIR4AI scores for {args.eval_json}:")
    print(format_report(scores))

    if args.dry_run:
        print("\n(dry run: file not modified)")
        return 0

    doc.setdefault("summary", {})["fair4ai_scores"] = scores
    with open(args.eval_json, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"\nWrote summary.fair4ai_scores into {args.eval_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
