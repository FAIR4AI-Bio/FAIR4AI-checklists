---
name: fair4ai-scoring
description: Compute reproducible, quantitative FAIR4AI scores (0-1) from a FAIR4AI evaluation JSON by running scripts/compute_fair4ai_scores.py. Use after per-item statuses are assigned, to populate summary.fair4ai_scores. Invoke whenever you need FAIR4AI dimension scores or an overall score for an evaluation.
---

# FAIR4AI scoring skill

Turn the per-item `meets | partial | does not meet | N/A` ratings in a FAIR4AI
evaluation JSON into **quantitative, traceable, reproducible** scores. Scores are
computed by a deterministic Python script — never estimate them by hand.

## When to use

- During `/evaluate-dataset`, after Step 4 (every response has a `status` and a
  `fair4ai_category`) and before writing/reporting the file, to populate
  `summary.fair4ai_scores`.
- Any time you need to (re)compute scores for an existing evaluation JSON.

## How to run

From the agent directory:

```bash
python scripts/compute_fair4ai_scores.py <path/to/eval.json>
```

This computes the scores and **writes them back** into `summary.fair4ai_scores`.
Options:

- `--dry-run` — print the scores without modifying the file.
- `--selftest` — run the script's internal correctness checks (no input file needed).

On Windows use `python` (not `python3`). The script is stdlib-only — no install step.

## Input contract

The script reads `responses[]` from the JSON. Each response must carry:

- `status` — one of `meets`, `partial`, `does not meet`, `N/A` (case-insensitive).
- `fair4ai_category` — copied verbatim from the checklist's `FAIR4AI category`
  column: one or more of `Findable | Accessible | Interoperable | Reusable |
  AI-ready`, pipe-separated. Blank for context-only (non-scored) items. Drives the
  **Traditional FAIR** assessment (the `AI-ready` token is ignored here).
- `criteria` — copied verbatim from the checklist's `Criteria:
  Structural/Scientific/Provenance` column: one or more of `Structural`,
  `Scientific`, `Provenance` (e.g. `Structural/Scientific`), or blank. Drives the
  **AI-FAIR** assessment.
- `section` — the checklist **Broad category** verbatim. Items whose section is
  `Governance` feed the AI-FAIR `care_compliance` category, so this must be copied
  exactly (case-insensitive match on `governance`).

If a scoreable item is missing its `fair4ai_category`, the script excludes it from
Traditional FAIR; the parser also warns on an unrecognized `criteria` value or a
scoreable item that maps to nothing at all. Fix the response rather than ignoring
the warning.

## Scoring rules (what the script does)

Per item: `meets → 1.0`, `partial → 0.5`, `does not meet → 0.0`; `N/A` (and any
blank facet) is **excluded**. A dimension/facet with zero scored items is `null` and
**omitted** from every mean that would include it, so equal weighting is preserved.
The script computes **two assessments**, both in **0–1 where 1 is "most FAIR4AI"**,
rounded to 3 decimals.

**Traditional FAIR** (from `fair4ai_category`):

- Per-dimension score (`findable`/`accessible`/`interoperable`/`reusable`) = mean of
  contributing item scores; an item mapped to *k* dimensions counts in each.
- `overall` = **equal-weight** mean of the (up to four) non-null dimension scores.

**AI-FAIR** (from `criteria` + the Governance section) — first four **facet base
scores** (means of contributing items): `structural`, `scientific`, `provenance`
(from `criteria`), and `governance` (items whose `section` is Governance). Then the
four categories are **equal-weight means of their non-null facet components**:

- `ml_ready` = `structural`
- `ai_ready_for_task` = mean(`structural`, `scientific`)
- `traceable` = mean(`provenance`, `structural`)
- `care_compliance` = `governance`
- `overall` = equal-weight mean of the four non-null categories.

Facets deliberately overlap (structural feeds three categories) — this encodes the
hierarchy ML-ready ⊆ AI-ready-for-task. Categories combine by **averaging
sub-scores**, not by pooling items.

## Output written to `summary.fair4ai_scores`

```json
"fair4ai_scores": {
  "traditional_fair": {
    "findable": 0.82, "accessible": 0.83, "interoperable": 0.83, "reusable": 0.62,
    "overall": 0.78,
    "details": {
      "findable": { "n_scored": 17, "meets": 14, "partial": 0, "does_not_meet": 3, "na": 3 }
      // ... one per dimension ...
    }
  },
  "ai_fair": {
    "ml_ready": 0.73, "ai_ready_for_task": 0.71, "traceable": 0.67,
    "care_compliance": 1.0, "overall": 0.78,
    "components": {
      "structural": { "score": 0.73, "n_scored": 41, "meets": 24, "partial": 12, "does_not_meet": 5, "na": 7 },
      "scientific": { "...": "..." }, "provenance": { "...": "..." }, "governance": { "...": "..." }
    }
  }
}
```

The `details`/`components` blocks record per-dimension and per-facet counts so every
score is auditable back to the items that produced it. When reporting to the user,
cite both the **Overall FAIR** and **Overall AI-FAIR** scores (plus the four AI-FAIR
categories), and note that they are script-computed (reproducible), not estimated.
