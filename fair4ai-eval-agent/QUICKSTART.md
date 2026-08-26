# Quickstart: `/evaluate-dataset`

This skill evaluates a biodiversity, ecology, or environmental science dataset against the FAIR4AI-Bio checklist and produces a structured JSON evaluation report. Invoke it as `/evaluate-dataset`.

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

The agent will ask for six inputs. Only #1 is required — hit Enter to accept the default for any of the others.

| # | Parameter | Required? | Default |
|---|-----------|-----------|---------|
| 1 | **Dataset source** — URL to a landing page, or local path to a directory of metadata files | Yes | — |
| 2 | **Checklist file** — path to the checklist CSV | No | `CHECKLIST.csv` in the current directory |
| 3 | **Template file** — path to the output structure template JSON | No | `example_outputs/FAIR4AI_eval_neon_beetles_2026-08-21_120000.json` in the current directory |
| 4 | **Output directory** — the workspace root where run folders are created | No | Current working directory |
| 5 | **Output filename** | No | `FAIR4AI_eval_<short_name>_<YYYY-MM-DD_HHMMSS>.json` |
| 6 | **Rerun existing evaluation?** — re-evaluate a dataset already evaluated in the Output directory | No | No |

Each run creates a **run folder** `<output dir>/fair4ai_run_<TS>/` holding `retrieved_metadata/` (cached metadata) and `evaluation_results/` (the timestamped evaluation JSON). Before evaluating, the agent scans the Output directory for a prior `FAIR4AI_eval_<short_name>_*.json`; if one exists and Rerun is **No**, it **prints a warning, notes the skip in `evaluate_progress.md`, and stops** without re-evaluating. It also looks for already-downloaded metadata before fetching anew.

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
One object per checklist item, in checklist-CSV order. Each response contains:

```json
{
  "item": "File Integrity Verification",
  "requirement_definition": "The dataset implements checksums for file integrity verification.",
  "status": "does not meet",
  "evidence": "No mention of checksums in any metadata source reviewed.",
  "notes": "",
  "recommendation": "Generate and publish SHA-256 checksums for all released data files...",
  "fair_category": "Reusable",
  "ai_fair_criteria": "Provenance | Structural"
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
- `fair4ai_scores` — reproducible scores in **0–1** (1 = "most FAIR4AI") in two nested blocks computed by the `fair4ai-scoring` skill (`scripts/compute_fair4ai_scores.py`):
  - `traditional_fair` — Findable, Accessible, Interoperable, Reusable + an `overall`, with per-dimension `details` counts (from each item's `fair_category`)
  - `ai_fair` — ML-ready, AI-ready for task, Traceable, CARE compliance + an `overall`, with per-facet `components` counts (from each item's `ai_fair_criteria`)

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
Rerun existing evaluation?: [Enter]
```
Output file: `fair4ai_run_2026-04-30_142530/evaluation_results/FAIR4AI_eval_neon_beetles_2026-04-30_142530.json`

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

To re-evaluate the same dataset after making improvements, answer **Yes** to *Rerun existing evaluation?* (or say "rerun"/"re-evaluate"). Each re-run gets its own timestamped file and run folder, so you can compare outputs to track progress; re-runs reuse the cached metadata rather than re-fetching.

---

## Batch mode — evaluating many datasets

To evaluate a whole list of datasets in one run, use the companion skill:

```
/batch-evaluate-datasets
```

**Input** — point it at a dataset list in any of three formats:
- a **CSV** (ideally `email,name,dataset_short_name,url,notes`, but it maps other column layouts too),
- a **Markdown** file (a table with a URL column, `- Name — URL` bullets, or `[Name](URL)` links),
- a **plain-text** file (one `name, url` or bare URL per line).

The skill normalizes whatever you give it into a standard `batch_datasets_<date>.csv` (kept as an
artifact), then asks which model the per-dataset sub-agents should use — default **Claude Haiku 4.5**
(`claude-haiku-4-5-20251001`). See `example_inputs/` for ready-to-use `.csv` and `.md` samples.

**What it does** — as a **coordinator**, it launches one sub-agent per dataset in parallel (waves of
5), each running `/evaluate-dataset` non-interactively, validates every result (89 responses, valid
statuses, non-null scores), then **hands off to the `summarize-outputs` skill** for the compiled CSV,
figure, and report.

**Output** — one self-contained, resumable **run folder** (`batch_run_<date>/`) containing: the
normalized CSV, a `retrieved_metadata/<short_name>/` cache per dataset, every per-dataset
`evaluation_results/FAIR4AI_eval_<short_name>_<YYYY-MM-DD_HHMMSS>.json`, a `confidence_map.json`, a
compiled `fair4ai_scores_summary_<date>.csv`, a summary figure
(`fair4ai_score_distributions_<date>.{png,pdf,svg}`), a narrative `FAIR4AI_summary_report_<date>.md`,
and a `batch_evaluate_progress.md` tracker. Re-invoking the skill on an existing run folder
**resumes** — only pending/failed datasets are re-run. Timestamped filenames mean re-runs never
collide, and `summarize-outputs` keeps only the newest run of each dataset by default.

> The summary figure needs `numpy` + `matplotlib` (`pip install -r scripts/requirements-viz.txt`).
> If they're missing, the figure is skipped and the CSV + report are still produced.

---

## Summarizing on its own — `/summarize-outputs`

You can also summarize **any directory of evaluation JSONs** (a batch run folder's
`evaluation_results/`, or a folder of single-run outputs) without re-evaluating:

```
/summarize-outputs
```

It compiles a scores CSV, builds the summary figure (graceful skip if numpy/matplotlib are absent),
and authors the narrative report. By default it **dedups reruns** — keeping only the newest run of
each dataset and noting the older ones it ignored — or pass dedup mode `all` to include every run.
The dataset list is derived from the JSONs, so a source CSV is optional.

---

## Updating the checklist or template

- **New checklist items**: add rows to the checklist CSV following the existing column structure. `build_response_scaffold.py` reads the CSV fresh each run, so new rows flow into the scaffold (and the rating guide) automatically.
- **New output fields**: edit `scripts/build_response_scaffold.py` (`RESPONSE_FIELDS` and the field-fill logic), which owns the `responses[]` schema, and keep `scripts/merge_ratings.py`/`compute_fair4ai_scores.py` and `tests/test_scaffold_and_merge.py` in sync. The template JSON is now just a human-readable structural reference.
- **Changing defaults**: update the checklist filename or template filename in `.claude/skills/evaluate-dataset/SKILL.md` under the "Gather parameters" step.

---

## Files involved

| File | Role |
|------|------|
| `.claude/skills/retrieve-metadata/SKILL.md` | The `/retrieve-metadata` skill (fetch + cache metadata into `retrieved_metadata/<short_name>/`) |
| `.claude/skills/evaluate-dataset/SKILL.md` | The `/evaluate-dataset` skill and evaluation workflow (run folder, skip/rerun, downloaded-first; also supports Batch / non-interactive mode) |
| `.claude/skills/fair4ai-scoring/SKILL.md` | The `/fair4ai-scoring` skill (deterministic 0–1 scoring) |
| `.claude/skills/batch-evaluate-datasets/SKILL.md` | The `/batch-evaluate-datasets` coordinator skill (parallel per-dataset evals → hands off to `summarize-outputs`) |
| `.claude/skills/summarize-outputs/SKILL.md` | The `/summarize-outputs` skill (compile any results dir → CSV + figure + report, dedups reruns) |
| `scripts/build_response_scaffold.py` | Builds the scaffold JSON (89 responses, verbatim fields pre-filled) and emits the compact per-section rating guide; run at Step 3 of an evaluation |
| `scripts/merge_ratings.py` | Merges a section's `{item, status, evidence, notes, recommendation}` ratings into the scaffold in place (one call per section → incremental, resumable writes); pass `--checklist CHECKLIST.csv` to enforce the "Never NA" guard (mandatory items can't be rated `N/A`) |
| `scripts/compute_fair4ai_scores.py` | Scoring tool the fair4ai-scoring skill runs |
| `scripts/compile_fair4ai_results.py` | Compiles a directory of evaluation JSONs into a scores CSV + aggregates (source CSV optional; dedups reruns) |
| `scripts/make_fair4ai_figure.py` | Renders the summary figure (needs numpy + matplotlib) |
| `example_inputs/` | Sample `.csv` / `.md` batch input lists |
| `RATING_RUBRIC.md` | Authority for the `meets / partial / does not meet / N/A` rating |
| `CLAUDE.md` | Project context auto-loaded by Claude Code each session |
| `CHECKLIST.csv` | Default checklist source |
| `example_outputs/FAIR4AI_eval_neon_beetles_2026-08-21_120000.json` | Default output template (current schema) |
| `CHECKLIST_OVERVIEW.md` | Human-readable checklist summary (reference) |
