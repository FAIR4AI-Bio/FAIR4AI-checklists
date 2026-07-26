# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this directory.

## What this agent does

Evaluates biodiversity, ecology, and environmental science datasets for AI-readiness using the FAIR4AI-Bio checklist. Reads a dataset landing page or local metadata files, rates 96 checklist items (`meets | partial | does not meet | N/A`, per `RATING_RUBRIC.md`), and produces a structured JSON report with reproducible FAIR4AI scores across five dimensions (Findable, Accessible, Interoperable, Reusable, AI-ready) plus an overall score — each in **0–1, where 1 is "most FAIR4AI"**. Scores are computed deterministically by the `fair4ai-scoring` skill (`scripts/compute_fair4ai_scores.py`), not estimated.

## Running an evaluation

Type `/evaluate-dataset` in Claude Code chat. The agent will prompt for:

1. **Dataset source** *(required)* — URL to a landing page, or a local path to a directory of metadata files
2. **Checklist file** *(optional)* — defaults to `CHECKLIST.csv`
3. **Template file** *(optional)* — defaults to `example_outputs/FAIR4AI_eval_NEON_beetles_DP1.10022.001_2026-01-25.json`
4. **Output directory** *(optional)* — defaults to current working directory
5. **Output filename** *(optional)* — defaults to `FAIR4AI_eval_<dataset-name>_<YYYY-MM-DD>.json`

For detailed usage examples, see `QUICKSTART.md`.

## Checklist structure

`CHECKLIST.csv` has 8 sections (`Broad categories` column) and 96 items. Key columns: `Item`, `Proposed definition`, `Criteria: Structural/Scientific/Provenance`, `Broad categories`, `Sub category`, `Note`, `Required (core, auto, or recommended)`, `Use-case scope (Condition)`, `Applies-at-level`, `mappedEML`, `mappedDataCite`, `mappedSOSO`, `mappedCroissant`, `Croissant scope`, and `FAIR4AI category` (the dimension(s) each item counts toward for scoring).

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
    { "section": "...", "sub_section": "...", "question": "...", "status": "meets|partial|does not meet|N/A", "evidence": "...", "notes": "...", "recommendation": "...", "fair4ai_category": "Accessible | Reusable" }
  ],
  "summary": {
    "strengths": ["..."],
    "gaps": ["..."],
    "overall_assessment": "...",
    "fair4ai_scores": {
      "findable": 0.83, "accessible": 0.75, "interoperable": 0.6,
      "reusable": 0.7, "ai_ready": 0.33, "overall": 0.64,
      "details": { "findable": { "n_scored": 6, "meets": 4, "partial": 2, "does_not_meet": 0, "na": 1 } }
    }
  }
}
```

`summary.fair4ai_scores` is computed by the **`fair4ai-scoring`** skill (`scripts/compute_fair4ai_scores.py`), not written by hand: `meets → 1`, `partial → 0.5`, `does not meet → 0`, `N/A → excluded`; per-dimension score = mean of contributing items (an item mapped to several dimensions counts in each); overall = equal-weight mean of scored dimensions; all in 0–1.

## Expected score patterns

From prior evaluations of primary observational biodiversity datasets:
- FAIR dimensions (findable, accessible, interoperable, reusable): typically strong (≈0.7–0.9)
- AI-ready: typically weak (≈0.3–0.4)

Universal gaps in most datasets: no ML split guidance, no class distribution statistics, no AI/ML usage history, no CARE Principles documentation.
