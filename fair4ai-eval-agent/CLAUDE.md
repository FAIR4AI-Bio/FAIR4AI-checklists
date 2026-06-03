# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this directory.

## What this agent does

Evaluates biodiversity, ecology, and environmental science datasets for AI-readiness using the FAIR4AI-Bio checklist. Reads a dataset landing page or local metadata files, scores ~80 checklist items, and produces a structured JSON report with FAIR4AI scores across five dimensions (Findable, Accessible, Interoperable, Reusable, AI-ready — each /10).

## Running an evaluation

Type `/evaluate-dataset` in Claude Code chat. The agent will prompt for:

1. **Dataset source** *(required)* — URL to a landing page, or a local path to a directory of metadata files
2. **Checklist file** *(optional)* — defaults to `CHECKLIST.csv`
3. **Template file** *(optional)* — defaults to `example_outputs/FAIR4AI_eval_NEON_beetles_DP1.10022.001_2026-01-25.json`
4. **Output directory** *(optional)* — defaults to current working directory
5. **Output filename** *(optional)* — defaults to `FAIR4AI_eval_<dataset-name>_<YYYY-MM-DD>.json`

For detailed usage examples, see `QUICKSTART.md`.

## Checklist structure

`CHECKLIST.csv` has 8 sections (`Broad categories` column) and ~80 items. Key columns: `Broad categories`, `sub category`, `items`, `Proposed definition`, `note`, `mappedEML`, `mappedDataCite`, `mappedSOSO`, `mappedCroissant`.

Skip rows where `items` is blank, starts with `-`, or where `Broad categories` is `Other`.

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
    { "section": "...", "sub_section": "...", "question": "...", "status": "meets|partial|does not meet|N/A", "evidence": "...", "notes": "...", "recommendation": "..." }
  ],
  "summary": {
    "strengths": ["..."],
    "gaps": ["..."],
    "overall_assessment": "...",
    "fair4ai_scores": {
      "findable": "X/10 — rationale",
      "accessible": "X/10 — rationale",
      "interoperable": "X/10 — rationale",
      "reusable": "X/10 — rationale",
      "ai_ready": "X/10 — rationale"
    }
  }
}
```

## Expected score patterns

From prior evaluations of primary observational biodiversity datasets:
- FAIR dimensions (findable, accessible, interoperable, reusable): typically 7–8/10
- AI-ready: typically 3–4/10

Universal gaps in most datasets: no ML split guidance, no class distribution statistics, no AI/ML usage history, no CARE Principles documentation.

## Known open issues

- `Criteria` column in `CHECKLIST.csv` is mostly empty — population is future work
- No formal version number on the checklist CSV (version noted in `CHECKLIST_OVERVIEW.md`)
