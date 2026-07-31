#!/usr/bin/env python
"""Multipanel figure summarizing FAIR4AI-Bio scores across a batch of datasets.

One panel per FAIR4AI category (Findable, Accessible, Interoperable, Reusable,
AI-ready, Overall). Each panel shows the distribution of per-dataset scores as a
histogram over the 0-1 range, with every dataset drawn as a point (rug) along the
bottom, mean/median marker lines, and a summary-stats inset (n, mean, median, SD,
range).

Reads:  the scores summary CSV from compile_fair4ai_results.py (one row per dataset).
Writes: <out-base>.{png,pdf,svg}

Design tokens (colors, ink, grid) follow the dataviz skill's validated reference
palette; the 6 categorical hues passed the palette validator (light mode). Color is
decorative here — every panel is titled and its stats are printed, so identity never
rests on color alone.

This is the ONLY part of the pipeline that needs third-party packages (numpy +
matplotlib, see scripts/requirements-viz.txt). Scoring and compilation stay
stdlib-only, so if these imports fail this script exits non-zero with an install hint
and the batch skill reports "figure skipped" while still producing the CSV + report.

Usage:
    python scripts/make_fair4ai_figure.py --in-csv <run>/fair4ai_scores_summary_<date>.csv \
        [--out-base <run>/fair4ai_score_distributions_<date>] \
        [--title "..."] [--subtitle "..."] [--footnote "..."] \
        [--model "Claude Haiku 4.5"] [--date 2026-07-30] [--formats png,pdf,svg]
"""
import argparse
import csv
import os
import sys

try:
    import numpy as np
    import matplotlib as mpl
    mpl.use("Agg")
    import matplotlib.pyplot as plt
except ImportError as e:  # graceful: the batch skill catches this and continues
    sys.stderr.write(
        f"ERROR: make_fair4ai_figure.py needs numpy + matplotlib ({e}).\n"
        "Install them with:  python -m pip install -r scripts/requirements-viz.txt\n"
        "(Scoring and the summary CSV do not need these packages.)\n"
    )
    raise SystemExit(2)

# --- design tokens (dataviz reference palette, light mode) ---
SURFACE = "#fcfcfb"
INK = "#0b0b0b"        # primary
INK_2 = "#52514e"      # secondary
MUTED = "#898781"      # axis / labels
GRID = "#e1e0d9"       # hairline gridline
BASELINE = "#c3c2b7"   # axis / baseline

# categorical hues, fixed order (validated); one per panel
CATEGORIES = [
    ("findable",     "Findable",      "#2a78d6"),  # blue
    ("accessible",   "Accessible",    "#eb6834"),  # orange
    ("interoperable", "Interoperable", "#1baf7a"),  # aqua
    ("reusable",     "Reusable",      "#eda100"),  # yellow
    ("ai_ready",     "AI-ready",      "#e87ba4"),  # magenta
    ("overall",      "Overall",       "#008300"),  # green
]


def load_scores(csv_path):
    """Return {key: [floats]} for each panel, skipping null/blank dimension cells."""
    data = {key: [] for key, _, _ in CATEGORIES}
    n_rows = 0
    with open(csv_path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            n_rows += 1
            for key, _, _ in CATEGORIES:
                try:
                    data[key].append(float(row.get(key, "")))
                except (TypeError, ValueError):
                    pass  # excluded dimension (null), not zero
    return data, n_rows


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Render the FAIR4AI score-distribution figure from the summary CSV.")
    ap.add_argument("--in-csv", required=True, help="scores summary CSV (compile step output)")
    ap.add_argument("--out-base", default=None,
                    help="output path stem (default: <csv dir>/fair4ai_score_distributions_<date>)")
    ap.add_argument("--title", default=None, help="figure suptitle")
    ap.add_argument("--subtitle", default=None, help="figure subtitle / thesis line")
    ap.add_argument("--footnote", default=None, help="bottom-left footnote")
    ap.add_argument("--model", default=None, help="evaluation model label for the default footnote")
    ap.add_argument("--date", default=None, help="run date for default filenames/footnote")
    ap.add_argument("--formats", default="png,pdf,svg", help="comma-separated output formats")
    args = ap.parse_args(argv)

    data, n_rows = load_scores(args.in_csv)
    if n_rows == 0:
        sys.stderr.write(f"ERROR: no data rows in {args.in_csv}\n")
        return 1

    csv_dir = os.path.dirname(os.path.abspath(args.in_csv))
    date = args.date or "compiled"
    out_base = args.out_base or os.path.join(csv_dir, f"fair4ai_score_distributions_{date}")

    title = args.title or f"FAIR4AI-Bio scores across {n_rows} datasets"
    subtitle = args.subtitle or (
        "Traditional FAIR dimensions tend to score well; AI-readiness is usually the "
        "weakest dimension — FAIR is necessary but not sufficient for AI-ready data.   "
        "Solid line = mean · dashed = median · dots = individual datasets.")
    model_bit = f" with {args.model}" if args.model else ""
    footnote = args.footnote or (
        f"n = {n_rows} datasets · FAIR4AI-Bio checklist (96 items) · evaluated {date}"
        f"{model_bit} · scores computed by compute_fair4ai_scores.py")

    # --- global font / rc ---
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial", "sans-serif"],
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "text.color": INK,
        "axes.edgecolor": BASELINE,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.labelcolor": INK_2,
    })

    BINS = np.linspace(0.0, 1.0, 11)  # width 0.1

    # common y-limit (max bin count across panels) for comparability
    max_count = 0
    for key, _, _ in CATEGORIES:
        counts, _ = np.histogram(np.asarray(data[key]), bins=BINS)
        max_count = max(max_count, int(counts.max()) if counts.size else 0)
    Y_MAX = max(1, max_count) + max(1, int(np.ceil(max(1, max_count) * 0.18)))

    rng = np.random.default_rng(42)  # deterministic jitter for the rug

    fig, axes = plt.subplots(2, 3, figsize=(13.5, 7.4), constrained_layout=True)
    fig.patch.set_facecolor(SURFACE)

    for ax, (key, label, hue) in zip(axes.flat, CATEGORIES):
        vals = np.asarray(data[key], dtype=float)
        n = vals.size
        if n == 0:
            ax.set_title(label, loc="left", fontsize=13, fontweight="bold", color=INK, pad=6)
            ax.text(0.5, 0.5, "no scored datasets", transform=ax.transAxes,
                    ha="center", va="center", fontsize=10, color=MUTED)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, Y_MAX)
            continue

        # histogram — hue fill, surface edge for the inter-bar gap
        ax.hist(vals, bins=BINS, color=hue, edgecolor=SURFACE, linewidth=1.6,
                alpha=0.92, zorder=2)

        # rug: every dataset as a point along the bottom, slight vertical jitter
        jitter = rng.uniform(0.10 * Y_MAX, 0.16 * Y_MAX, size=n)
        ax.scatter(vals, jitter, s=26, color=hue, edgecolor=SURFACE, linewidth=0.8,
                   alpha=0.9, zorder=3, clip_on=False)

        # mean marker (solid) + median (dashed)
        mean, median = float(np.mean(vals)), float(np.median(vals))
        ax.axvline(mean, color=INK, linewidth=1.6, zorder=4)
        ax.axvline(median, color=INK_2, linewidth=1.4, linestyle=(0, (4, 3)), zorder=4)
        ax.annotate(f"mean {mean:.2f}", xy=(mean, Y_MAX), xytext=(0, -2),
                    textcoords="offset points", ha="center", va="top",
                    fontsize=8.5, color=INK, fontweight="bold")

        # summary-stats inset (upper-left; distributions skew high so the left is clear)
        sd = float(np.std(vals, ddof=1)) if n > 1 else 0.0
        stats = (f"n = {n}\n"
                 f"mean    {mean:.2f}\n"
                 f"median  {median:.2f}\n"
                 f"SD      {sd:.2f}\n"
                 f"min     {vals.min():.2f}\n"
                 f"max     {vals.max():.2f}")
        ax.text(0.035, 0.955, stats, transform=ax.transAxes, ha="left", va="top",
                fontsize=8.4, color=INK_2, family="monospace", zorder=5,
                bbox=dict(boxstyle="round,pad=0.45", facecolor=SURFACE,
                          edgecolor=GRID, linewidth=1.0))

        ax.set_title(label, loc="left", fontsize=13, fontweight="bold", color=INK, pad=6)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, Y_MAX)
        ax.set_xticks(np.arange(0, 1.01, 0.2))
        ax.set_yticks(np.arange(0, Y_MAX + 1, max(1, Y_MAX // 5)))
        ax.set_xlabel("score  (0–1,  1 = most FAIR4AI)", fontsize=9.5, color=INK_2)
        ax.set_ylabel("datasets", fontsize=9.5, color=INK_2)
        ax.yaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(BASELINE)
            ax.spines[side].set_linewidth(1.0)
        ax.tick_params(length=3)

    # --- figure title / subtitle / footnote ---
    fig.suptitle(title, x=0.008, ha="left", fontsize=17, fontweight="bold", color=INK)
    fig.text(0.008, 0.945, subtitle, ha="left", fontsize=10, color=INK_2)
    fig.text(0.008, 0.012, footnote, ha="left", fontsize=8, color=MUTED)

    fig.get_layout_engine().set(rect=(0.006, 0.03, 0.988, 0.90))

    dpi_by_fmt = {"png": 220}
    for ext in [x.strip() for x in args.formats.split(",") if x.strip()]:
        out = f"{out_base}.{ext}"
        fig.savefig(out, dpi=dpi_by_fmt.get(ext), facecolor=SURFACE)
        print("Wrote:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
