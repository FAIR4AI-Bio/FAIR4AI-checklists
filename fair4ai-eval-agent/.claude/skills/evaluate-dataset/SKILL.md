---
name: evaluate-dataset
description: Evaluate a dataset for AI-readiness in biodiversity/ecology using the FAIR4AI-Bio checklist. Produces a structured JSON evaluation report. Invoke as /evaluate-dataset, or whenever asked to score/assess a dataset's FAIR4AI or AI-readiness.
---

You are evaluating a dataset for AI-readiness in biodiversity, ecology, and environmental science using the FAIR4AI-Bio checklist.

## Step 1: Gather parameters

Before doing any evaluation, present the following parameter prompt to the user and wait for their response. Show each parameter on its own line with the default clearly stated:

---
**FAIR4AI Dataset Evaluation — Parameters**

Please provide the following. Press Enter to accept the default for any optional parameter.

1. **Dataset source** *(required)* — URL to the dataset landing page, OR a local path to a directory containing dataset metadata files.

2. **Checklist file** *(optional)* — Path to the checklist CSV.
   Default: `CHECKLIST.csv` in the current working directory.

3. **Template file** *(optional)* — Path to the output template JSON to use as structural reference.
   Default: `example_outputs/FAIR4AI_eval_neon_beetles_2026-08-21_120000.json` in the current working directory (the current-schema example, with `fair_category` on every response and script-computed 0–1 `fair4ai_scores`).

4. **Output directory** *(optional)* — Workspace directory where this run's run folder will be created. Skip/reuse checks scan across the run folders it contains.
   Default: current working directory.

5. **Output filename** *(optional)* — Filename for the evaluation JSON.
   Default: auto-generated as `FAIR4AI_eval_<short_name>_<YYYY-MM-DD_HHMMSS>.json` (timestamp to the second, so re-runs never collide).

6. **Rerun existing evaluation?** *(optional)* — Default: **No**. When No and a prior evaluation of this dataset already exists in the Output directory, the run is **skipped** (see Step 2). Set to Yes — or phrase the request as "rerun"/"re-evaluate" — to force a fresh evaluation.
---

After the user responds, confirm the resolved parameters (substituting defaults for any blanks) before proceeding.

## Batch / non-interactive mode

When you are invoked by a **batch coordinator** (the `batch-evaluate-datasets` skill) rather than
directly by a person, you will be given all parameters up front in your prompt. In that case:

- **Skip Step 1's interactive prompt entirely.** Do not ask the user anything. Treat the supplied
  values (dataset source, checklist file, template file, output directory, output filename, and
  evaluator name/email) as the resolved parameters and proceed directly to Step 3.
- **The coordinator already created the run folder.** Do **not** create a new run folder and do
  **not** run Step 2's skip check (the coordinator owns resume/skip via its progress tracker).
  Save any retrieved metadata into `<run folder>/retrieved_metadata/<short_name>/` (the sibling of
  the output directory the coordinator gave you) and write the evaluation JSON into the supplied
  output directory. Then run Steps 3–7 exactly as written, including computing scores with
  `compute_fair4ai_scores.py`.
- **File-hygiene rule (critical in batch mode):** use the **absolute paths** the coordinator gives
  you — the checklist and the **output directory**. Do **not** rely on the current working
  directory: never read `CHECKLIST.csv` by a bare relative name, and never `cd` into the agent
  source tree. Your only writes are **inside the run folder**: retrieved metadata under
  `retrieved_metadata/<short_name>/`, the **evaluation JSON** in the supplied output directory, and
  the small per-section **ratings/session/summary batch files** you feed to the helper scripts
  (keep those under `<output dir>/_ratings/`). You **may invoke** the committed helper scripts in
  `scripts/` by absolute path — `build_response_scaffold.py`, `merge_ratings.py`, and
  `compute_fair4ai_scores.py` — that is how the JSON is produced. You may **not author your own**
  `.py` scripts, create renamed/duplicate evaluation JSONs or scratch notes, or **ever** write into
  the agent source tree (`fair4ai-eval-agent/` — where `CHECKLIST.csv`, the skills, and `scripts/`
  live).
- **Interpreter rule:** run all Python via the `python` command exactly as written. Do **not**
  call `python3`, `pip`, `py -m pip`, or `python -m venv`, and never trigger any Python installer
  — the scripts are stdlib-only and need no install. If `python` is unavailable, use `py -3`,
  never `python3` (on Windows `python3` may resolve to the Microsoft Store redirector and open the
  install manager).
- **End your turn by returning the structured result** below as your final message (in addition to
  producing the JSON file via Steps 3–7) — the coordinator parses this instead of re-opening your file:

  ```json
  {
    "short_name": "<dataset_short_name>",
    "output_path": "<full path to the JSON you wrote>",
    "n_responses": 89,
    "meets": <int>, "partial": <int>, "does_not_meet": <int>, "na": <int>,
    "overall_fair": <summary.fair4ai_scores.traditional_fair.overall>,
    "overall_ai_fair": <summary.fair4ai_scores.ai_fair.overall>,
    "confidence": "high | medium | low",
    "one_line_note": "<one sentence: what metadata you retrieved and the headline finding>"
  }
  ```

  `confidence` is **your self-assessed retrieval confidence** — how complete the metadata you could
  actually fetch was: `high` (rich metadata fully retrieved), `medium` (partial retrieval), `low`
  (landing page thin or retrieval largely failed; treat scores as provisional). Note any retrieval
  limitation in `session.evaluator.evaluation_description` as usual.

## Step 2: Establish the run folder and check for a prior evaluation

*(Interactive mode only. In Batch / non-interactive mode the coordinator has already
done this — skip straight to Step 3.)*

1. Derive a **`short_name`** — a lowercase, underscore-separated slug from the dataset
   name or the URL's last meaningful path segment.
2. Get a run timestamp from the shell: `date +%Y-%m-%d_%H%M%S` → call it `<TS>`.
3. **Skip check:** search the **Output directory** recursively for any existing
   `FAIR4AI_eval_<short_name>_*.json` (e.g. `ls`/glob under prior `fair4ai_run_*`
   folders). If one or more exist **and Rerun is No**:
   - **Print a warning** to the user naming the existing file(s), e.g.
     *"⚠️ <short_name> was already evaluated (found: …). Skipping — pass Rerun=Yes to
     re-evaluate."*
   - **Append a skip note** to `<Output directory>/evaluate_progress.md` (create it if
     absent; see the log format below).
   - **Stop.** Do not create a run folder or a new evaluation.
   If no prior evaluation exists, or **Rerun is Yes**, continue.
4. Create the run folder `<Output directory>/fair4ai_run_<TS>/` with two subfolders:
   `retrieved_metadata/` and `evaluation_results/`. This run's evaluation JSON goes in
   `evaluation_results/`; retrieved metadata goes in `retrieved_metadata/<short_name>/`.

`evaluate_progress.md` log format (one line per invocation, newest appended):

```markdown
# FAIR4AI Evaluation — Progress Log (Output directory: <path>)

- <TS> — <short_name> — evaluated → fair4ai_run_<TS>/evaluation_results/FAIR4AI_eval_<short_name>_<TS>.json (reused cached metadata: yes/no)
- <TS> — <short_name> — SKIPPED (already evaluated: <existing file(s)>); pass Rerun=Yes to re-evaluate
```

## Step 3: Build the response scaffold and load the rating guide

**Do not read the whole `CHECKLIST.csv` into context or hand-write the 89 response objects.**
Instead run the blessed helper `build_response_scaffold.py`. It (a) writes a **scaffold**
evaluation JSON with all 89 responses pre-filled — `item`, `requirement_definition`,
`fair_category`, and `ai_fair_criteria` copied **verbatim** from the checklist, **`status`
defaulting to `meets`** (the exception-based norm), and `evidence`/`notes`/`recommendation`
empty — and (b) prints a **compact, per-section rating guide** (requirement + per-item N/A
condition) that you rate from:

```bash
python scripts/build_response_scaffold.py \
  --checklist <checklist path> \
  --out <run folder>/evaluation_results/<output filename> \
  --emit-guide
```

Read the guide from the command's **stdout**. It groups all 89 items into their **9 `Broad
categories` sections** and, per item, shows the `Requirement`, the item's **`N/A when`** condition,
the `AI FAIR Criteria`, the `FAIR category`, and any `Note`. Also read **`RATING_RUBRIC.md`** once —
its §4 facet guidance (Structural / Scientific / Provenance / Governance) is your **authoritative
philosophy** for deciding meets / partial / does not meet. This guide is your rating surface — you
do **not** re-read the raw CSV, and you **never** edit the four verbatim fields (the scaffold owns
them, which keeps them exactly correct). Because every item already defaults to `meets`, your job in
Steps 4–5 is only to **override the exceptions** — the items that are `partial`, `does not meet`, or
`N/A` — by producing their `status`, `evidence`, `notes`, and `recommendation`.

## Step 4: Obtain the dataset metadata (look for downloaded data first)

Get the metadata to evaluate against, preferring already-available data over a fresh
fetch — in this order:

1. **Local source** — if the **Dataset source** is a local directory path, read its
   files directly (JSON, XML, CSV, Markdown, text; prioritize schema.org JSON-LD, EML
   XML, DataCite XML, then README/docs). No fetch needed.
2. **Reuse cached metadata** — otherwise, search the **Output directory** (including
   prior `fair4ai_run_*/retrieved_metadata/<short_name>/` folders) for previously saved
   metadata for this dataset. If found, **reuse it** (read those files and its
   `retrieval_manifest.json`) instead of re-fetching. Note in
   `session.evaluator.evaluation_description` that cached metadata was reused.
3. **Retrieve fresh** — only if neither of the above yields metadata, invoke the
   **`retrieve-metadata`** skill with: Dataset source = the source; Short name =
   `<short_name>`; Save location = `<run folder>/retrieved_metadata/<short_name>/`;
   Save metadata? = Yes. Use its returned `source_files`, `evaluation_method`, and
   `confidence`.

Record every URL/file used in `session.source_files` and describe how metadata was
accessed in `session.evaluation_method`. If metadata is incomplete or retrieval failed
for some sources, note this in `session.evaluator.evaluation_description` and proceed
with what is available.

**Read the metadata once and keep it in your working context for the whole evaluation.** All 9
sections in Step 5 are rated against the same metadata — do **not** re-read the raw files per
section. Reading it once and reusing it across sections is what keeps token cost flat as the
number of rated items grows.

## Step 5: Rate the checklist, one section at a time, merging as you go

Work the guide **section by section** (the 9 `Broad categories` groups). The scaffold already scores
every item `meets`, so this step is **exception-based**: for each section you review every item, but
you only **emit ratings for the items that deviate** — those that are `partial`, `does not meet`, or
`N/A`. Everything you leave alone stays `meets`. After reviewing each section, **write that section's
deviations to the scaffold immediately** with `merge_ratings.py`, then move to the next section. This
makes progress visible, keeps writes small, and makes the run resumable. Do **not** wait and write
once at the end.

**You must review all 9 sections.** Because unreviewed items silently stay `meets` (= full credit),
skipping a section would inflate the score. Keep an explicit tally as you go and confirm at the end
of the step that every one of the 9 sections was reviewed (see the coverage check below).

For each section:

1. Review **every** item in the section against its `Requirement` and the `RATING_RUBRIC.md` §4 facet
   guidance. Decide which items fall short or are out of scope. For each such item, set its `status`
   and write `evidence` / `notes` / `recommendation` (guidance below). Items that clearly meet their
   requirement need **no entry** — they keep the default. You do **not** touch `item`,
   `requirement_definition`, `fair_category`, or `ai_fair_criteria` (the scaffold holds them verbatim).
2. Emit that section's **deviations only** as a small JSON array to a batch file under
   `<output dir>/_ratings/<section>.json`, each entry `{"item", "status", "evidence", "notes",
   "recommendation"}` (the `item` must match the checklist item name **exactly** — `merge_ratings.py`
   rejects unknown names, which catches drift). If a section has no deviations, record that in your
   tally and skip the merge for it.
3. Merge it (always pass `--checklist` so the "Never NA" guard is active):
   ```bash
   python scripts/merge_ratings.py \
     --scaffold <run folder>/evaluation_results/<output filename> \
     --ratings <output dir>/_ratings/<section>.json \
     --checklist CHECKLIST.csv
   ```
   With `--checklist`, the merge **rejects** an `N/A` rating on any item whose `N/A when` cell reads
   "Never NA …" (mandatory for all datasets) — the enforcement behind the N/A rule below. It also
   prints how many items now carry a non-`meets` status so you can track deviations. **Resume:** if
   a run is interrupted, the presence of a `_ratings/<section>.json` file marks a section as already
   reviewed; resume with the sections that have no batch file yet.

**Section-coverage check (required before Step 6).** Confirm you reviewed all 9 sections — e.g. a
short tally like `General Information: reviewed, 3 deviations; Data Access: reviewed, 0 deviations; …`
for every section. Do not proceed until each of the 9 sections has been reviewed; a section left
unreviewed would leave its items silently at the `meets` default.

**`RATING_RUBRIC.md` is your authoritative rating framework.** Judge each item against its
`Requirement` (what it asks the dataset to disclose) and use the rubric's §4 facet guidance
(Structural / Scientific / Provenance / Governance — what "present / incomplete / absent" concretely
look like) to decide whether a missing or weak element is `partial` or `does not meet`. The only
item-specific cell is `Scoring: NA` (shown as `N/A when` in the guide), which governs the `N/A`
decision. Fill in the fields below:

- **`status`**: one of exactly four values (rubric §2 gives the general meaning; rubric §4 gives the per-facet detail):
  - `"meets"` — the information the item asks for is clearly present and evidence-locatable in the metadata (this is the **default**; leave the item alone rather than emitting a redundant `meets` entry)
  - `"partial"` — the information is present but incomplete, ambiguous, buried in free text, or not machine-locatable (rubric §4)
  - `"does not meet"` — the item applies but the information is absent or not findable (includes dangling links that do not resolve)
  - `"N/A"` — the condition in the item's `N/A when` (`Scoring: NA`) cell holds for this dataset (see the N/A rule below)

  **Evidence is required for `partial`** (rubric §2) — cite what is present. For `does not meet`, state what is absent. (Items that `meet` keep the default and need no entry.)

  **N/A rule (rubric §3):** an item is `N/A` only when the condition in its **`N/A when` (`Scoring: NA`)** cell applies to this dataset — typically a **scope mismatch** (e.g. derived-dataset-only items for a primary dataset; conditional-disclosure items whose condition is absent; experimental-design items for observational data) or a **modality mismatch** (e.g. language items for an image/tabular dataset; sensor/instrument or resolution items for a dataset with no such captures). Items whose `N/A when` cell reads **"Never NA …"** are never `N/A`. **A rating of `N/A` removes the item from scoring entirely — it is neither credit nor penalty — so use it whenever the item is out of scope rather than leaving it at the `meets` default (which would wrongly award full credit).**

  **Conditional-disclosure items must not be scored as gaps for a clean dataset.** Several items are phrased as conditional statements (document *when such content/restriction is present*), so a dataset that lacks the condition is `N/A` per its `Scoring: NA` cell, **never** `does not meet`:
  - *Sensitive Data Handling and Obfuscation*: a dataset with **no** PII or sensitive localities → **`N/A`** (name the absent dimension in `notes`). Rate `meets` only when such content is present *and* its handling is documented.
  - *Access Restriction Justification* / *Secure Access Procedure*: a fully open dataset with **no** access restriction → **`N/A`**. Rate `meets` when access is restricted *and* the conditions are documented.
  Scoring one of these `does not meet` for a clean, open dataset is a **polarity error** — it would wrongly drag down Accessible/Reusable for exactly the datasets that have nothing to disclose.

  **Blended criteria (rubric §4):** when the `AI FAIR Criteria: Structural | Scientific | Provenance | Governance` column lists more than one facet, rate each applicable facet and take the **lower** status.

- **`evidence`**: quote or cite specific metadata fields, field names, or values that support the status. For `"does not meet"`, state explicitly what is absent.

- **`notes`**: caveats, edge cases, or secondary observations not captured in evidence. For `"N/A"`, you **must** name in `notes` why the item is out of scope (the specific scope/modality that is absent, per its `N/A when` condition).

- **`recommendation`**: for `"partial"` or `"does not meet"` you **must** provide a concise, actionable recommendation — name the field, standard, or format the dataset should adopt, and briefly explain why it matters for AI/ML reuse. Leave as `""` for `"meets"` and `"N/A"`.

(You do **not** write `item`, `requirement_definition`, `fair_category`, or `ai_fair_criteria` — the scaffold already carries them verbatim from the checklist. `fair_category` drives Traditional FAIR and `ai_fair_criteria` drives AI-FAIR in Step 6, but they are fixed; your ratings are what feed the scores. The guide still shows each item's `AI FAIR Criteria` so you can apply the blended-criteria "take the lower" rule.)

When evidence is ambiguous, assign `"partial"` rather than guessing in either direction, and explain the ambiguity in `notes`.

## Step 6: Fill the `session` block and `summary` narrative

The scaffold `build_response_scaffold.py` wrote in Step 3 **already has the full document shape** —
the `session`/`responses`/`summary` keys, all 89 `responses[]` objects (verbatim fields + the ratings
Step 5 merged in), and `summary.fair4ai_scores: {}`. You are **not** rebuilding it. This step fills
the two remaining hand-authored pieces: the `session` block (dataset identity + evaluator + method)
and the `summary` narrative (`strengths`, `gaps`, `overall_assessment`). Leave `fair4ai_scores` empty
— Step 7 computes it.

Set both by handing `merge_ratings.py` small JSON files (do **not** re-Write the whole document):

```bash
python scripts/merge_ratings.py \
  --scaffold <run folder>/evaluation_results/<output filename> \
  --session-json <output dir>/_ratings/session.json \
  --summary-json <output dir>/_ratings/summary.json
```

`--session-json` replaces the top-level `session` block; `--summary-json` sets
`summary.strengths`/`gaps`/`overall_assessment` (it never touches `fair4ai_scores`). Use `null` for
unknown values in `session` rather than leaving fields empty. The two files carry exactly these
shapes (the same structure the finished document uses below):

```json
// session.json
{
  "evaluation_date": "<today YYYY-MM-DD>",
  "ai_model": "Claude (Anthropic)",
  "evaluation_method": "<one sentence describing how metadata was accessed>",
  "source_files": ["<URL or file path 1>", "..."],
  "dataset": {
    "title": "<dataset title>",
    "product_id": "<product or accession ID, or null>",
    "repository_url": "<repository root URL, or null>",
    "landing_page_url": "<dataset landing page URL, or null>",
    "citation": "<full preferred citation, or null>"
  },
  "evaluator": {
    "name": "<user-provided name, or 'Automated FAIR4AI Evaluation'>",
    "affiliation": "<user affiliation, or null>",
    "email": "<user email, or null>",
    "relationship_to_dataset": "<Data Provider/Producer | Processor | Host | Data User/Developer | Catalog Curator>",
    "evaluation_purpose": "<publishing for others | open-ended use | use in a specific project>",
    "evaluation_description": "<brief description of what sources were used and any retrieval limitations>"
  }
}
```

```json
// summary.json
{
  "strengths": ["<notable strength>", "..."],
  "gaps": ["<notable gap>", "..."],
  "overall_assessment": "<2-3 sentence narrative summary>"
}
```

For reference, the finished document the scaffold + these merges + Step 7's scoring produce has this
structure (do not omit any top-level key):

```json
{
  "session": {
    "evaluation_date": "<today YYYY-MM-DD>",
    "ai_model": "Claude (Anthropic)",
    "evaluation_method": "<one sentence describing how metadata was accessed>",
    "source_files": ["<URL or file path 1>", "..."],
    "dataset": {
      "title": "<dataset title>",
      "product_id": "<product or accession ID, or null>",
      "repository_url": "<repository root URL, or null>",
      "landing_page_url": "<dataset landing page URL, or null>",
      "citation": "<full preferred citation, or null>"
    },
    "evaluator": {
      "name": "<user-provided name, or 'Automated FAIR4AI Evaluation'>",
      "affiliation": "<user affiliation, or null>",
      "email": "<user email, or null>",
      "relationship_to_dataset": "<Data Provider/Producer | Processor | Host | Data User/Developer | Catalog Curator>",
      "evaluation_purpose": "<publishing for others | open-ended use | use in a specific project>",
      "evaluation_description": "<brief description of what sources were used and any retrieval limitations>"
    }
  },
  "responses": [
    {
      "item": "<Item value copied verbatim from CSV>",
      "requirement_definition": "<Requirement Definition value copied verbatim from CSV>",
      "status": "<meets | partial | does not meet | N/A>",
      "evidence": "<specific evidence from metadata>",
      "notes": "<additional context or blank>",
      "recommendation": "<actionable guidance, or blank string>",
      "fair_category": "<FAIR category value copied verbatim from CSV, e.g. 'Accessible | Reusable', or blank>",
      "ai_fair_criteria": "<AI FAIR Criteria value copied verbatim from CSV, e.g. 'Structural | Scientific', or blank>"
    }
  ],
  "summary": {
    "strengths": ["<notable strength>", "..."],
    "gaps": ["<notable gap>", "..."],
    "overall_assessment": "<2-3 sentence narrative summary>",
    "fair4ai_scores": "<computed by the fair4ai-scoring skill in this step — leave as an empty object {} until then>"
  }
}
```

Do **not** estimate the FAIR4AI scores yourself. `responses[]` were filled per section in Step 5 and
the `session`/`summary` narrative in Step 6; in Step 7 you compute `summary.fair4ai_scores`
deterministically by invoking the **`fair4ai-scoring`** skill:

```bash
python scripts/compute_fair4ai_scores.py <output.json>
```

The skill computes `summary.fair4ai_scores` deterministically as **two assessments** (per item: `meets → 1`, `partial → 0.5`, `does not meet → 0`, `N/A`/blank → excluded; any all-N/A dimension/facet is `null` and omitted from means). All scores are **0–1, where 1 is "most FAIR4AI"**:

- **Traditional FAIR** — from `fair_category`: per-dimension mean for `findable`/`accessible`/`interoperable`/`reusable`, then `overall` = equal-weight mean of the non-null dimensions.
- **AI-FAIR** — from `ai_fair_criteria`: facet base scores `structural`/`scientific`/`provenance` and `governance`, all read from `ai_fair_criteria` (an item counts toward `governance` if its `ai_fair_criteria` includes `Governance`; for older evaluations the scorer also falls back to a `Governance` `section`); then `ml_ready` = structural, `ai_ready_for_task` = mean(structural, scientific), `traceable` = mean(provenance, structural), `care_compliance` = governance, and `overall` = equal-weight mean of the four.

It writes this block back into the file:

```json
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
```

(Two checklist columns drive the two assessments. `FAIR category` → Traditional FAIR: Findable = PID/DOI, rich metadata, keywords, landing page; Accessible = download/API/open formats/license/access conditions; Interoperable = standards (EML, DwC, schema.org, ENVO), machine-readable formats, controlled vocab; Reusable = attribution, provenance, methods docs, license clarity, checksums. `AI FAIR Criteria` → AI-FAIR: Structural = machine-ingestable format/schema; Scientific = fitness for a scientific/ML task; Provenance = traceability of sources and processing; Governance = the CARE/ethical items carrying the `Governance` criteria token.)

## Step 7: Compute scores and report to the user

1. The evaluation file already exists — it is the scaffold `build_response_scaffold.py` wrote in
   Step 3 at `<run folder>/evaluation_results/<output filename>` (`FAIR4AI_eval_<short_name>_<TS>.json`,
   or the custom Output filename if one was supplied), progressively filled by the Step 5 rating
   merges and the Step 6 session/summary merge, with `fair4ai_scores` still `{}`. This is the **only**
   evaluation file — the sole extra writes are the small batch files under `<output dir>/_ratings/`;
   do not emit a generator script, an intermediate/renamed JSON, or any other scratch file, and never
   write into the agent source tree (`fair4ai-eval-agent/`). (Retrieved metadata already lives under
   `retrieved_metadata/<short_name>/` from Step 4.)
2. Confirm the file is complete before scoring: all 89 `responses[]` are present with a valid
   `status` (they default to `meets`, so what matters is the **section-coverage check** from Step 5 —
   every one of the 9 sections was reviewed and its deviations merged), every `partial`/`does not
   meet` item carries a `recommendation`, every `N/A` item explains itself in `notes`, and `session` /
   `summary` are filled from Step 6. Re-run `merge_ratings.py` on any section whose deviations were not
   yet merged.
3. Compute the scores reproducibly by invoking the **`fair4ai-scoring`** skill on the file:
   ```bash
   python scripts/compute_fair4ai_scores.py <output.json>
   ```
   This populates `summary.fair4ai_scores` with both assessments (Traditional FAIR + AI-FAIR, each 0–1 with per-dimension/facet `details`). Resolve any `WARNING:` it prints (e.g., a scoreable item missing its `fair_category`, an unrecognized `criteria` value, or an item mapping to nothing) and re-run.
4. Append an **"evaluated"** line to `<Output directory>/evaluate_progress.md` (see the log format in Step 2), noting the run folder, output file, and whether cached metadata was reused. *(Interactive mode only — in Batch mode the coordinator maintains its own progress tracker.)*
5. Report to the user:
   - Full path of the output file written (and the run folder)
   - Total checklist items evaluated
   - Count breakdown by status (meets / partial / does not meet / N/A)
   - Both **0–1** headline scores — **Overall FAIR** and **Overall AI-FAIR** — plus the four AI-FAIR categories (ml_ready, ai_ready_for_task, traceable, care_compliance), noting they are script-computed (reproducible), not estimated. Call out the FAIR-vs-AI-FAIR gap if present.
   - Top 3 highest-priority recommendations (those for "does not meet" items first, then "partial")
