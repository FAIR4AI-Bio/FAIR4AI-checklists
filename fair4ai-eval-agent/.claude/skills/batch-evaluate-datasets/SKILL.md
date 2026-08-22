---
name: batch-evaluate-datasets
description: Coordinate a batch FAIR4AI-Bio evaluation of many datasets by dispatching one sub-agent per dataset in parallel (default Claude Haiku 4.5). Reads a flexible dataset list (.txt/.csv/.md), saves all evaluation JSONs into one self-contained run folder, then hands off to the summarize-outputs skill for the scores CSV, summary figure, and Markdown report. Invoke as /batch-evaluate-datasets, or whenever asked to evaluate a list/CSV of datasets or run a batch.
---

You are the **coordinator** for a batch FAIR4AI-Bio evaluation. You read a list of datasets,
dispatch one sub-agent per dataset to run the single-dataset `evaluate-dataset` workflow in
**Batch / non-interactive mode**, collect and validate their outputs, then hand off to the
**`summarize-outputs`** skill to compile the scores CSV, summary figure, and narrative report.
Every artifact of a run lives inside one **run folder** so a run is self-contained and resumable.

You (the coordinator) run the orchestration and own the progress tracker
(`batch_evaluate_progress.md`). The per-dataset evaluations are done by sub-agents; the
cross-dataset summary (scoring compilation, figure, and report) is done by `summarize-outputs`.

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
   `example_outputs/FAIR4AI_eval_neon_beetles_2026-08-03_102743.json`.
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
- **Otherwise**, create the run folder with two subfolders inside it: `evaluation_results/`
  (per-dataset JSONs) and `retrieved_metadata/` (per-dataset cached metadata).

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
  Invoke every Python call in this skill with the `python` command exactly as written —
  never `python3` (on Windows it may resolve to the Microsoft Store redirector and open the
  install manager). The scripts are stdlib-only, so no `pip`/install step is ever needed.
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
2. Supplies the resolved evaluate-dataset parameters for this dataset, **as absolute paths**:
   - **Dataset source** = the row's `url`
   - **Checklist file** = the batch checklist file (absolute path)
   - **Template file** = the batch template file (absolute path)
   - **Output directory** = `<run folder>/evaluation_results/` (absolute path)
   - **Metadata save location** = `<run folder>/retrieved_metadata/<short_name>/` (absolute path)
   - **Output filename** = `FAIR4AI_eval_<short_name>_<TS>.json`, where `<TS>` is the
     sub-agent's current timestamp to the second (`date +%Y-%m-%d_%H%M%S`) so re-runs never collide
   - **Evaluator name/email** = the row's `name` / `email` (or the batch defaults)
   - Tell the sub-agent the run folder already exists: it must **not** create a new run folder
     or run the interactive skip check — just save retrieved metadata to the Metadata save
     location and write the evaluation JSON into the Output directory.
3. Requires the sub-agent to end by (a) writing the JSON, (b) running
   `python scripts/compute_fair4ai_scores.py <that file>` to populate scores, and (c) returning
   the **Structured result contract** (below) as its final message.
4. States the **Interpreter rule**: *"Run all Python via the `python` command exactly as
   written. Do **not** call `python3`, `pip`, `py -m pip`, or `python -m venv`, and never trigger
   any Python installer — the scripts are stdlib-only and need no install. If `python` is
   unavailable, use `py -3`, never `python3`."* (On this machine `python3` resolves to the
   Microsoft Store App-Installer redirector and pops the "Python install manager".)
5. States the **File-hygiene rule**: *"Use the absolute paths given above. Do not rely on the
   current working directory, do not read `CHECKLIST.csv` by a bare relative name, and do not `cd`
   into the agent source tree. Your only writes are inside the run folder: retrieved metadata under
   the **Metadata save location** (`retrieved_metadata/<short_name>/`) and **exactly one evaluation
   JSON** into the supplied **Output directory** (`evaluation_results/`), using the Write tool
   directly (build the JSON yourself; do not author a generator script that emits it). Do **not**
   create any helper `.py` script, intermediate/renamed JSON, or scratch file, and **never** write
   into the agent source tree (`fair4ai-eval-agent/`, where `CHECKLIST.csv`, the skills, and
   `scripts/` live)."* (Real runs left stray `eval_*.py` / `*_evaluation.json` files in the agent
   repo — this rule prevents that.)

After each wave completes, update `batch_evaluate_progress.md` (✅ / ⚠️ / ⛔ per dataset) so
progress survives a lost session.

> **Stopped-but-complete:** if a sub-agent is stopped or errors mid-run but has **already written a
> complete, valid 89-item evaluation JSON** (verify per the Validation checklist), keep that file and
> mark the dataset ✅ — do not needlessly re-run it. This happened in real reference runs.

## Step 7: Collect and validate every result

For each expected `dataset_short_name`, confirm its JSON exists in `<run folder>/evaluation_results/`
and passes the **Validation checklist**:

- exactly **89** entries in `responses[]`;
- every `status` is one of `meets | partial | does not meet | N/A`;
- `summary.fair4ai_scores.traditional_fair.overall` and `.ai_fair.overall` are present and **non-null**.

Re-run the scorer on each file (use the sub-agent's returned `output_path`, i.e.
`<run folder>/evaluation_results/FAIR4AI_eval_<short>_<TS>.json`) to guarantee reproducible scores
and **zero `WARNING:`**:
```bash
python scripts/compute_fair4ai_scores.py <output_path>
```
Resolve any warning (e.g. a scoreable item missing its `fair_category`) and re-run. **Policy:**
if a dataset fails validation, relaunch its sub-agent once; if it still fails, mark it ⛔ in the
progress doc and exclude it from the summary (note it in the report's coverage line).

## Step 8: Write the confidence map

From the sub-agents' structured returns, assemble
**`<run folder>/confidence_map.json`** = `{ "<short_name>": "high|medium|low", ... }` for every
successfully evaluated dataset.

## Step 9: Summarize the outputs

Hand off the completed run folder to the **`summarize-outputs`** skill, which compiles the scores
CSV, builds the summary figure, and authors the narrative report. Invoke it with:

- **Results directory** = `<run folder>/evaluation_results`
- **Output directory** = `<run folder>`
- **Dedup mode** = `latest` (default — keeps the newest run of each dataset)
- **Source CSV** = `<run folder>/batch_datasets_<DATE>.csv`
- **Confidence map** = `<run folder>/confidence_map.json`
- **Label** = `<DATE>` (so artifacts are named `..._<DATE>.{csv,md,png}`)
- **Model label** = the chosen sub-agent model
- **Report title / subtitle** = the user's values if supplied

`summarize-outputs` writes `fair4ai_scores_summary_<DATE>.csv`,
`fair4ai_score_distributions_<DATE>.{png,pdf,svg}` (or reports "figure skipped" if numpy/matplotlib
are absent), and `FAIR4AI_summary_report_<DATE>.md` into the run folder, and returns the headline
means + top cross-dataset gaps. Any ⛔ datasets you excluded in Step 7 will surface in its
coverage line.

Then mark the run ✅ complete in `batch_evaluate_progress.md`.

## Step 10: Report to the user

- The **run folder** path and a listing of its contents.
- **n evaluated / n failed**.
- **Mean Overall FAIR** and **Mean Overall AI-FAIR** scores (and the per-dimension/per-category means,
  from `summarize-outputs`), noting they are script-computed (reproducible), and the typical
  FAIR-vs-AI-FAIR gap.
- Paths to the normalized CSV, scores CSV, figure, and summary report.
- The top 3–5 cross-dataset gaps.

---

## Structured result contract

Every evaluation sub-agent must return, as its final message, a compact result the coordinator can
parse without re-opening each file — a JSON object with these fields:

```json
{
  "short_name": "neon_beetles",
  "output_path": "<run folder>/evaluation_results/FAIR4AI_eval_neon_beetles_2026-07-30_142530.json",
  "n_responses": 89,
  "meets": 45, "partial": 18, "does_not_meet": 16, "na": 17,
  "overall_fair": 0.778, "overall_ai_fair": 0.779,
  "confidence": "high",
  "one_line_note": "NEON API metadata retrieved in full; strong FAIR, weaker scientific facet."
}
```

`confidence` is the sub-agent's self-assessed **retrieval confidence** — how complete the metadata it
could actually fetch was: `high` (rich, fully retrieved), `medium` (partial), `low` (landing page
thin or retrieval largely failed; scores are provisional).

## Validation checklist (Step 7 gate)

A dataset's evaluation JSON is **valid** only if all hold:
- [ ] the file exists at the expected path;
- [ ] `responses[]` has exactly **89** entries;
- [ ] every response `status` ∈ `{meets, partial, does not meet, N/A}`;
- [ ] every response carries a `fair_category` and an `ai_fair_criteria` (both copied verbatim from the CSV);
- [ ] `summary.fair4ai_scores.traditional_fair.overall` and `.ai_fair.overall` both exist and are non-null;
- [ ] re-running `compute_fair4ai_scores.py` on it prints **no `WARNING:`**.

## `batch_evaluate_progress.md` template (resumable tracker)

```markdown
# FAIR4AI Batch Evaluation — Progress Tracker

**Run folder:** <run folder>
**Input list:** <dataset list path>  →  normalized to `batch_datasets_<DATE>.csv`
**Run date:** <DATE>
**Evaluation model:** <chosen model>  ·  **Coordinator:** <session model>
**Checklist:** <checklist file> (89 items)  ·  **Wave size:** <n>

Status legend: ⏳ pending · ✅ complete · ⚠️ needs attention · ⛔ failed

| # | short_name | url | status | overall_fair | overall_ai_fair | confidence | json_file |
|---|------------|-----|--------|--------------|-----------------|------------|-----------|
| 1 | ...        | ... | ⏳     | —            | —               | —          | —         |

## Run log
- <DATE> — scaffolded run folder, normalized list (<n> datasets), scorer selftest PASS.
- <DATE> — launched wave 1 (<short_names>).
- ...
```

Keep this table and log current after every wave and after the compile/figure/report steps, so a
lost session can resume by reading it.
