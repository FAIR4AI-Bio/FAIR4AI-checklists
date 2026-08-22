#!/usr/bin/env python
"""Merge a batch of item ratings into a FAIR4AI evaluation scaffold, in place.

Second of the two blessed helper scripts (with build_response_scaffold.py). The
agent rates the checklist one `Broad categories` section at a time and, after each
section, calls this script to write that section's judgments into the on-disk
scaffold. Benefits:

  - the file grows section-by-section (visible progress), and a failed turn loses
    only one section instead of the whole run (resumable);
  - the largest single Write is ~10 items, well under the payload/turn length that
    was tripping ECONNRESET/403 with the all-89-at-once approach;
  - only `status`/`evidence`/`notes`/`recommendation` are ever written here — the
    verbatim fields stay exactly as build_response_scaffold.py produced them.

The ratings file is JSON, either a list of objects or an object keyed by item:
    [ {"item": "...", "status": "meets", "evidence": "...", "notes": "",
       "recommendation": ""}, ... ]
    { "<item>": {"status": "partial", "evidence": "...", ...}, ... }
`item` + `status` are required per entry; `evidence`/`notes`/`recommendation`
default to "" when omitted. A PARTIAL batch is fine (unrated items stay pending).

Validation (fails loudly, writes nothing on error): every rated `item` must exist
in the scaffold (catches transcription drift / stale item names), and every status
must be one of meets | partial | does not meet | N/A (case/spacing-normalized to the
canonical spelling). Re-merging the same batch is idempotent.

Stdlib only. Usage:
    python scripts/merge_ratings.py --scaffold /abs/scaffold.json --ratings /abs/section.json
    python scripts/merge_ratings.py --scaffold /abs/scaffold.json --ratings -   # read stdin
    # --summary-json also sets summary.strengths/gaps/overall_assessment;
    # --session-json replaces the top-level `session` block:
    python scripts/merge_ratings.py --scaffold /abs/scaffold.json --ratings s.json --summary-json /abs/summary.json --session-json /abs/session.json
    python scripts/merge_ratings.py --selftest
"""
import argparse
import json
import sys

RATING_FIELDS = ["status", "evidence", "notes", "recommendation"]
VALID_STATUSES = ["meets", "partial", "does not meet", "N/A"]
# normalized form -> canonical spelling the tests/scorer expect.
_STATUS_CANON = {
    "meets": "meets",
    "partial": "partial",
    "doesnotmeet": "does not meet",
    "na": "N/A",
}


def _norm_status(s):
    return "".join(ch for ch in str(s).lower() if ch.isalnum())


def canonical_status(raw):
    """Return the canonical status spelling, or None if unrecognized."""
    return _STATUS_CANON.get(_norm_status(raw))


def normalize_ratings(ratings):
    """Accept a list or item-keyed dict; return a list of {item, <fields...>} dicts."""
    out = []
    if isinstance(ratings, dict):
        for item, body in ratings.items():
            entry = dict(body) if isinstance(body, dict) else {}
            entry["item"] = item
            out.append(entry)
    elif isinstance(ratings, list):
        for entry in ratings:
            if isinstance(entry, dict):
                out.append(dict(entry))
            else:
                raise ValueError("each rating in a list must be a JSON object")
    else:
        raise ValueError("ratings must be a JSON list or object")
    return out


def merge(doc, ratings):
    """Apply ratings to doc['responses'] in place. Returns (n_merged, n_rated_total).

    Raises ValueError (with ALL problems collected) before mutating anything.
    """
    responses = doc.get("responses")
    if not isinstance(responses, list):
        raise ValueError("scaffold has no 'responses' list")
    by_item = {}
    for resp in responses:
        if isinstance(resp, dict) and "item" in resp:
            by_item[resp["item"].strip()] = resp

    entries = normalize_ratings(ratings)
    errors = []
    prepared = []  # (target_response, updates) applied only after full validation
    for i, entry in enumerate(entries):
        item = (entry.get("item") or "").strip()
        if not item:
            errors.append(f"rating[{i}]: missing 'item'")
            continue
        target = by_item.get(item)
        if target is None:
            errors.append(f"rating[{i}]: item {item!r} is not in the scaffold "
                          f"(check spelling / stale checklist)")
            continue
        if "status" not in entry:
            errors.append(f"rating[{i}] ({item!r}): missing 'status'")
            continue
        canon = canonical_status(entry["status"])
        if canon is None:
            errors.append(f"rating[{i}] ({item!r}): invalid status {entry['status']!r} "
                          f"(must be one of {VALID_STATUSES})")
            continue
        updates = {"status": canon}
        for field in RATING_FIELDS:
            if field == "status":
                continue
            if field in entry and entry[field] is not None:
                updates[field] = str(entry[field])
        prepared.append((target, updates))

    if errors:
        raise ValueError("cannot merge ratings:\n  - " + "\n  - ".join(errors))

    for target, updates in prepared:
        target.update(updates)

    n_rated_total = sum(1 for r in responses if isinstance(r, dict) and r.get("status"))
    return len(prepared), n_rated_total


def apply_summary(doc, summary):
    """Set summary.strengths/gaps/overall_assessment from a dict (leaves scores alone)."""
    dst = doc.setdefault("summary", {})
    for key in ("strengths", "gaps", "overall_assessment"):
        if key in summary:
            dst[key] = summary[key]


def apply_session(doc, session):
    """Replace the top-level `session` block (dataset identity, evaluator, method, etc.).

    Provided as a scripted alternative to hand-editing JSON: the session block depends on the
    metadata fetched at eval time, so it is set after the scaffold is built.
    """
    doc["session"] = session


def _read_json_arg(value):
    if value == "-":
        return json.load(sys.stdin)
    with open(value, encoding="utf-8") as f:
        return json.load(f)


def _selftest():
    scaffold = {
        "session": {},
        "responses": [
            {"item": "A", "requirement_definition": "ra", "status": "", "evidence": "",
             "notes": "", "recommendation": "", "fair_category": "Findable", "ai_fair_criteria": "Structural"},
            {"item": "B", "requirement_definition": "rb", "status": "", "evidence": "",
             "notes": "", "recommendation": "", "fair_category": "Reusable", "ai_fair_criteria": "Provenance"},
        ],
        "summary": {"strengths": [], "gaps": [], "overall_assessment": "", "fair4ai_scores": {}},
    }
    import copy

    # list form, partial batch, status normalization
    d = copy.deepcopy(scaffold)
    n, total = merge(d, [{"item": "A", "status": "Does Not Meet", "evidence": "none", "recommendation": "add it"}])
    assert n == 1 and total == 1, (n, total)
    a = d["responses"][0]
    assert a["status"] == "does not meet", a["status"]
    assert a["evidence"] == "none" and a["recommendation"] == "add it"
    assert d["responses"][1]["status"] == "", "unrated item must stay pending"
    # the 8 fields are unchanged in set (no new keys, verbatim fields intact)
    assert set(a.keys()) == set(scaffold["responses"][0].keys())
    assert a["fair_category"] == "Findable" and a["requirement_definition"] == "ra"

    # dict (item-keyed) form + N/A normalization
    d = copy.deepcopy(scaffold)
    n, total = merge(d, {"A": {"status": "meets", "evidence": "x"}, "B": {"status": "n/a"}})
    assert n == 2 and total == 2
    assert d["responses"][0]["status"] == "meets"
    assert d["responses"][1]["status"] == "N/A", d["responses"][1]["status"]

    # idempotent
    d1 = copy.deepcopy(scaffold)
    merge(d1, [{"item": "A", "status": "meets", "evidence": "x"}])
    d2 = copy.deepcopy(d1)
    merge(d2, [{"item": "A", "status": "meets", "evidence": "x"}])
    assert d1 == d2, "re-merging the same batch must be idempotent"

    # unknown item -> error, nothing mutated
    d = copy.deepcopy(scaffold)
    try:
        merge(d, [{"item": "ZZZ", "status": "meets"}])
        assert False, "unknown item must raise"
    except ValueError as e:
        assert "not in the scaffold" in str(e)
    assert d == scaffold, "no mutation on validation failure"

    # invalid status -> error, nothing mutated (even for the valid sibling in the batch)
    d = copy.deepcopy(scaffold)
    try:
        merge(d, [{"item": "A", "status": "meets"}, {"item": "B", "status": "sorta"}])
        assert False, "invalid status must raise"
    except ValueError as e:
        assert "invalid status" in str(e)
    assert d == scaffold, "no partial mutation when any entry in the batch is invalid"

    # missing status -> error
    d = copy.deepcopy(scaffold)
    try:
        merge(d, [{"item": "A", "evidence": "x"}])
        assert False, "missing status must raise"
    except ValueError as e:
        assert "missing 'status'" in str(e)

    # summary passthrough
    d = copy.deepcopy(scaffold)
    apply_summary(d, {"strengths": ["s1"], "gaps": ["g1"], "overall_assessment": "ok",
                      "fair4ai_scores": "IGNORED"})
    assert d["summary"]["strengths"] == ["s1"] and d["summary"]["overall_assessment"] == "ok"
    assert d["summary"]["fair4ai_scores"] == {}, "apply_summary must not touch scores"

    # session passthrough
    d = copy.deepcopy(scaffold)
    apply_session(d, {"evaluation_date": "2026-01-01", "dataset": {"title": "T"}})
    assert d["session"]["dataset"]["title"] == "T" and d["session"]["evaluation_date"] == "2026-01-01"

    print("merge_ratings selftest: PASS")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Merge item ratings into a FAIR4AI scaffold JSON.")
    ap.add_argument("--scaffold", help="absolute path to the scaffold/eval JSON to update in place")
    ap.add_argument("--ratings", help="path to the ratings JSON, or '-' for stdin")
    ap.add_argument("--summary-json", help="optional JSON file setting summary.strengths/gaps/overall_assessment")
    ap.add_argument("--session-json", help="optional JSON file that replaces the top-level `session` block")
    ap.add_argument("--selftest", action="store_true", help="run internal checks and exit")
    args = ap.parse_args(argv)

    if args.selftest:
        _selftest()
        return 0
    if not args.scaffold:
        ap.error("--scaffold is required unless --selftest is given")
    if not (args.ratings or args.summary_json or args.session_json):
        ap.error("provide --ratings (and/or --summary-json / --session-json)")

    try:
        with open(args.scaffold, encoding="utf-8") as f:
            doc = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: scaffold not found: {args.scaffold}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in scaffold {args.scaffold}: {e}", file=sys.stderr)
        return 1

    n_merged = 0
    total = sum(1 for r in doc.get("responses", []) if isinstance(r, dict) and r.get("status"))
    if args.ratings:
        try:
            ratings = _read_json_arg(args.ratings)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR: could not read --ratings: {e}", file=sys.stderr)
            return 1
        try:
            n_merged, total = merge(doc, ratings)
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1

    if args.summary_json:
        try:
            with open(args.summary_json, encoding="utf-8") as f:
                apply_summary(doc, json.load(f))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR: could not read --summary-json: {e}", file=sys.stderr)
            return 1

    if args.session_json:
        try:
            with open(args.session_json, encoding="utf-8") as f:
                apply_session(doc, json.load(f))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR: could not read --session-json: {e}", file=sys.stderr)
            return 1

    with open(args.scaffold, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")

    n_total_responses = len(doc.get("responses", []))
    print(f"merged {n_merged} rating(s); {total}/{n_total_responses} items now rated -> {args.scaffold}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
