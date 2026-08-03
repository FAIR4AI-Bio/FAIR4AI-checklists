#!/usr/bin/env python
"""Compile a folder of FAIR4AI evaluation JSONs into one scores CSV + aggregate stats.

Used by the `summarize-outputs` skill (and, via it, the `batch-evaluate-datasets`
coordinator) after datasets have been evaluated. Each dataset produces a
`FAIR4AI_eval_<short_name>_<TIMESTAMP>.json` scored by `compute_fair4ai_scores.py`,
where `<TIMESTAMP>` is either a legacy date `YYYY-MM-DD` or a to-the-second
`YYYY-MM-DD_HHMMSS`. This script:

  - determines the dataset list either from a normalized source CSV (schema:
    email,name,dataset_short_name,url,notes) OR, when `--source-csv` is omitted,
    by discovering it from the evaluation JSONs themselves (short_name parsed from
    each filename; url/title/email read from each JSON's `session` block);
  - collects every `FAIR4AI_eval_*.json` in the results directory, groups them by
    short_name, and by default (`--dedup latest`) keeps only the newest run of each
    dataset, reporting the older runs it superseded; `--dedup all` keeps every run
    (one row per file, disambiguated by a `run_timestamp` column);
  - pulls each chosen JSON's title, the two-assessment 0-1 scores (Traditional FAIR:
    F/A/I/R + overall_fair; AI-FAIR: ml_ready/ai_ready_for_task/traceable/
    care_compliance + overall_ai_fair), per-status counts, and response count;
  - optionally joins a per-dataset confidence level from a confidence-map JSON;
  - writes a one-row-per-result summary CSV (sorted by AI-FAIR overall, high to low); and
  - prints an `AGG:{json}` line with cross-dataset aggregates (fair/ai-fair means, overall
    means, n, missing list, superseded list, by-confidence groupings) that the summarizer
    uses to author the summary report.

Stdlib-only (no third-party dependencies), so scoring/compilation never depends on
the plotting stack. The figure is produced separately by `make_fair4ai_figure.py`.

Usage:
    python scripts/compile_fair4ai_results.py \
        --results-dir <run>/evaluation_results \
        [--source-csv  <run>/batch_datasets_<date>.csv] \
        [--out-csv    <run>/fair4ai_scores_summary_<date>.csv] \
        [--confidence-map <run>/confidence_map.json] \
        [--dedup latest|all] \
        [--date 2026-07-30] \
        [--agg-out <run>/aggregates.json]
"""
import argparse
import csv
import glob
import json
import os
import re
import sys

FAIR_DIMS = ["findable", "accessible", "interoperable", "reusable"]
AI_CATS = ["ml_ready", "ai_ready_for_task", "traceable", "care_compliance"]
CSV_COLS = [
    "dataset_short_name", "title", "url", "evaluator_email",
    "findable", "accessible", "interoperable", "reusable", "overall_fair",
    "ml_ready", "ai_ready_for_task", "traceable", "care_compliance", "overall_ai_fair",
    "n_meets", "n_partial", "n_does_not_meet", "n_na", "confidence",
    "run_timestamp", "json_file",
]

# FAIR4AI_eval_<short_name>_<TIMESTAMP>.json  where <TIMESTAMP> is
# YYYY-MM-DD  or  YYYY-MM-DD_HHMMSS.  short_name may itself contain underscores
# and dots (e.g. NEON_beetles_DP1.10022.001), so <short> is greedy and the
# timestamp is anchored at the end.
_FNAME_RE = re.compile(
    r"^FAIR4AI_eval_(?P<short>.+)_(?P<ts>\d{4}-\d{2}-\d{2}(?:_\d{6})?)\.json$"
)


def parse_filename(fname):
    """(short_name, timestamp) from a FAIR4AI_eval_*.json filename, or (None, None)."""
    m = _FNAME_RE.match(os.path.basename(fname))
    if not m:
        return None, None
    return m.group("short"), m.group("ts")


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


def collect_jsons(results_dir):
    """Group evaluation JSONs by short_name.

    Returns short_name -> list of (timestamp, path) sorted ascending by timestamp
    (so the last element is the newest run). Unparseable filenames are skipped.
    """
    by_short = {}
    for path in glob.glob(os.path.join(results_dir, "FAIR4AI_eval_*.json")):
        short, ts = parse_filename(path)
        if not short:
            continue
        by_short.setdefault(short, []).append((ts, path))
    for short in by_short:
        by_short[short].sort(key=lambda x: x[0])
    return by_short


def derive_source_from_json(path):
    """Fallback {url, email, name} pulled from a JSON's session block."""
    try:
        with open(path, encoding="utf-8") as f:
            doc = json.load(f)
    except (OSError, ValueError):
        return {"url": "", "email": "", "name": ""}
    ds = (doc.get("session", {}) or {}).get("dataset", {}) or {}
    ev = (doc.get("session", {}) or {}).get("evaluator", {}) or {}
    return {
        "url": (ds.get("landing_page_url") or ds.get("repository_url") or "").strip(),
        "email": (ev.get("email") or "").strip(),
        "name": (ev.get("name") or ds.get("title") or "").strip(),
    }


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


def build_row(short, meta, ts, jpath):
    with open(jpath, encoding="utf-8") as f:
        doc = json.load(f)
    scores = (doc.get("summary", {}) or {}).get("fair4ai_scores", {}) or {}
    tf = scores.get("traditional_fair", {}) or {}
    af = scores.get("ai_fair", {}) or {}
    counts = count_statuses(doc)
    return {
        "short_name": short,
        "title": (doc.get("session", {}).get("dataset", {}) or {}).get("title") or "",
        "url": meta.get("url", ""),
        "email": meta.get("email", ""),
        "fair": {d: tf.get(d) for d in FAIR_DIMS},
        "overall_fair": tf.get("overall"),
        "ai": {c: af.get(c) for c in AI_CATS},
        "overall_ai_fair": af.get("overall"),
        "counts": counts,
        "n_responses": len(doc.get("responses", [])),
        "run_timestamp": ts or "",
        "json_file": os.path.basename(jpath),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Compile FAIR4AI evaluation JSONs into a scores CSV + aggregates.")
    ap.add_argument("--results-dir", required=True,
                    help="folder containing FAIR4AI_eval_*.json files")
    ap.add_argument("--source-csv", default=None,
                    help="optional normalized batch CSV (email,name,dataset_short_name,url,notes); "
                         "if omitted, datasets are discovered from the JSON files themselves")
    ap.add_argument("--out-csv", default=None,
                    help="output CSV path (default: <results-dir>/fair4ai_scores_summary_<date>.csv)")
    ap.add_argument("--date", default=None,
                    help="run label used in the default output filename")
    ap.add_argument("--dedup", choices=("latest", "all"), default="latest",
                    help="latest (default): keep only the newest run per dataset; "
                         "all: keep every run (one row per file)")
    ap.add_argument("--confidence-map", default=None,
                    help="JSON {short_name: 'high|medium|low'}; confidence column blank if absent")
    ap.add_argument("--agg-out", default=None,
                    help="also write the AGG aggregate JSON to this file")
    args = ap.parse_args(argv)

    results_dir = os.path.abspath(args.results_dir)
    confidence = read_confidence_map(args.confidence_map)
    by_short = collect_jsons(results_dir)

    # --- determine the dataset list + per-dataset metadata (url/email/name) ---
    if args.source_csv:
        src = read_source_csv(args.source_csv)
    else:
        # discover from the JSON files; metadata comes from each JSON's newest run.
        src = {}
        for short, runs in by_short.items():
            src[short] = derive_source_from_json(runs[-1][1])

    out_csv = args.out_csv or os.path.join(
        results_dir, f"fair4ai_scores_summary_{args.date or 'compiled'}.csv")

    rows = []
    missing = []
    superseded = []  # (short, json_file) older runs dropped by --dedup latest
    for sn, meta in src.items():
        runs = by_short.get(sn, [])
        if not runs:
            missing.append(sn)
            continue
        if args.dedup == "latest":
            chosen = [runs[-1]]
            superseded.extend((sn, os.path.basename(p)) for (_, p) in runs[:-1])
        else:
            chosen = runs
        for ts, jpath in chosen:
            rows.append(build_row(sn, meta, ts, jpath))

    # --- write CSV (sorted by AI-FAIR overall desc, nulls last) ---
    os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(CSV_COLS)
        for r in sorted(rows, key=lambda x: (x["overall_ai_fair"] is None,
                                             -(x["overall_ai_fair"] or 0))):
            w.writerow([
                r["short_name"], r["title"], r["url"], r["email"],
                r["fair"]["findable"], r["fair"]["accessible"], r["fair"]["interoperable"],
                r["fair"]["reusable"], r["overall_fair"],
                r["ai"]["ml_ready"], r["ai"]["ai_ready_for_task"], r["ai"]["traceable"],
                r["ai"]["care_compliance"], r["overall_ai_fair"],
                r["counts"]["meets"], r["counts"]["partial"], r["counts"]["does not meet"],
                r["counts"]["N/A"], confidence.get(r["short_name"], ""),
                r["run_timestamp"], r["json_file"],
            ])
    print("Wrote:", out_csv)

    # --- aggregates for the summary report ---
    agg = {
        "n_total": len(rows),
        "dedup": args.dedup,
        "missing": missing,
        "superseded": [f"{sn}: {fn}" for (sn, fn) in superseded],
        "fair_means": {d: mean([r["fair"][d] for r in rows]) for d in FAIR_DIMS},
        "overall_fair_mean": mean([r["overall_fair"] for r in rows]),
        "ai_fair_means": {c: mean([r["ai"][c] for r in rows]) for c in AI_CATS},
        "overall_ai_fair_mean": mean([r["overall_ai_fair"] for r in rows]),
        "by_confidence": {},
        "csv_path": out_csv,
    }
    for level in ("high", "medium", "low", ""):
        names = sorted({r["short_name"] for r in rows
                        if (confidence.get(r["short_name"], "") or "") == level})
        agg["by_confidence"][level or "unspecified"] = names

    if args.agg_out:
        with open(args.agg_out, "w", encoding="utf-8") as f:
            json.dump(agg, f, indent=2)
        print("Wrote:", args.agg_out)

    if superseded:
        print("Superseded (older runs ignored under --dedup latest):",
              ", ".join(f"{sn} [{fn}]" for (sn, fn) in superseded), file=sys.stderr)
    if missing:
        print("WARNING: no evaluation JSON found for:", ", ".join(missing),
              file=sys.stderr)

    print("AGG:" + json.dumps(agg))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
