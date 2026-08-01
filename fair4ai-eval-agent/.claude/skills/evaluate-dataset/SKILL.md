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
   Default: `example_outputs/FAIR4AI_eval_NEON_beetles_DP1.10022.001_2026-07-26.json` in the current working directory (the current-schema example, with `fair4ai_category` on every response and script-computed 0–1 `fair4ai_scores`).

4. **Output directory** *(optional)* — Directory where the evaluation JSON will be saved.
   Default: current working directory.

5. **Output filename** *(optional)* — Filename for the evaluation JSON.
   Default: auto-generated as `FAIR4AI_eval_<dataset-name>_<YYYY-MM-DD>.json`.
---

After the user responds, confirm the resolved parameters (substituting defaults for any blanks) before proceeding.

## Batch / non-interactive mode

When you are invoked by a **batch coordinator** (the `batch-evaluate-datasets` skill) rather than
directly by a person, you will be given all parameters up front in your prompt. In that case:

- **Skip Step 1's interactive prompt entirely.** Do not ask the user anything. Treat the supplied
  values (dataset source, checklist file, template file, output directory, output filename, and
  evaluator name/email) as the resolved parameters and proceed directly to Step 2.
- Run Steps 2–6 exactly as written, including computing scores with `compute_fair4ai_scores.py`.
- **Interpreter rule:** run all Python via the `python` command exactly as written. Do **not**
  call `python3`, `pip`, `py -m pip`, or `python -m venv`, and never trigger any Python installer
  — the scripts are stdlib-only and need no install. If `python` is unavailable, use `py -3`,
  never `python3` (on Windows `python3` may resolve to the Microsoft Store redirector and open the
  install manager).
- **End your turn by returning the structured result** below as your final message (in addition to
  writing the JSON file) — the coordinator parses this instead of re-opening your file:

  ```json
  {
    "short_name": "<dataset_short_name>",
    "output_path": "<full path to the JSON you wrote>",
    "n_responses": 96,
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

## Step 2: Load the checklist

Read the checklist CSV file (`CHECKLIST.csv`, 96 items). Each row with a non-blank `Item` is a checklist item. Key columns:

| CSV column | Maps to JSON field / use |
|---|---|
| `Broad categories` | `section` — copy **verbatim** (the `Governance` value routes CARE scoring) |
| `Sub category` | `sub_section` |
| `Item` | basis for `question` |
| `Proposed definition` / `Note` | context to interpret the criterion |
| `Criteria: Structural/Scientific/Provenance` | copied verbatim into each response's `criteria` |
| `FAIR4AI category` | copied verbatim into each response's `fair4ai_category` |
| `Use-case scope (Condition)` | drives the **N/A** decision (see Step 4) |
| `Required (core, auto, or recommended)` | emphasis in the narrative (core gaps weigh more) |
| `Applies-at-level` | context for what "present" means (dataset / event / occurrence / media-annotation) |

Skip only rows where `Item` is blank. (This checklist has no leading-`-` rows and no `Other` category.) For the few rows with a blank `Broad categories` (some CARE/governance rows), fall back to the `Sub category` value for the `section` label. Rewrite each `Item` value as a complete, clear question for the `question` field.

## Step 3: Fetch dataset metadata

**If the user provided a URL:**
- Use WebFetch to retrieve the landing page.
- Look for `<script type="application/ld+json">` blocks (schema.org / JSON-LD).
- Try appending `/api` or common API patterns if the dataset is from a known repository (NEON, GBIF, DataONE, Zenodo, Dryad, Hugging Face, etc.).
- Retrieve any linked metadata documents (EML, DataCite XML, DarwinCore, README).
- Note all URLs successfully fetched in `session.source_files`.

**If the user provided a local path:**
- Read all files in the directory: JSON, XML, CSV, Markdown, text.
- Prioritize schema.org JSON-LD, EML XML, DataCite XML, then README/documentation files.
- List all files read in `session.source_files`.

If metadata retrieval is incomplete or fails for some sources, note this in the `session.evaluator.evaluation_description` and proceed with what is available.

## Step 4: Evaluate each checklist item

`RATING_RUBRIC.md` is the authority for how to choose a status — read it and apply it. For every checklist item, assess the dataset metadata and fill in six fields:

- **`status`**: one of exactly four values (rubric §2):
  - `"meets"` — the information the item asks for is clearly present and evidence-locatable in the metadata
  - `"partial"` — the information is present but incomplete, ambiguous, buried in free text, or not machine-locatable
  - `"does not meet"` — the item applies to this dataset but the information is absent or not findable (includes dangling links that do not resolve)
  - `"N/A"` — the item does not apply to this dataset (see the N/A rule below)

  **Evidence is required for `meets` and `partial`** (rubric §2). If you cannot cite concrete evidence, the correct status is `does not meet`, not `meets`.

  **N/A rule (rubric §3):** an item is `N/A` only when its `Use-case scope (Condition)` does not apply to this dataset — a **scope mismatch** (e.g. `Derived/compiled datasets` items for a primary dataset; `Human/sensitive data` items for non-sensitive data; `Experimental data` items for observational data) or a **modality mismatch** (e.g. `Text/NLP` language for an image/tabular dataset; sensor/instrument items for a dataset with no such captures). Items scoped `All use cases` are **never** N/A. The `Required` tier (`core`/`auto`/`recommended`) never triggers N/A — a missing in-scope item is `does not meet`, just lower-emphasis.

  **Blended criteria (rubric §4):** when the `Criteria: Structural/Scientific/Provenance` column lists more than one facet, rate each applicable facet and take the **lower** status.

- **`evidence`**: quote or cite specific metadata fields, field names, or values that support the status. For `"does not meet"`, state explicitly what is absent.

- **`notes`**: caveats, edge cases, or secondary observations not captured in evidence. For `"N/A"`, name the scope/modality that is absent.

- **`recommendation`**: if status is `"partial"` or `"does not meet"`, provide specific and actionable guidance — name the field, standard, or format the dataset should adopt, and briefly explain why it matters for AI/ML reuse. Leave as `""` if status is `"meets"` or `"N/A"`.

- **`fair4ai_category`**: copy the item's `FAIR4AI category` value **verbatim** from the checklist (a pipe-separated subset of `Findable | Accessible | Interoperable | Reusable | AI-ready`, or blank for context-only items). Drives the **Traditional FAIR** assessment in Step 5 — do not omit it.

- **`criteria`**: copy the item's `Criteria: Structural/Scientific/Provenance` value **verbatim** from the checklist (one or more of `Structural | Scientific | Provenance`, e.g. `Structural/Scientific`, or blank). Drives the **AI-FAIR** assessment in Step 5. Combined with the `section` value (which must be the Broad category verbatim, so a `Governance` section routes to CARE scoring), this is what makes AI-readiness measurable — do not omit it.

When evidence is ambiguous, assign `"partial"` rather than guessing in either direction, and explain the ambiguity in `notes`.

## Step 5: Build the output JSON

Construct the full evaluation document using the structure below. Do not omit any top-level key. Use `null` for unknown values in the `session` block rather than leaving fields empty.

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
      "section": "<Broad categories value from CSV>",
      "sub_section": "<Sub category value from CSV>",
      "question": "<item text rewritten as a complete question>",
      "status": "<meets | partial | does not meet | N/A>",
      "evidence": "<specific evidence from metadata>",
      "notes": "<additional context or blank>",
      "recommendation": "<actionable guidance, or blank string>",
      "fair4ai_category": "<FAIR4AI category value copied verbatim from CSV, e.g. 'Accessible | Reusable', or blank>",
      "criteria": "<Criteria value copied verbatim from CSV, e.g. 'Structural/Scientific', or blank>"
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

Do **not** estimate the FAIR4AI scores yourself. Instead, build `responses[]` (each with its `status` and `fair4ai_category`) and the rest of the `summary`, write the file (Step 6), then invoke the **`fair4ai-scoring`** skill:

```bash
python scripts/compute_fair4ai_scores.py <output.json>
```

The skill computes `summary.fair4ai_scores` deterministically as **two assessments** (per item: `meets → 1`, `partial → 0.5`, `does not meet → 0`, `N/A`/blank → excluded; any all-N/A dimension/facet is `null` and omitted from means). All scores are **0–1, where 1 is "most FAIR4AI"**:

- **Traditional FAIR** — from `fair4ai_category` (the `AI-ready` token is ignored): per-dimension mean for `findable`/`accessible`/`interoperable`/`reusable`, then `overall` = equal-weight mean of the non-null dimensions.
- **AI-FAIR** — from `criteria` + the Governance section: facet base scores `structural`/`scientific`/`provenance` (`criteria`) and `governance` (section); then `ml_ready` = structural, `ai_ready_for_task` = mean(structural, scientific), `traceable` = mean(provenance, structural), `care_compliance` = governance, and `overall` = equal-weight mean of the four.

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

(Two checklist columns drive the two assessments. `FAIR4AI category` → Traditional FAIR: Findable = PID/DOI, rich metadata, keywords, landing page; Accessible = download/API/open formats/license/access conditions; Interoperable = standards (EML, DwC, schema.org, ENVO), machine-readable formats, controlled vocab; Reusable = attribution, provenance, methods docs, license clarity, checksums. `Criteria` + the Governance section → AI-FAIR: Structural = machine-ingestable format/schema; Scientific = fitness for a scientific/ML task; Provenance = traceability of sources and processing; Governance = the CARE/ethical items in the Governance broad category.)

## Step 6: Write the output, compute scores, and report to the user

1. Generate the output filename: `FAIR4AI_eval_<dataset-name-sanitized>_<YYYY-MM-DD>.json` (replace spaces and special characters with underscores in the dataset name portion).
2. Write the JSON file to the specified output directory (with `fair4ai_scores` as an empty object for now).
3. Compute the scores reproducibly by invoking the **`fair4ai-scoring`** skill on the file just written:
   ```bash
   python scripts/compute_fair4ai_scores.py <output.json>
   ```
   This populates `summary.fair4ai_scores` with both assessments (Traditional FAIR + AI-FAIR, each 0–1 with per-dimension/facet `details`). Resolve any `WARNING:` it prints (e.g., a scoreable item missing its `fair4ai_category`, an unrecognized `criteria` value, or an item mapping to nothing) and re-run.
4. Report to the user:
   - Full path of the output file written
   - Total checklist items evaluated
   - Count breakdown by status (meets / partial / does not meet / N/A)
   - Both **0–1** headline scores — **Overall FAIR** and **Overall AI-FAIR** — plus the four AI-FAIR categories (ml_ready, ai_ready_for_task, traceable, care_compliance), noting they are script-computed (reproducible), not estimated. Call out the FAIR-vs-AI-FAIR gap if present.
   - Top 3 highest-priority recommendations (those for "does not meet" items first, then "partial")
