#!/usr/bin/env python
"""Compile a folder of FAIR4AI evaluation JSONs into one scores CSV + aggregate stats.

Used by the `batch-evaluate-datasets` skill after every dataset in a batch has been
evaluated (each dataset producing a `FAIR4AI_eval_<short_name>_<date>.json` scored by
`compute_fair4ai_scores.py`). This script:

  - reads the batch's normalized source CSV (schema: email,name,dataset_short_name,url,notes)
    to map each short_name -> {url, email, name};
  - glob-matches each short_name's evaluation JSON in the results directory and pulls its
    title, six 0-1 scores, per-status counts, and response count;
  - optionally joins a per-dataset confidence level from a confidence-map JSON;
  - writes a one-row-per-dataset summary CSV (sorted by overall score, high to low); and
  - prints an `AGG:{json}` line with cross-dataset aggregates (means, n, missing list,
    by-confidence groupings) that the coordinator uses to author the summary report.

Stdlib-only (no third-party dependencies), so batch scoring/compilation never depends on
the plotting stack. The figure is produced separately by `make_fair4ai_figure.py`.

Usage:
    python scripts/compile_fair4ai_results.py \
        --results-dir <run>/evaluation_results \
        --source-csv  <run>/batch_datasets_<date>.csv \
        [--out-csv    <run>/fair4ai_scores_summary_<date>.csv] \
        [--confidence-map <run>/confidence_map.json] \
        [--date 2026-07-30] \
        [--json-pattern "FAIR4AI_eval_{short}_*.json"] \
        [--agg-out <run>/aggregates.json]
"""
import argparse
import csv
import glob
import json
import os
import sys

DIMS = ["findable", "accessible", "interoperable", "reusable", "ai_ready"]
CSV_COLS = [
    "dataset_short_name", "title", "url", "evaluator_email",
    "findable", "accessible", "interoperable", "reusable", "ai_ready", "overall",
    "n_meets", "n_partial", "n_does_not_meet", "n_na", "confidence", "json_file",
]


def read_source_csv(path):
    """short_name -> {url, email, name}, preserving CSV row order."""
    src = {}
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            sn = (row.get("dataset_short_name") or "").strip()
            if sn:
                src[sn] = {
                    "url": (row.get("url") or "").strip(),
                    "email": (row.get("email") or "").strip(),
                    "name": (row.get("name") or "").strip(),
                }
    return src


def read_confidence_map(path):
    if not path or not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {str(k): (str(v).strip() if v is not None else "") for k, v in data.items()}


def find_json(results_dir, short, pattern, date):
    """Locate a dataset's evaluation JSON. Prefers an exact date match, else globs."""
    if date:
        exact = os.path.join(results_dir, f"FAIR4AI_eval_{short}_{date}.json")
        if os.path.exists(exact):
            return exact
    matches = sorted(glob.glob(os.path.join(results_dir, pattern.format(short=short))))
    return matches[-1] if matches else None


def count_statuses(doc):
    counts = {"meets": 0, "partial": 0, "does not meet": 0, "N/A": 0}
    for r in doc.get("responses", []):
        s = str(r.get("status", "")).strip().lower()
        if s == "meets":
            counts["meets"] += 1
        elif s == "partial":
            counts["partial"] += 1
        elif s in ("does not meet", "does-not-meet"):
            counts["does not meet"] += 1
        elif s in ("n/a", "na"):
            counts["N/A"] += 1
    return counts


def mean(vals):
    vals = [v for v in vals if v is not None]
    return round(sum(vals) / len(vals), 3) if vals else None


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Compile FAIR4AI evaluation JSONs into a scores CSV + aggregates.")
    ap.add_argument("--results-dir", required=True,
                    help="folder containing FAIR4AI_eval_*.json files")
    ap.add_argument("--source-csv", required=True,
                    help="normalized batch CSV (email,name,dataset_short_name,url,notes)")
    ap.add_argument("--out-csv", default=None,
                    help="output CSV path (default: <results-dir>/fair4ai_scores_summary_<date>.csv)")
    ap.add_argument("--date", default=None,
                    help="run date used in default filenames and exact-match lookups")
    ap.add_argument("--confidence-map", default=None,
                    help="JSON {short_name: 'high|medium|low'}; confidence column blank if absent")
    ap.add_argument("--json-pattern", default="FAIR4AI_eval_{short}_*.json",
                    help="glob pattern for a dataset's JSON (use {short} placeholder)")
    ap.add_argument("--agg-out", default=None,
                    help="also write the AGG aggregate JSON to this file")
    args = ap.parse_args(argv)

    results_dir = os.path.abspath(args.results_dir)
    src = read_source_csv(args.source_csv)
    confidence = read_confidence_map(args.confidence_map)

    out_csv = args.out_csv or os.path.join(
        results_dir, f"fair4ai_scores_summary_{args.date or 'compiled'}.csv")

    rows = []
    for sn in src:
        jpath = find_json(results_dir, sn, args.json_pattern, args.date)
        if not jpath:
            rows.append({"short_name": sn, "missing": True})
            continue
        with open(jpath, encoding="utf-8") as f:
            doc = json.load(f)
        scores = (doc.get("summary", {}) or {}).get("fair4ai_scores", {}) or {}
        counts = count_statuses(doc)
        rows.append({
            "short_name": sn,
            "title": (doc.get("session", {}).get("dataset", {}) or {}).get("title") or "",
            "url": src[sn]["url"],
            "email": src[sn]["email"],
            "scores": {d: scores.get(d) for d in DIMS},
            "overall": scores.get("overall"),
            "counts": counts,
            "n_responses": len(doc.get("responses", [])),
            "confidence": confidence.get(sn, ""),
            "json_file": os.path.basename(jpath),
        })

    # --- write CSV (sorted by overall desc, nulls/missing last) ---
    scored = [r for r in rows if not r.get("missing")]
    os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(CSV_COLS)
        for r in sorted(scored, key=lambda x: (x["overall"] is None, -(x["overall"] or 0))):
            w.writerow([
                r["short_name"], r["title"], r["url"], r["email"],
                r["scores"]["findable"], r["scores"]["accessible"], r["scores"]["interoperable"],
                r["scores"]["reusable"], r["scores"]["ai_ready"], r["overall"],
                r["counts"]["meets"], r["counts"]["partial"], r["counts"]["does not meet"],
                r["counts"]["N/A"], r["confidence"], r["json_file"],
            ])
    print("Wrote:", out_csv)

    # --- aggregates for the summary report ---
    agg = {
        "n_total": len(scored),
        "missing": [r["short_name"] for r in rows if r.get("missing")],
        "dim_means": {d: mean([r["scores"][d] for r in scored]) for d in DIMS},
        "overall_mean": mean([r["overall"] for r in scored]),
        "by_confidence": {},
        "csv_path": out_csv,
    }
    for level in ("high", "medium", "low", ""):
        names = [r["short_name"] for r in scored if (r["confidence"] or "") == level]
        agg["by_confidence"][level or "unspecified"] = names

    if args.agg_out:
        with open(args.agg_out, "w", encoding="utf-8") as f:
            json.dump(agg, f, indent=2)
        print("Wrote:", args.agg_out)

    if agg["missing"]:
        print("WARNING: no evaluation JSON found for:", ", ".join(agg["missing"]),
              file=sys.stderr)

    print("AGG:" + json.dumps(agg))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
