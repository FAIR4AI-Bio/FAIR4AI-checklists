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
