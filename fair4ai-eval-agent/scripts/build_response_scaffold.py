#!/usr/bin/env python
"""Build a FAIR4AI evaluation *scaffold* JSON from the checklist CSV.

This is one of two blessed helper scripts (with merge_ratings.py) that make the
`/evaluate-dataset` workflow cheaper and more reliable. Instead of the agent
hand-transcribing the four verbatim fields for all 89 items into one giant Write
(the pattern that triggered ECONNRESET/timeout/403 "at the write step"), this
script pre-fills them deterministically:

  - each response gets `item`, `requirement_definition`, `fair_category`, and
    `ai_fair_criteria` copied VERBATIM from the checklist row (so the tests/ verbatim
    check passes by construction), a default `status` of `meets` (the exception-based
    norm: the agent overrides only the items that fall short or are N/A), and empty
    `evidence`/`notes`/`recommendation`;
  - `--emit-guide` prints a COMPACT, per-section rating guide (requirement definition +
    per-item NA guidance) so the agent never has to load the full CSV into context. The
    agent judges meets/partial/does-not-meet against RATING_RUBRIC.md (§4), not per-item
    cells.

The agent then produces only its judgments and merges them in with merge_ratings.py.

Output schema matches the current example outputs exactly: an 8-field response object,
a `session` block, and a `summary` skeleton with `fair4ai_scores` left as `{}` (the
fair4ai-scoring skill fills it after ratings are merged).

Stdlib only. Usage:
    python scripts/build_response_scaffold.py \
        --checklist /abs/CHECKLIST.csv --out /abs/run/.../scaffold.json
    python scripts/build_response_scaffold.py \
        --checklist /abs/CHECKLIST.csv --out /abs/.../scaffold.json \
        --session-json /abs/.../session.json --emit-guide
    python scripts/build_response_scaffold.py --checklist /abs/CHECKLIST.csv --selftest
"""
import argparse
import csv
import json
import sys

# The 8 fields of a current-schema response, in display order.
RESPONSE_FIELDS = [
    "item",
    "requirement_definition",
    "status",
    "evidence",
    "notes",
    "recommendation",
    "fair_category",
    "ai_fair_criteria",
]

# Columns pulled verbatim into the response (CSV header -> JSON field).
VERBATIM_MAP = {
    "Item": "item",
    "Requirement Definition": "requirement_definition",
    "FAIR category": "fair_category",
    # "AI FAIR Criteria: ..." is matched by prefix (long header) -> ai_fair_criteria
}

# Item-specific rating cell surfaced in the --emit-guide output (never emitted into the
# scaffold JSON itself). Only the N/A condition remains per-item; meets/partial/does-not-
# meet judgment comes from RATING_RUBRIC.md (§4), not the CSV.
GUIDE_SCORING_COLS = ["Scoring: NA"]


def _find_col(fieldnames, name):
    """Return the actual header matching `name` (exact after strip), or None."""
    for h in fieldnames:
        if h and h.strip() == name:
            return h
    return None


def _find_criteria_col(fieldnames):
    """Return the (long) 'AI FAIR Criteria: ...' header, matched by prefix."""
    for h in fieldnames:
        if h and h.strip().startswith("AI FAIR Criteria"):
            return h
    return None


def load_rows(checklist_path):
    """Read the checklist; return (rows, colmap).

    rows: list of dicts (only non-blank-Item rows), each mapping the ORIGINAL header
    to the cell value. colmap: resolved header names for the columns we care about.
    """
    with open(checklist_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        colmap = {
            "item": _find_col(fieldnames, "Item"),
            "requirement_definition": _find_col(fieldnames, "Requirement Definition"),
            "fair_category": _find_col(fieldnames, "FAIR category"),
            "ai_fair_criteria": _find_criteria_col(fieldnames),
            "broad": _find_col(fieldnames, "Broad categories"),
            "note": _find_col(fieldnames, "Note"),
        }
        for key in GUIDE_SCORING_COLS:
            colmap[key] = _find_col(fieldnames, key)

        missing = [k for k in ("item", "requirement_definition", "fair_category",
                               "ai_fair_criteria") if not colmap[k]]
        if missing:
            raise ValueError(
                f"checklist is missing required column(s): {missing} "
                f"(found headers: {fieldnames})"
            )

        item_col = colmap["item"]
        rows = [row for row in reader if (row.get(item_col) or "").strip()]
    return rows, colmap


def _cell(row, header):
    """Verbatim cell value (stripped), or '' if the column is absent."""
    if not header:
        return ""
    return (row.get(header) or "").strip()


def build_responses(rows, colmap):
    """Return the list of scaffold response objects (verbatim fields + empty ratings)."""
    responses = []
    for row in rows:
        resp = {
            "item": _cell(row, colmap["item"]),
            "requirement_definition": _cell(row, colmap["requirement_definition"]),
            "status": "meets",
            "evidence": "",
            "notes": "",
            "recommendation": "",
            "fair_category": _cell(row, colmap["fair_category"]),
            "ai_fair_criteria": _cell(row, colmap["ai_fair_criteria"]),
        }
        # Guarantee exactly the 8 fields in the canonical order.
        responses.append({k: resp[k] for k in RESPONSE_FIELDS})
    return responses


def _blank_session():
    return {
        "evaluation_date": None,
        "ai_model": None,
        "evaluation_method": None,
        "source_files": [],
        "dataset": {
            "title": None, "product_id": None, "repository_url": None,
            "landing_page_url": None, "citation": None,
        },
        "evaluator": {
            "name": None, "affiliation": None, "email": None,
            "relationship_to_dataset": None, "evaluation_purpose": None,
            "evaluation_description": None,
        },
    }


def build_document(rows, colmap, session=None):
    return {
        "session": session if session is not None else _blank_session(),
        "responses": build_responses(rows, colmap),
        "summary": {
            "strengths": [],
            "gaps": [],
            "overall_assessment": "",
            "fair4ai_scores": {},
        },
    }


def group_by_section(rows, colmap):
    """Group rows by `Broad categories`, preserving first-appearance order.

    The same category can recur in non-adjacent CSV blocks; collecting every item of
    a category together gives the ~9 clean sections the batched rating workflow rates
    one at a time. Returns a list of (section_name, [rows]) pairs.
    """
    groups = {}
    order = []
    for row in rows:
        section = _cell(row, colmap["broad"]) or "(uncategorized)"
        if section not in groups:
            groups[section] = []
            order.append(section)
        groups[section].append(row)
    return [(name, groups[name]) for name in order]


def format_guide(rows, colmap):
    """Compact rating guide (markdown), grouped into whole sections. Rating columns only."""
    sections = group_by_section(rows, colmap)
    lines = []
    lines.append(f"# Rating guide — {len(rows)} items in {len(sections)} sections")
    lines.append("")
    lines.append("Rate one section at a time. Judge each item against its Requirement and the")
    lines.append("section-level guidance in RATING_RUBRIC.md (§4) to decide meets / partial / does")
    lines.append("not meet; an item is `N/A` only when its `NA` condition below applies. For blended")
    lines.append("`AI FAIR Criteria`, rate each facet and take the LOWER status. `item`,")
    lines.append("`requirement_definition`, `fair_category`, and `ai_fair_criteria` are already filled")
    lines.append("in the scaffold, and every item defaults to `meets` — you only emit ratings for")
    lines.append("items that are `partial`, `does not meet`, or `N/A` (with a `recommendation` for")
    lines.append("shortfalls). Merge each section's deviations with merge_ratings.py before the next.")
    lines.append("")
    lines.append("Sections: " + ", ".join(f"{name} ({len(rs)})" for name, rs in sections))
    lines.append("")

    for name, section_rows in sections:
        lines.append(f"## Section: {name} — {len(section_rows)} item(s)")
        lines.append("")
        for row in section_rows:
            lines.append(f"### {_cell(row, colmap['item'])}")
            lines.append(f"- Requirement: {_cell(row, colmap['requirement_definition'])}")
            for key in GUIDE_SCORING_COLS:
                val = _cell(row, colmap[key])
                if val:
                    label = key.replace("Scoring: NA", "N/A when").replace("Scoring: ", "")
                    lines.append(f"- {label}: {val}")
            crit = _cell(row, colmap["ai_fair_criteria"])
            fair = _cell(row, colmap["fair_category"])
            note = _cell(row, colmap["note"])
            lines.append(f"- AI FAIR Criteria: {crit or '(none)'}  |  FAIR category: {fair or '(none)'}")
            if note:
                lines.append(f"- Note: {note}")
            lines.append("")
    return "\n".join(lines)


def _selftest():
    import tempfile
    import os

    csv_text = (
        "Item,Requirement Definition,Scoring: NA,FAIR category,"
        "AI FAIR Criteria: Structural | Scientific | Provenance | Governance,"
        "Broad categories,Sub category,mappedEML,Note\n"
        "Descriptive Title,A clear title.,Never NA.,Findable,Provenance,"
        "General,Naming,eml:title,Some note.\n"
        "Access License,A license is present.,Never NA.,Accessible | Reusable,"
        "Provenance | Governance,Governance,Licensing,,\n"
        # A second 'General' row AFTER 'Governance' — non-contiguous; must regroup.
        "Keywords,Has keywords.,Never NA.,Findable,Structural,General,Tags,eml:keyword,\n"
        ",blank item should be skipped,,,,,,,\n"
    )
    with tempfile.TemporaryDirectory() as d:
        cpath = os.path.join(d, "CHECKLIST.csv")
        with open(cpath, "w", encoding="utf-8", newline="") as f:
            f.write(csv_text)
        rows, colmap = load_rows(cpath)
        assert len(rows) == 3, f"blank-Item row must be skipped, got {len(rows)}"
        doc = build_document(rows, colmap)
        resps = doc["responses"]
        assert len(resps) == 3
        # scaffold preserves CSV order (merge is keyed by item, so grouping is guide-only)
        assert [r["item"] for r in resps] == ["Descriptive Title", "Access License", "Keywords"]
        # exactly the 8 fields, in order
        assert list(resps[0].keys()) == RESPONSE_FIELDS, list(resps[0].keys())
        # verbatim copy
        assert resps[0]["item"] == "Descriptive Title"
        assert resps[0]["fair_category"] == "Findable"
        assert resps[1]["ai_fair_criteria"] == "Provenance | Governance"
        # status defaults to meets (exception-based); other rating fields start empty
        for r in resps:
            assert r["status"] == "meets", r["status"]
            assert r["evidence"] == r["notes"] == r["recommendation"] == ""
        # session/summary skeleton
        assert doc["summary"]["fair4ai_scores"] == {}
        assert doc["session"]["dataset"]["title"] is None
        # embedded session is passed through
        doc2 = build_document(rows, colmap, session={"evaluation_date": "2026-01-01"})
        assert doc2["session"] == {"evaluation_date": "2026-01-01"}
        # non-contiguous 'General' rows regroup into ONE section (not two)
        sections = group_by_section(rows, colmap)
        assert [name for name, _ in sections] == ["General", "Governance"], sections
        general_items = [_cell(r, colmap["item"]) for r in dict(sections)["General"]]
        assert general_items == ["Descriptive Title", "Keywords"], general_items
        # guide contains sections and rubric cells, not the mapped* columns
        guide = format_guide(rows, colmap)
        assert guide.count("## Section:") == 2, "must be 2 sections, not one per row"
        assert "## Section: General" in guide and "## Section: Governance" in guide
        assert "Requirement: A clear title." in guide
        assert "N/A when: Never NA." in guide, "guide must surface the per-item NA condition"
        assert "Meets:" not in guide, "removed per-item scoring cells must not appear"
        assert "eml:title" not in guide, "guide must omit non-rating columns"
    print("build_response_scaffold selftest: PASS")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build a FAIR4AI evaluation scaffold JSON from the checklist.")
    ap.add_argument("--checklist", help="absolute path to CHECKLIST.csv")
    ap.add_argument("--out", help="absolute path for the scaffold JSON to write")
    ap.add_argument("--session-json", help="optional path to a JSON file whose contents become the `session` block")
    ap.add_argument("--emit-guide", action="store_true", help="print the compact per-section rating guide to stdout")
    ap.add_argument("--selftest", action="store_true", help="run internal checks and exit")
    args = ap.parse_args(argv)

    # The guide (and any non-ASCII CSV content) is emitted on stdout; on Windows a
    # redirected stdout defaults to cp1252 and would mangle em-dashes/curly quotes.
    # Force utf-8 so the agent captures the guide faithfully.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    if args.selftest:
        _selftest()
        return 0
    if not args.checklist:
        ap.error("--checklist is required unless --selftest is given")

    try:
        rows, colmap = load_rows(args.checklist)
    except FileNotFoundError:
        print(f"ERROR: checklist not found: {args.checklist}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    session = None
    if args.session_json:
        try:
            with open(args.session_json, encoding="utf-8") as f:
                session = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR: could not read --session-json: {e}", file=sys.stderr)
            return 1

    doc = build_document(rows, colmap, session=session)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"Wrote scaffold with {len(doc['responses'])} responses "
              f"(default status 'meets') -> {args.out}", file=sys.stderr)
    else:
        print(f"(no --out given; built {len(doc['responses'])} responses)", file=sys.stderr)

    if args.emit_guide:
        # Guide goes to STDOUT so the agent reads it directly from the tool result.
        print(format_guide(rows, colmap))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
