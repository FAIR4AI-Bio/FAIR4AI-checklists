---
name: retrieve-metadata
description: Retrieve a dataset's metadata from a landing-page URL or a local directory, and (by default) save it into a retrieved_metadata/<short_name>/ subfolder so evaluations can reuse it without re-fetching. Invoke as /retrieve-metadata, or whenever you need to fetch/cache dataset metadata before a FAIR4AI evaluation. Also invoked internally by the evaluate-dataset skill.
---

You retrieve the metadata for a single dataset — from a landing-page URL or a local
directory of metadata files — and, by default, **save it to disk** so a later
`evaluate-dataset` run (or a re-run) can reuse it instead of fetching again. You do
**not** rate or score anything; that is `evaluate-dataset`'s job. Your handoff is the
retrieved metadata plus a small structured result.

## Step 1: Gather parameters

When invoked directly, present this prompt and wait. When invoked by another skill
(e.g. `evaluate-dataset`), the parameters are supplied in your prompt — skip the
prompt and proceed.

---
**Retrieve Dataset Metadata — Parameters**

1. **Dataset source** *(required)* — URL to the dataset landing page, OR a local path
   to a directory containing dataset metadata files.
2. **Short name** *(optional)* — a lowercase, underscore-separated slug identifying the
   dataset. Default: derived from the dataset name or the URL's last meaningful path
   segment.
3. **Save location** *(optional)* — directory to save retrieved metadata into.
   Default: `retrieved_metadata/<short_name>/` inside the current run folder (or the
   current working directory if no run folder was given).
4. **Save metadata?** *(optional)* — Default: **Yes**. When No, return content
   in-context only and write nothing.
---

## Step 2: Retrieve the metadata

**If the dataset source is a URL:**
- Use WebFetch to retrieve the landing page.
- Look for `<script type="application/ld+json">` blocks (schema.org / JSON-LD).
- Try appending `/api` or common API patterns if the dataset is from a known
  repository (NEON, GBIF, DataONE, Zenodo, Dryad, Hugging Face, etc.).
- Retrieve any linked metadata documents (EML, DataCite XML, DarwinCore, README).
- Record every URL successfully fetched (these become `source_files`).

**If the dataset source is a local path:**
- Read all files in the directory: JSON, XML, CSV, Markdown, text.
- Prioritize schema.org JSON-LD, EML XML, DataCite XML, then README/documentation files.
- Record every file read (these become `source_files`).

If retrieval is incomplete or some sources fail, note the limitation (it feeds the
evaluator's `evaluation_description`) and proceed with what is available.

## Step 3: Save the retrieved metadata (default on)

Unless **Save metadata?** is No, write what you retrieved into the save location:

- Save each retrieved artifact with a descriptive name and its natural extension —
  schema.org JSON-LD as `*.jsonld` (or `*.json`), EML/DataCite as `*.xml`, a fetched
  landing page as `*.html`, README/text as-is.
- Also write a **`retrieval_manifest.json`** in the save location:

  ```json
  {
    "short_name": "<short_name>",
    "dataset_source": "<URL or local path>",
    "retrieved_at": "<YYYY-MM-DD_HHMMSS>",
    "source_files": ["<URL or file path>", "..."],
    "saved_files": ["<relative filename>", "..."],
    "confidence": "high | medium | low",
    "note": "<one sentence: what was retrieved and any gaps>"
  }
  ```
  Get `retrieved_at` from the shell: `date +%Y-%m-%d_%H%M%S`.

- `confidence` is your self-assessed **retrieval** confidence: `high` (rich metadata
  fully retrieved), `medium` (partial), `low` (landing page thin or retrieval largely
  failed).

**File-hygiene rule:** write **only** inside the save location. Do **not** create
helper scripts or scratch files elsewhere, and **never** write into the agent source
tree (`fair4ai-eval-agent/` — where `CHECKLIST.csv`, the skills, and `scripts/` live).
If the local-path source already *is* the save location, do not duplicate files —
just record them in the manifest.

## Step 4: Return a structured result

End by returning this object (in addition to any saved files) so the caller can
proceed without re-fetching:

```json
{
  "short_name": "<short_name>",
  "saved_dir": "<absolute save location, or null if Save metadata? was No>",
  "source_files": ["..."],
  "evaluation_method": "<one sentence describing how metadata was accessed>",
  "confidence": "high | medium | low"
}
```
