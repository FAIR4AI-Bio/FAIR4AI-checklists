---
name: batch-evaluate-datasets
description: Batch-evaluate many datasets against the FAIR4AI-Bio checklist by coordinating one sub-agent per dataset in parallel (default Claude Haiku 4.5). Reads a flexible dataset list (.txt/.csv/.md), saves all evaluation JSONs into one self-contained run folder, then compiles a scores CSV, a summary plot, and a Markdown report. Invoke as /batch-evaluate-datasets, or whenever asked to evaluate a list/CSV of datasets, run a batch, or produce a cross-dataset FAIR4AI summary.
---

You are the **coordinator** for a batch FAIR4AI-Bio evaluation. You read a list of datasets,
dispatch one sub-agent per dataset to run the single-dataset `evaluate-dataset` workflow in
**Batch / non-interactive mode**, collect and validate their outputs, then compile a scores
CSV, a summary figure, and a narrative Markdown report. Every artifact of a run lives inside
one **run folder** so a run is self-contained and resumable.

You (the coordinator) run the orchestration and author the two Markdown documents. The scoring,
compilation, and figure are done by scripts. The per-dataset evaluations are done by sub-agents.

---

## Step 1: Gather batch parameters

Present this parameter prompt and wait for the user's response. Show each on its own line with
the default stated:

---
**FAIR4AI Batch Evaluation — Parameters**

Press Enter to accept the default for any optional parameter.

1. **Dataset list** *(required)* — path to a `.txt`, `.csv`, or `.md` file listing datasets and
   their URLs (any layout; see Step 4).
2. **Run folder** *(optional)* — directory that will hold every artifact of this run.
   Default: `batch_run_<YYYY-MM-DD>/` in the current working directory.
3. **Checklist file** *(optional)* — Default: `CHECKLIST.csv` in the current working directory.
4. **Template file** *(optional)* — Default:
   `example_outputs/FAIR4AI_eval_NEON_beetles_DP1.10022.001_2026-07-26.json`.
5. **Run date** *(optional)* — Default: today, `YYYY-MM-DD`.
6. **Wave size** *(optional)* — how many sub-agents to run concurrently. Default: `5`.
7. **Report title / subtitle** *(optional)* — Defaults derived from the dataset count and date.
---

After the user responds, confirm the resolved parameters (substituting defaults for blanks)
before proceeding.

## Step 2: Resume check

Look at the resolved run folder:

- **If it already exists and contains `batch_evaluate_progress.md`**, read that file. Report which
  datasets are already ✅ complete (a valid evaluation JSON exists for them — verify per the
  Validation checklist) and which are ⏳ pending / ⚠️ / ⛔. You will **resume**: only pending and
  failed datasets get (re)launched in Step 6. Do not re-evaluate completed ones.
- **Otherwise**, create the run folder and an `evaluation_results/` subfolder inside it.

## Step 3: Confirm the sub-agent model

State the default sub-agent model — **Claude Haiku 4.5** (`claude-haiku-4-5-20251001`) — and ask
whether to use it or specify a different model. Record the chosen model; it appears in the report
and figure footnote. If the user wants to pick a current model id, consult the `claude-api` skill.

(The coordinator itself keeps running as the session model; only the per-dataset evaluation
sub-agents run as the chosen model.)

## Step 4: Parse and normalize the dataset list

Read the input file and extract, for each dataset, at least a **URL** and ideally a **name**,
regardless of the file's layout:

- **CSV** — if it already has the columns `email,name,dataset_short_name,url,notes`, use them
  directly. Otherwise map whatever columns exist (a `url`/`link` column, a `name`/`title` column,
  an `email` column) onto that schema.
- **Markdown** — pull datasets from tables (a URL column/cell), bullet lists (`- Name — URL`),
  or inline links `[Name](URL)`. Ignore prose.
- **Plain text** — one dataset per non-empty line: accept `name, url`, `name<TAB>url`, or a bare
  URL on its own line.

For every parsed dataset:
- Derive a **`dataset_short_name`** if one isn't given — a lowercase, underscore-separated slug
  from the name (or from the URL's last meaningful path segment). Ensure short_names are **unique**
  (append `_2`, `_3`, … on collision).
- Carry `email`, `name`, and `notes` when present; leave blank otherwise.

Write the normalized list to **`<run folder>/batch_datasets_<DATE>.csv`** with exactly the header
`email,name,dataset_short_name,url,notes` (UTF-8). This normalized CSV is the artifact every
downstream step reads — write it even when the input was already a CSV.

**Validate:** every row has a non-empty `url` and a unique `dataset_short_name`. Report the row
count and any input lines/rows that could not be parsed into a URL. Show the user the normalized
list and **confirm before launching** any sub-agents.

## Step 5: Preflight

- Run the scorer selftest and require it to pass before spending model calls:
  ```bash
  python scripts/compute_fair4ai_scores.py --selftest
  ```
- Seed (or refresh, on resume) **`<run folder>/batch_evaluate_progress.md`** — see the template at
  the end of this file. It records the resolved params, chosen model, run folder, and one row per
  dataset with status ⏳ pending (or the already-known status on resume).

## Step 6: Launch sub-agents in waves

Launch the datasets that still need evaluating (skip any already ✅ complete) in **waves of the
configured size** (default 5) — send the wave's sub-agent calls in a single message so they run
concurrently, wait for the wave to finish, then start the next wave. This avoids rate-limit and
WebFetch throttling on large lists.

Each sub-agent uses the **chosen model** and gets a prompt that:

1. States: *"Operate in **Batch / non-interactive mode** per the `evaluate-dataset` skill
   (`.claude/skills/evaluate-dataset/SKILL.md`). Do not ask the user anything."*
2. Supplies the resolved evaluate-dataset parameters for this dataset:
   - **Dataset source** = the row's `url`
   - **Checklist file** = the batch checklist file
   - **Template file** = the batch template file
   - **Output directory** = `<run folder>/evaluation_results/`
   - **Output filename** = `FAIR4AI_eval_<short_name>_<DATE>.json`
   - **Evaluator name/email** = the row's `name` / `email` (or the batch defaults)
3. Requires the sub-agent to end by (a) writing the JSON, (b) running
   `python scripts/compute_fair4ai_scores.py <that file>` to populate scores, and (c) returning
   the **Structured result contract** (below) as its final message.

After each wave completes, update `batch_evaluate_progress.md` (✅ / ⚠️ / ⛔ per dataset) so
progress survives a lost session.

> **Stopped-but-complete:** if a sub-agent is stopped or errors mid-run but has **already written a
> complete, valid 96-item evaluation JSON** (verify per the Validation checklist), keep that file and
> mark the dataset ✅ — do not needlessly re-run it. This happened in real reference runs.

## Step 7: Collect and validate every result

For each expected `dataset_short_name`, confirm its JSON exists in `<run folder>/evaluation_results/`
and passes the **Validation checklist**:

- exactly **96** entries in `responses[]`;
- every `status` is one of `meets | partial | does not meet | N/A`;
- `summary.fair4ai_scores.overall` is present and **non-null**.

Re-run the scorer on each file to guarantee reproducible scores and **zero `WARNING:`**:
```bash
python scripts/compute_fair4ai_scores.py <run folder>/evaluation_results/FAIR4AI_eval_<short>_<DATE>.json
```
Resolve any warning (e.g. a scoreable item missing its `fair4ai_category`) and re-run. **Policy:**
if a dataset fails validation, relaunch its sub-agent once; if it still fails, mark it ⛔ in the
progress doc and exclude it from the compile step (note it in the report's coverage line).

## Step 8: Write the confidence map

From the sub-agents' structured returns, assemble
**`<run folder>/confidence_map.json`** = `{ "<short_name>": "high|medium|low", ... }` for every
successfully evaluated dataset.

## Step 9: Compile the scores CSV

```bash
python scripts/compile_fair4ai_results.py \
  --results-dir "<run folder>/evaluation_results" \
  --source-csv  "<run folder>/batch_datasets_<DATE>.csv" \
  --confidence-map "<run folder>/confidence_map.json" \
  --out-csv "<run folder>/fair4ai_scores_summary_<DATE>.csv" \
  --date <DATE>
```
Capture the printed `AGG:{...}` line — it carries `n_total`, per-dimension `dim_means`,
`overall_mean`, the `missing` list, and `by_confidence` groupings you will cite in the report.

## Step 10: Build the summary figure (optional / graceful)

```bash
python scripts/make_fair4ai_figure.py \
  --in-csv "<run folder>/fair4ai_scores_summary_<DATE>.csv" \
  --out-base "<run folder>/fair4ai_score_distributions_<DATE>" \
  --model "<chosen model label>" --date <DATE>
```
This needs `numpy` + `matplotlib`. If the script exits non-zero with an import error, report
*"figure skipped — install `scripts/requirements-viz.txt`"* and **continue** (the CSV and report
are still produced). Pass `--title` / `--subtitle` if the user supplied custom text.

## Step 11: Author the narrative summary report

Write **`<run folder>/FAIR4AI_summary_report_<DATE>.md`**, mirroring the structure and tone of the
reference report (`example_outputs/` and prior runs). Include:

- **Header** — date, checklist (96 items), evaluation model (the chosen sub-agent model),
  coordinator/aggregation model, scoring method (one line), retrieval method, and a **coverage** line
  (n evaluated of n listed; note any ⛔ excluded datasets).
- **Scores at a glance** — a table of all datasets with the six 0–1 scores, **sorted by overall
  desc**, plus a final **Mean (n=…)** row (use `dim_means`/`overall_mean` from the AGG line).
- **Status breakdown** — per-dataset meets / partial / does not meet / N/A counts (from the CSV).
- **Cross-dataset patterns** — the strongest and weakest dimensions, the recurring AI-ready gaps,
  and any notable outliers. Anchor on the thesis: *FAIR ≠ AI-ready*.
- **Per-dataset summaries** — a short paragraph + top gaps/recommendations per dataset.
- **Caveats** — explicitly note that ratings were produced by the chosen sub-agent model, that this
  is a **metadata-only** evaluation, and flag low-confidence datasets.
- **Artifacts** — a table linking the normalized CSV, scores CSV, figure, each JSON, and the
  progress doc.

Then mark the run ✅ complete in `batch_evaluate_progress.md`.

## Step 12: Report to the user

- The **run folder** path and a listing of its contents.
- **n evaluated / n failed**.
- **Mean overall** score and the per-dimension means, noting they are script-computed (reproducible).
- Paths to the normalized CSV, scores CSV, figure, and summary report.
- The top 3–5 cross-dataset gaps.

---

## Structured result contract

Every evaluation sub-agent must return, as its final message, a compact result the coordinator can
parse without re-opening each file — a JSON object with these fields:

```json
{
  "short_name": "neon_beetles",
  "output_path": "<run folder>/evaluation_results/FAIR4AI_eval_neon_beetles_2026-07-30.json",
  "n_responses": 96,
  "meets": 45, "partial": 18, "does_not_meet": 16, "na": 17,
  "overall": 0.733,
  "confidence": "high",
  "one_line_note": "NEON API metadata retrieved in full; strong FAIR, weak AI-ready."
}
```

`confidence` is the sub-agent's self-assessed **retrieval confidence** — how complete the metadata it
could actually fetch was: `high` (rich, fully retrieved), `medium` (partial), `low` (landing page
thin or retrieval largely failed; scores are provisional).

## Validation checklist (Step 7 gate)

A dataset's evaluation JSON is **valid** only if all hold:
- [ ] the file exists at the expected path;
- [ ] `responses[]` has exactly **96** entries;
- [ ] every response `status` ∈ `{meets, partial, does not meet, N/A}`;
- [ ] `summary.fair4ai_scores.overall` exists and is non-null;
- [ ] re-running `compute_fair4ai_scores.py` on it prints **no `WARNING:`**.

## `batch_evaluate_progress.md` template (resumable tracker)

```markdown
# FAIR4AI Batch Evaluation — Progress Tracker

**Run folder:** <run folder>
**Input list:** <dataset list path>  →  normalized to `batch_datasets_<DATE>.csv`
**Run date:** <DATE>
**Evaluation model:** <chosen model>  ·  **Coordinator:** <session model>
**Checklist:** <checklist file> (96 items)  ·  **Wave size:** <n>

Status legend: ⏳ pending · ✅ complete · ⚠️ needs attention · ⛔ failed

| # | short_name | url | status | overall | confidence | json_file |
|---|------------|-----|--------|---------|------------|-----------|
| 1 | ...        | ... | ⏳     | —       | —          | —         |

## Run log
- <DATE> — scaffolded run folder, normalized list (<n> datasets), scorer selftest PASS.
- <DATE> — launched wave 1 (<short_names>).
- ...
```

Keep this table and log current after every wave and after the compile/figure/report steps, so a
lost session can resume by reading it.
