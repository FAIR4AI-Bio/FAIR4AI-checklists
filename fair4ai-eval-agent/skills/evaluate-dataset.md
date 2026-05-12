---
description: Evaluate a dataset for AI-readiness in biodiversity/ecology using the FAIR4AI-Bio checklist. Produces a structured JSON evaluation report.
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
   Default: `example_outputs/FAIR4AI_eval_NEON_beetles_DP1.10022.001_2026-01-25.json` in the current working directory.

4. **Output directory** *(optional)* — Directory where the evaluation JSON will be saved.
   Default: current working directory.

5. **Output filename** *(optional)* — Filename for the evaluation JSON.
   Default: auto-generated as `FAIR4AI_eval_<dataset-name>_<YYYY-MM-DD>.json`.
---

After the user responds, confirm the resolved parameters (substituting defaults for any blanks) before proceeding.

## Step 2: Load the checklist

Read the checklist CSV file. Each non-blank row is a checklist item. Key columns:

| CSV column | Maps to JSON field |
|---|---|
| `Broad categories` | `section` |
| `sub category` | `sub_section` |
| `items` | basis for `question` |
| `Proposed definition` / `note` | context to interpret the criterion |

Skip rows where `items` is blank, starts with `-`, or where `Broad categories` is `Other`. Rewrite each `items` value as a complete, clear question for the `question` field.

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

For every checklist item, assess the dataset metadata and fill in four fields:

- **`status`**: one of exactly four values:
  - `"meets"` — criterion is clearly and fully satisfied by the metadata
  - `"partial"` — criterion is addressed but incompletely or only implicitly
  - `"does not meet"` — criterion is not addressed at all, or actively absent
  - `"N/A"` — criterion is not applicable to this dataset type (e.g., derived-dataset questions for a primary dataset)

- **`evidence`**: quote or cite specific metadata fields, field names, or values that support the status. For `"does not meet"`, state explicitly what is absent.

- **`notes`**: caveats, edge cases, or secondary observations not captured in evidence.

- **`recommendation`**: if status is `"partial"` or `"does not meet"`, provide specific and actionable guidance — name the field, standard, or format the dataset should adopt, and briefly explain why it matters for AI/ML reuse. Leave as `""` if status is `"meets"` or `"N/A"`.

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
      "sub_section": "<sub category value from CSV>",
      "question": "<item text rewritten as a complete question>",
      "status": "<meets | partial | does not meet | N/A>",
      "evidence": "<specific evidence from metadata>",
      "notes": "<additional context or blank>",
      "recommendation": "<actionable guidance, or blank string>"
    }
  ],
  "summary": {
    "strengths": ["<notable strength>", "..."],
    "gaps": ["<notable gap>", "..."],
    "overall_assessment": "<2-3 sentence narrative summary>",
    "fair4ai_scores": {
      "findable": "<X/10 — one-line rationale>",
      "accessible": "<X/10 — one-line rationale>",
      "interoperable": "<X/10 — one-line rationale>",
      "reusable": "<X/10 — one-line rationale>",
      "ai_ready": "<X/10 — one-line rationale>"
    }
  }
}
```

Score each FAIR4AI dimension out of 10 using this guidance:
- **Findable**: PID/DOI, rich metadata, keywords, landing page
- **Accessible**: download, API, open formats, clear license, access conditions documented
- **Interoperable**: use of standards (EML, DwC, schema.org, ENVO, etc.), machine-readable formats, linked controlled vocabularies
- **Reusable**: attribution, provenance, methods documentation, license clarity, checksums
- **AI-ready**: annotation provenance, split guidance, bias/limitations documented, class distributions, missing-data semantics, AI/ML usage history, issue reporting

## Step 6: Write the output and report to the user

1. Generate the output filename: `FAIR4AI_eval_<dataset-name-sanitized>_<YYYY-MM-DD>.json` (replace spaces and special characters with underscores in the dataset name portion).
2. Write the JSON file to the specified output directory.
3. Report to the user:
   - Full path of the output file written
   - Total checklist items evaluated
   - Count breakdown by status (meets / partial / does not meet / N/A)
   - FAIR4AI scores (one line each)
   - Top 3 highest-priority recommendations (those for "does not meet" items first, then "partial")
