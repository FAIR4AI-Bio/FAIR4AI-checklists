#!/usr/bin/env python
"""Compute reproducible FAIR4AI scores from a FAIR4AI evaluation JSON.

The FAIR4AI-Bio checklist rates each item `meets | partial | does not meet | N/A`
(see RATING_RUBRIC.md). This script turns those ratings into quantitative,
traceable, reproducible per-dimension and overall scores in the range 0-1, where
1 is "most FAIR4AI".

Scoring rules (see RATING_RUBRIC.md and the fair4ai-scoring skill):
  - Per-item score:  meets -> 1.0 | partial -> 0.5 | does not meet -> 0.0
                     N/A (or blank FAIR4AI category) -> excluded, does not count.
  - Each response carries a `fair4ai_category` field copied verbatim from the
    checklist's `FAIR4AI category` column: one or more of the five FAIR4AI
    dimensions (Findable | Accessible | Interoperable | Reusable | AI-ready),
    pipe-separated. An item mapped to k dimensions contributes its score to EACH
    of those k dimensions' means ("allow multiple" semantics).
  - Per-dimension score = mean of contributing item scores in that dimension (0-1).
    A dimension with zero scored items (all N/A) is reported as null and OMITTED
    from the overall mean so equal weighting is not skewed.
  - Overall score = equal-weight mean of the (up to five) per-dimension scores (0-1).

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

# Canonical dimension keys, in fixed display order.
DIMENSIONS = ["findable", "accessible", "interoperable", "reusable", "ai_ready"]

# Normalized category token -> canonical key. Tokens are matched case-insensitively
# after stripping and collapsing separators (space/hyphen/underscore -> "").
_CATEGORY_ALIASES = {
    "findable": "findable",
    "accessible": "accessible",
    "interoperable": "interoperable",
    "reusable": "reusable",
    "airead": None,          # guard against typos; not used
    "aiready": "ai_ready",
}

# status string (normalized) -> numeric score, or None if excluded.
_STATUS_SCORE = {
    "meets": 1.0,
    "partial": 0.5,
    "partiallymeets": 0.5,
    "doesnotmeet": 0.0,
    "na": None,
    "n/a": None,
}


def _norm(s):
    """Lowercase and strip spaces/hyphens/underscores/slashes for robust matching."""
    return "".join(ch for ch in str(s).lower() if ch.isalnum())


def _norm_status(s):
    return "".join(ch for ch in str(s).lower() if ch.isalnum() or ch == "/")


def parse_categories(raw):
    """Parse a pipe-separated FAIR4AI category string into canonical dimension keys.

    Returns (keys, unknown_tokens). Blank/None -> ([], []).
    """
    if not raw or not str(raw).strip():
        return [], []
    keys, unknown = [], []
    for token in str(raw).split("|"):
        token = token.strip()
        if not token:
            continue
        key = _CATEGORY_ALIASES.get(_norm(token))
        if key in DIMENSIONS:
            if key not in keys:
                keys.append(key)
        else:
            unknown.append(token)
    return keys, unknown


def score_document(doc):
    """Compute FAIR4AI scores from a loaded evaluation document.

    Returns a dict suitable for `summary.fair4ai_scores`:
      { <dim>: float|None, ..., "overall": float|None,
        "details": { <dim>: {n_scored, meets, partial, does_not_meet, na} } }
    Also returns a list of warnings (unknown categories, unmapped scoreable items).
    """
    # per-dimension accumulators
    tally = {d: {"sum": 0.0, "n_scored": 0, "meets": 0, "partial": 0,
                 "does_not_meet": 0, "na": 0} for d in DIMENSIONS}
    warnings = []
    unmapped_scoreable = 0

    for i, resp in enumerate(doc.get("responses", [])):
        status_key = _norm_status(resp.get("status", ""))
        value = _STATUS_SCORE.get(status_key, "unknown")
        if value == "unknown":
            warnings.append(f"response[{i}]: unrecognized status {resp.get('status')!r} (excluded)")
            continue

        keys, unknown = parse_categories(resp.get("fair4ai_category", ""))
        for tok in unknown:
            warnings.append(f"response[{i}]: unknown FAIR4AI category token {tok!r} (ignored)")

        if not keys:
            # N/A items with no category are expected; scoreable items without a
            # category are a data problem worth flagging.
            if value is not None:
                unmapped_scoreable += 1
            continue

        for d in keys:
            if value is None:  # N/A
                tally[d]["na"] += 1
                continue
            tally[d]["sum"] += value
            tally[d]["n_scored"] += 1
            if value == 1.0:
                tally[d]["meets"] += 1
            elif value == 0.5:
                tally[d]["partial"] += 1
            else:
                tally[d]["does_not_meet"] += 1

    if unmapped_scoreable:
        warnings.append(f"{unmapped_scoreable} scoreable response(s) had a blank FAIR4AI "
                        f"category and were excluded from all dimensions")

    # per-dimension mean (raw), then overall = equal-weight mean of scored dimensions
    raw_scores = {}
    for d in DIMENSIONS:
        n = tally[d]["n_scored"]
        raw_scores[d] = (tally[d]["sum"] / n) if n else None

    scored_dims = [raw_scores[d] for d in DIMENSIONS if raw_scores[d] is not None]
    overall_raw = (sum(scored_dims) / len(scored_dims)) if scored_dims else None

    result = {}
    for d in DIMENSIONS:
        result[d] = round(raw_scores[d], 3) if raw_scores[d] is not None else None
    result["overall"] = round(overall_raw, 3) if overall_raw is not None else None
    result["details"] = {
        d: {
            "n_scored": tally[d]["n_scored"],
            "meets": tally[d]["meets"],
            "partial": tally[d]["partial"],
            "does_not_meet": tally[d]["does_not_meet"],
            "na": tally[d]["na"],
        }
        for d in DIMENSIONS
    }
    return result, warnings


def format_report(scores):
    lines = []
    for d in DIMENSIONS:
        s = scores[d]
        det = scores["details"][d]
        val = "  n/a" if s is None else f"{s:.3f}"
        lines.append(
            f"  {d:<14} {val}   "
            f"(scored {det['n_scored']}: {det['meets']} meets / "
            f"{det['partial']} partial / {det['does_not_meet']} does-not-meet; "
            f"{det['na']} N/A)"
        )
    ov = scores["overall"]
    lines.append(f"  {'OVERALL':<14} {'  n/a' if ov is None else f'{ov:.3f}'}   "
                 f"(equal-weight mean of scored dimensions)")
    return "\n".join(lines)


def selftest():
    """Internal correctness checks for the scoring math. Exits non-zero on failure."""
    doc = {
        "responses": [
            {"status": "meets", "fair4ai_category": "Findable"},                 # F=1
            {"status": "partial", "fair4ai_category": "Findable"},               # F=0.5
            {"status": "does not meet", "fair4ai_category": "Findable"},         # F=0
            {"status": "meets", "fair4ai_category": "Accessible | Reusable"},    # A=1, R=1 (multi)
            {"status": "partial", "fair4ai_category": "Reusable"},               # R=0.5
            {"status": "N/A", "fair4ai_category": "Interoperable"},              # I: all N/A -> null
            {"status": "meets", "fair4ai_category": ""},                         # scoreable, unmapped
            {"status": "N/A", "fair4ai_category": ""},                           # N/A, unmapped (ok)
            {"status": "meets", "fair4ai_category": "AI-ready"},                 # AI=1
        ]
    }
    scores, warnings = score_document(doc)
    expected = {
        "findable": round((1 + 0.5 + 0) / 3, 3),      # 0.5
        "accessible": 1.0,
        "interoperable": None,                          # all N/A
        "reusable": round((1 + 0.5) / 2, 3),           # 0.75
        "ai_ready": 1.0,
    }
    for d, exp in expected.items():
        assert scores[d] == exp, f"{d}: expected {exp}, got {scores[d]}"
    # overall = mean of scored dims {0.5, 1.0, 0.75, 1.0} (interoperable omitted)
    exp_overall = round((0.5 + 1.0 + 0.75 + 1.0) / 4, 3)
    assert scores["overall"] == exp_overall, f"overall: expected {exp_overall}, got {scores['overall']}"
    # details sanity
    assert scores["details"]["findable"] == {"n_scored": 3, "meets": 1, "partial": 1,
                                             "does_not_meet": 1, "na": 0}
    assert scores["details"]["interoperable"]["na"] == 1
    assert scores["details"]["reusable"]["n_scored"] == 2
    # idempotency: re-scoring the same doc yields identical output
    scores2, _ = score_document(doc)
    assert scores == scores2, "non-deterministic output"
    # the blank-category meets item must be flagged
    assert any("blank FAIR4AI category" in w for w in warnings), warnings
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

    with open(args.eval_json, encoding="utf-8") as f:
        doc = json.load(f)

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
