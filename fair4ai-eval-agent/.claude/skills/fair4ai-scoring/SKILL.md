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
  AI-ready`, pipe-separated. Blank for context-only (non-scored) items.

If a scoreable item is missing its `fair4ai_category`, the script excludes it and
prints a warning — fix the response rather than ignoring the warning.

## Scoring rules (what the script does)

- **Per item:** `meets → 1.0`, `partial → 0.5`, `does not meet → 0.0`.
  `N/A` (and any item with a blank category) is **excluded** — it does not count.
- **Multiple categories:** an item mapped to *k* dimensions contributes its score
  to **each** of those *k* dimensions' means.
- **Per-dimension score** = mean of contributing item scores in that dimension → 0–1.
  A dimension with zero scored items (all N/A) is reported as `null` and **omitted**
  from the overall so equal weighting is not skewed.
- **Overall score** = **equal-weight** mean of the (up to five) per-dimension
  scores → 0–1. Every dimension counts equally regardless of how many items it has.
- All scores are in **0–1, where 1 is "most FAIR4AI"**, rounded to 3 decimals.

## Output written to `summary.fair4ai_scores`

```json
"fair4ai_scores": {
  "findable": 0.83, "accessible": 0.75, "interoperable": 0.6,
  "reusable": 0.7, "ai_ready": 0.33, "overall": 0.64,
  "details": {
    "findable": { "n_scored": 6, "meets": 4, "partial": 2, "does_not_meet": 0, "na": 1 }
    // ... one per dimension ...
  }
}
```

The `details` block records per-dimension counts so every score is auditable back
to the items that produced it. When reporting to the user, cite the 0–1
per-dimension scores and the overall score, and note that they are script-computed
(reproducible), not estimated.
