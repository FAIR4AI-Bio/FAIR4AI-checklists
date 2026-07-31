# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this directory.

## What this agent does

Evaluates biodiversity, ecology, and environmental science datasets for AI-readiness using the FAIR4AI-Bio checklist. Reads a dataset landing page or local metadata files, rates 96 checklist items (`meets | partial | does not meet | N/A`, per `RATING_RUBRIC.md`), and produces a structured JSON report with **two reproducible assessments** — **Traditional FAIR** (Findable, Accessible, Interoperable, Reusable + overall) and **AI-FAIR** (ml_ready, ai_ready_for_task, traceable, care_compliance + overall) — each score in **0–1, where 1 is "most FAIR4AI"**. Scores are computed deterministically by the `fair4ai-scoring` skill (`scripts/compute_fair4ai_scores.py`), not estimated. Reporting the two side by side operationalizes the thesis that FAIR is necessary but not sufficient for AI-ready data.

## Running an evaluation

Type `/evaluate-dataset` in Claude Code chat. The agent will prompt for:

1. **Dataset source** *(required)* — URL to a landing page, or a local path to a directory of metadata files
2. **Checklist file** *(optional)* — defaults to `CHECKLIST.csv`
3. **Template file** *(optional)* — defaults to `example_outputs/FAIR4AI_eval_NEON_beetles_DP1.10022.001_2026-07-26.json` (the current-schema example)
4. **Output directory** *(optional)* — defaults to current working directory
5. **Output filename** *(optional)* — defaults to `FAIR4AI_eval_<dataset-name>_<YYYY-MM-DD>.json`

For detailed usage examples, see `QUICKSTART.md`.

## Running a batch

Type `/batch-evaluate-datasets` to evaluate a whole list of datasets at once. It reads a flexible
input list (`.txt`/`.csv`/`.md`), normalizes it to a standard CSV, coordinates one sub-agent per
dataset in parallel (waves of 5; default model **Claude Haiku 4.5**, `claude-haiku-4-5-20251001` —
it asks), then writes all evaluation JSONs plus a compiled scores CSV, a summary figure, and a
narrative report into one self-contained, resumable **run folder** (`batch_run_<date>/`). Sub-agents
run `evaluate-dataset` in its **Batch / non-interactive mode**.

## Batch scripts & dependencies

- `scripts/compute_fair4ai_scores.py` — scoring (stdlib-only); the scoring authority for every run.
- `scripts/compile_fair4ai_results.py` — compiles evaluation JSONs → scores CSV + `AGG:{...}`
  aggregates (stdlib-only).
- `scripts/make_fair4ai_figure.py` — 2×5 two-row (Traditional FAIR + AI-FAIR) score-distribution
  figure. **Needs `numpy` + `matplotlib`** (`scripts/requirements-viz.txt`); the figure step degrades
  gracefully if they're absent, so scoring/compilation never depend on the plotting stack.

## Checklist structure

`CHECKLIST.csv` has 9 sections (`Broad categories` column, including **Governance**) and 96 items. Key columns: `Item`, `Proposed definition`, `Criteria: Structural/Scientific/Provenance` (canonical tokens `Structural`/`Scientific`/`Provenance` and their `/`-joined blends; drives AI-FAIR), `Broad categories`, `Sub category`, `Note`, `Required (core, auto, or recommended)`, `Use-case scope (Condition)`, `Applies-at-level`, `mappedEML`, `mappedDataCite`, `mappedSOSO`, `mappedCroissant`, `Croissant scope`, and `FAIR4AI category` (the FAIR dimension(s) each item counts toward; drives Traditional FAIR). The five items in the **Governance** broad category drive the AI-FAIR `care_compliance` score via each response's `section` value.

Skip only rows where `Item` is blank. `Use-case scope (Condition)` governs the `N/A` decision (see `RATING_RUBRIC.md` §3).

## Output JSON schema

```json
{
  "session": {
    "evaluation_date": "YYYY-MM-DD",
    "ai_model": "...",
    "evaluation_method": "...",
    "source_files": ["..."],
    "dataset": { "title": "...", "product_id": "...", "repository_url": "...", "landing_page_url": "...", "citation": "..." },
    "evaluator": { "name": "...", "affiliation": "...", "email": "...", "relationship_to_dataset": "...", "evaluation_purpose": "...", "evaluation_description": "..." }
  },
  "responses": [
    { "section": "...", "sub_section": "...", "question": "...", "status": "meets|partial|does not meet|N/A", "evidence": "...", "notes": "...", "recommendation": "...", "fair4ai_category": "Accessible | Reusable", "criteria": "Provenance/Structural" }
  ],
  "summary": {
    "strengths": ["..."],
    "gaps": ["..."],
    "overall_assessment": "...",
    "fair4ai_scores": {
      "traditional_fair": {
        "findable": 0.82, "accessible": 0.83, "interoperable": 0.83, "reusable": 0.62,
        "overall": 0.78,
        "details": { "findable": { "n_scored": 17, "meets": 14, "partial": 0, "does_not_meet": 3, "na": 3 } }
      },
      "ai_fair": {
        "ml_ready": 0.73, "ai_ready_for_task": 0.71, "traceable": 0.67,
        "care_compliance": 1.0, "overall": 0.78,
        "components": { "structural": { "score": 0.73, "n_scored": 41, "meets": 24, "partial": 12, "does_not_meet": 5, "na": 7 } }
      }
    }
  }
}
```

`summary.fair4ai_scores` is computed by the **`fair4ai-scoring`** skill (`scripts/compute_fair4ai_scores.py`), not written by hand. Per item: `meets → 1`, `partial → 0.5`, `does not meet → 0`, `N/A`/blank → excluded; any all-N/A dimension/facet is `null` and omitted from means. Two assessments (both 0–1):
- **Traditional FAIR** — per-dimension mean from `fair4ai_category` (the `AI-ready` token is ignored); `overall` = equal-weight mean of the non-null dimensions.
- **AI-FAIR** — facet base scores `structural`/`scientific`/`provenance` (from `criteria`) and `governance` (from the Governance `section`); then `ml_ready` = structural, `ai_ready_for_task` = mean(structural, scientific), `traceable` = mean(provenance, structural), `care_compliance` = governance; `overall` = equal-weight mean of the four. Categories combine by averaging sub-scores.

## Expected score patterns

From prior evaluations of primary observational biodiversity datasets:
- Traditional FAIR (findable, accessible, interoperable, reusable): typically strong (≈0.7–0.9), though `reusable` often drags lower.
- AI-FAIR: usually lags Traditional FAIR; the `scientific` facet (fitness-for-task) and `care_compliance` are the common weak spots — the FAIR-vs-AI-FAIR overall gap is the headline finding.

Universal gaps in most datasets: no ML split guidance, no class distribution statistics, no AI/ML usage history, and thin CARE/governance documentation (permission, stewards, consent).
