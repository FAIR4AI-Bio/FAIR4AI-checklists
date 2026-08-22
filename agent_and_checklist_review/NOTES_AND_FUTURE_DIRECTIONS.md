# FAIR4AI-Bio — Notes & Future Directions

*A running log of ideas, identified gaps, and design tensions that are **out of
scope for the current checklist draft** but worth revisiting. Distinct from
`gap_analysis_results.md` (actionable R1–R13) and `PROGRESS.md` (build/iteration
tracking).*

**Started:** 2026-07-24 · **Maintainer:** Eric Sokol

---

## FD-1 — Controlled vocabulary for intended ML tasks: a gap to *enable*, not *enforce*

### The design decision
The checklist is an **evaluation instrument**, not a metadata template. Each item
should describe an aspect of a target dataset that a person or agent can assess as
**meets / partial / does not meet / N/A**. It must be **broadly applicable**
across the ecology/environmental data landscape (NEON, EDI, LTER, GBIF, iNaturalist,
NatureServe, DataONE, etc.).

Because of this, we decided **not to require datasets to declare intended ML tasks
from a controlled vocabulary** (nor bias/risk/limitation types from fixed enums).
Doing so would describe a *future* state of the field, not the current one, and would
make the instrument non-portable across repositories. Related consequence: the
`Controlled vocabulary / enumerated values` and `Applies-at-level` columns added in
v20260723 are candidates for removal — the enumerations belong in the *answer* space
(the rating rubric), not in the metadata template.

### The gap we identified
Controlled, machine-readable declaration of **intended ML tasks** (and, more broadly,
structured intended-use / bias / limitation metadata) **is regularly done only in the
ML-native hub ecosystem** — and is essentially **absent from the ecology/environmental
data ecosystem** our datasets come from.

**Where it IS done:**
- **Hugging Face Hub** — dataset-card YAML carries `task_categories` and finer-grained
  `task_ids`, drawn from an **enforced controlled vocabulary** (the same taxonomy that
  powers the Hub's "Tasks" filter: `image-classification`, `object-detection`,
  `audio-classification`, `token-classification`, …), with an `other:` escape hatch.
  BUT: optional, inconsistently populated, and concentrated in purpose-built ML corpora
  (TreeOfLife-200M, BIOSCAN-5M, iNat21) — rarely on NEON/EDI/GBIF datasets.
- **OpenML** — the most rigorous operationalization of "task-ready": a *task* is a
  first-class object = dataset + target attribute + estimation procedure (e.g. 10-fold
  CV) + evaluation measure + fixed splits. BUT: only tabular
  classification/regression/clustering/learning-curve benchmarking.
- **Papers with Code** — historically the richest task ontology + leaderboards, but
  archived/sunset (~2025); treat as a reference taxonomy, not a live standard.

**Where it is NOT done:**
- **Croissant (core)** — no controlled ML-task vocabulary; describes *structure*
  (`RecordSet`/`Field`/`FileSet`, `cr:conformsTo`), not intended tasks.
- **Croissant-RAI extension** — adds `rai:`-prefixed intended-use / bias / limitation
  / data-collection properties (and **NeurIPS 2026 now requires RAI metadata**), but
  these are largely **narrative / free-text**, not enumerated task lists. Notable: even
  the ML-focused standard treats "intended use" as prose.
- **Schema.org / DataCite / EML** — no ML-task vocabulary (`sc:educationalUse` is a
  poor fit; see the "Is task ready" row note in the checklist).

### Future direction (the opportunity)
There is a real opening for FAIR4AI-Bio to help **define and seed a lightweight,
community-adoptable convention for declaring intended ML tasks / recommended use in
ecology & environmental data** — so these datasets can become AI-FAIR without
depending on ML-native hubs. Possible paths to explore:
1. **Adopt/align with the HF task taxonomy** as an *optional reference vocabulary*
   ("when present, does the declared task come from a recognized taxonomy?"),
   extended with ecology-relevant tasks (species distribution modeling, occupancy
   modeling, bioacoustic recognition, phenology/forecasting, camera-trap detection).
2. **Contribute an ecology profile to Croissant-RAI** — map recommended-use /
   out-of-scope / bias / limitation to `rai:` properties, proposing an
   ecology-specific controlled vocabulary as an extension rather than free text.
3. **Borrow OpenML's "task = data + target + eval + splits" rigor** for the subset of
   ecology datasets that are genuinely benchmark-ready (e.g. labeled image corpora),
   without imposing it on observational/occurrence data.
4. **Publish the checklist's rating rubric itself** as the interim standard: a way to
   *assess* AI-readiness today that also signals to publishers what structured fields
   would raise their score tomorrow — creating a gentle on-ramp toward richer,
   machine-actionable metadata.

**Stance:** enable and incentivize, don't enforce. The near-term checklist evaluates
whether a dataset *communicates* its suitable/unsuitable uses at all; the long-term
ambition is to help the ecology community converge on a controlled, machine-readable
way to do so.

### Sources
- Hugging Face — Dataset Cards & metadata: https://huggingface.co/docs/hub/datasets-cards
- Croissant-RAI Specification (MLCommons): https://docs.mlcommons.org/croissant/docs/croissant-rai-spec.html
- Croissant-RAI paper: https://arxiv.org/html/2407.16883v1
- NeurIPS 2026 RAI metadata requirement: https://blog.neurips.cc/2026/05/04/responsible-ai-metadata-requirements-for-the-evaluations-and-datasets-track-neurips-2026/
- OpenML — tasks: https://docs.openml.org/examples/30_extended/tasks_tutorial/
- OpenML — basic concepts: https://github.com/openml/OpenML/wiki/Basic-Concepts



--- 
---

# Notes on aligning checklist format with other similar efforts (8/19/2026)

/plan The current iteration of the checklist is more of ***data dictionary definitions*** (it defines the entities/fields), whereas a checklist needs an ***evaluative criterion*** (it tests whether the dataset satisfies specific standards).

make a plan to update the checklist to better align with how established FAIR and AI-Readiness frameworks handle this. Specifically, use the information in the "Item" and "Proposed definition" columns to create three new columns at the beginning of the .csv. The new columns should be "Label", "Criterion", and "Evaluation guidance". All content in the columns should be sentence case. Use the guidance below on how to populate these three new columns from the existing data in the spreadsheet.  

---

### How Established FAIR & AI-Readiness Frameworks Handle This

#### 1. RDA FAIR Data Maturity Model (RDA FDMM)

The Research Data Alliance standardizes indicators by pairing a **concise label** with an **evaluative declarative statement**:

* **Indicator Label:** `RDA-R1.2-01M` (Provenance metadata)
* **Indicator Criterion:** *"Metadata includes information on the lineage and provenance of the data."*
* **Evaluation Guidance:** Specifies that compliance requires identifying data sources, processing history, and contributors.

#### 2. ESIP AI-Ready Environmental Data Checklist

The Earth Science Information Partners (ESIP) data readiness framework uses **question-based or condition-based criteria** specifically tailored for training pipelines:

* **Item Label:** `Data Lineage & Provenance`
* **Criterion/Question:** *"Is the provenance of the dataset tracked and documented, including source sensor/model and processing pipelines?"*
* **Scoring:** Yes / Partial / No / NA.

#### 3. FAIRplus / F-UJI Automated Metrics

FAIRplus and FAIRsFAIR separate the **Item Name** (human scannable) from the **Requirement Rule** and the **Maturity Rubric** (how to score):

* **Item:** `Funding Reference`
* **Requirement:** *"Dataset metadata explicitly specifies funding bodies and grant identifiers using persistent identifiers or structured text."*

---

### Recommended Structure for FAIR4AI-Bio

For a 96-item checklist evaluated by human reviewers, the most effective standard is a **Declarative Requirement Pattern**.

* **Item Label:** A short, scannable noun phrase (2–4 words).
* **Definition / Requirement:** A single declarative assertion stating what the dataset metadata or payload must contain.
* **Scoring Rubric (Internal or Tooltip):** What constitutes *Meets*, *Partial*, and *Does not meet*.

---

### Examples Across Different Dimensions of FAIR4AI-Bio

| Item Label | Definition / Requirement Statement | Meets | Partial | Does Not Meet | NA |
| --- | --- | --- | --- | --- | --- |
| **Funder Information** | Dataset metadata identifies funding organizations and associated award or grant identifiers. | Funder name and grant/award ID (or ROR/Crossref PID) are explicitly documented. | Funder name is mentioned in unstructured text without award ID or PID. | No funding or financial sponsor information is documented. | Dataset was produced without external funding or grants. |
| **Taxonomic Harmonization** | Biological entities are mapped to a standardized taxonomic authority (e.g., GBIF Backbone, ITIS, NCBI). | Valid scientific names and standard taxon keys/URIs are supplied for all records. | Scientific names are provided but contain uncurated typos, lack taxon IDs, or mix authorities. | Taxonomic names are informal, missing, or inconsistent with no authority mapping. | Dataset contains non-organismal environmental observations. |
| **Label Quality & Annotation** | Supervised target labels include class definitions, quality metrics, and annotation protocols. | Machine-readable label ontology, class balance statistics, and validation protocols are provided. | Class labels are present, but documentation lacks bounding/segmentation guidelines or QA stats. | Raw observations provided without annotation definitions or ground-truth documentation. | Dataset intended strictly for unsupervised pre-training or uncurated raster feeds. |
| **Spatial-Temporal Resolution** | Metadata explicitly specifies spatial coordinate reference systems (CRS), bounding box, and temporal sampling frequency. | Standardized CRS (e.g., EPSG:4326), spatial precision, and ISO 8601 timestamps are present across all records. | Spatial/temporal bounds exist in descriptive text but are not standardized or machine-actionable. | Georeferences or timestamps are missing, ambiguous, or lacking datum/CRS. | Data have no physical spatiotemporal attribute. |

---

### Rules of Thumb for Drafting the Remaining Items

1. **Avoid purely naming the concept:** Instead of `"Data format"`, use `"Standardized Data Formats"`.
2. **Start definitions with active verbs/conditions:** Use phrasing such as:
* *"Dataset metadata specifies..."*
* *"Data files adhere to..."*
* *"Labels are mapped to..."*
* *"Pipeline dependencies and environment specifications are provided for..."*


3. **Clarify the line between `Meets` and `Partial`:**
* **Meets:** Fully structured, standardized, and machine-actionable.
* **Partial:** Present in human-readable or unstructured text (e.g., embedded in a PDF paper or freeform README), but missing standard vocabularies or identifiers.
* **Does not meet:** Absent, ambiguous, or proprietary/inaccessible.
* **NA:** The specific constraint does not logically apply to the dataset type.

Update the progress.md document to document this plan to update the checklist, and the tasks that need to be tracked.


Notes from Eric 8/21/2026 - I iterated with Gemini and edited the checklist by hand. I did the following
1. I reviewed all items in the checklist personally
2. Marked items that overlapped in content - iterated with Gemini to either consolidate those items or refine their definitions and requirements to be orthogonal
3. Updated the categorizations based on the new requirement definitions
4. reordered the items to be more logical to a human reading the checklist, with high level overview items at the top of the list. 

These intermediate versions of the checklist are stored in /agent_and_checklist_review folder (this folder) with timestamps

