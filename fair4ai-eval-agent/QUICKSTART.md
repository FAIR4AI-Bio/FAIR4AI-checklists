# Quickstart: `/evaluate-dataset`

This slash command evaluates a biodiversity, ecology, or environmental science dataset against the FAIR4AI-Bio checklist and produces a structured JSON evaluation report.

---

## What it does

The agent reads the checklist CSV, fetches or reads the dataset's metadata, and scores each checklist item as **meets / partial / does not meet / N/A**. For every gap it finds, it writes a specific, actionable recommendation. The result is saved as a JSON file you can share, archive, or use to track improvements over time.

---

## How to invoke it

In the Claude Code chat, type:

```
/evaluate-dataset
```

The agent will immediately prompt you for the parameters it needs.

---

## Parameters

The agent will ask for five inputs. Only #1 is required — hit Enter to accept the default for any of the others.

| # | Parameter | Required? | Default |
|---|-----------|-----------|---------|
| 1 | **Dataset source** — URL to a landing page, or local path to a directory of metadata files | Yes | — |
| 2 | **Checklist file** — path to the checklist CSV | No | `CHECKLIST.csv` in the current directory |
| 3 | **Template file** — path to the output structure template JSON | No | `example_outputs/FAIR4AI_eval_NEON_beetles_DP1.10022.001_2026-01-25.json` in the current directory |
| 4 | **Output directory** — where to save the report | No | Current working directory |
| 5 | **Output filename** | No | `FAIR4AI_eval_<dataset-name>_<YYYY-MM-DD>.json` |

---

## Supported dataset sources

**URLs** — the agent fetches the landing page and looks for:
- `<script type="application/ld+json">` (schema.org / JSON-LD)
- Linked EML, DataCite XML, or DarwinCore Archive files
- REST API endpoints (it tries common patterns for NEON, GBIF, DataONE, Zenodo, Dryad, Hugging Face, etc.)

**Local paths** — the agent reads all files in the directory, prioritizing:
- schema.org JSON-LD, EML XML, DataCite XML
- README and documentation markdown files
- Any CSV, JSON, or text files with metadata content

Richer metadata sources produce more accurate evaluations. If the landing page is thin, point the agent to a directory of downloaded metadata files instead.

---

## What the output looks like

The JSON report has three top-level blocks:

### `session`
Who ran the evaluation, when, using which source files, and basic dataset identity (title, landing page URL, citation).

### `responses`
One object per checklist item, organized by `section` and `sub_section` to match the checklist CSV. Each response contains:

```json
{
  "section": "Data Quality",
  "sub_section": "Integrity",
  "question": "The dataset implements checksums for file integrity verification.",
  "status": "does not meet",
  "evidence": "No mention of checksums in any metadata source reviewed.",
  "notes": "",
  "recommendation": "Generate and publish SHA-256 checksums for all released data files..."
}
```

**Status values:**
- `meets` — criterion is fully satisfied
- `partial` — criterion is addressed but incompletely
- `does not meet` — criterion is absent
- `N/A` — criterion does not apply to this dataset type

### `summary`
- `strengths` — list of notable positives
- `gaps` — list of notable gaps
- `overall_assessment` — 2–3 sentence narrative
- `fair4ai_scores` — scores out of 10 for Findable, Accessible, Interoperable, Reusable, and AI-ready, each with a one-line rationale

---

## Example sessions

### Evaluating from a URL
```
/evaluate-dataset

Dataset source: https://data.neonscience.org/data-products/DP1.10022.001
Checklist file: [Enter]
Template file: [Enter]
Output directory: [Enter]
Output filename: [Enter]
```
Output file: `FAIR4AI_eval_Ground_beetles_sampled_from_pitfall_traps_2026-04-30.json`

---

### Evaluating from local metadata files
```
/evaluate-dataset

Dataset source: C:/Users/me/datasets/my-beetle-survey/metadata/
Checklist file: [Enter]
Template file: [Enter]
Output directory: C:/Users/me/datasets/my-beetle-survey/
Output filename: FAIR4AI_eval_my-beetle-survey.json
```

---

### Using a custom checklist
```
/evaluate-dataset

Dataset source: https://www.gbif.org/dataset/abc123
Checklist file: C:/projects/FAIR4AI/updated_checklist_v2.csv
Template file: [Enter]
Output directory: [Enter]
Output filename: [Enter]
```

---

## After the evaluation

At the end of the session the agent prints:
- The full path of the saved JSON file
- A status count summary (e.g., "42 meets · 18 partial · 11 does not meet · 9 N/A")
- FAIR4AI scores at a glance
- Top 3 priority recommendations

You can re-run the command on the same dataset after making improvements and compare outputs to track progress.

---

## Updating the checklist or template

- **New checklist items**: add rows to the checklist CSV following the existing column structure. The agent reads the CSV fresh each run.
- **New output fields**: edit the template JSON. The agent uses it as a structural reference, not a data source.
- **Changing defaults**: update the checklist filename or template filename in `.claude/commands/evaluate-dataset.md` under the "Gather parameters" step.

---

## Files involved

| File | Role |
|------|------|
| `.claude/commands/evaluate-dataset.md` | Defines the `/evaluate-dataset` command and evaluation workflow |
| `CLAUDE.md` | Project context auto-loaded by Claude Code each session |
| `CHECKLIST.csv` | Default checklist source |
| `example_outputs/FAIR4AI_eval_NEON_beetles_DP1.10022.001_2026-01-25.json` | Default output template |
| `CHECKLIST_OVERVIEW.md` | Human-readable checklist summary (reference) |
