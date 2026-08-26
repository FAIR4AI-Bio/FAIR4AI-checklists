# FAIR4AI-Bio: Gap Analysis Results

**Primary artifact:** `DRAFT AI-ready checklist – Schema Mapping_v20260722.csv` (8 sections, ~135 evaluable items)
**Framework:** Question–Data–Model (Q–D–M) Triangle
**Companion document:** `personas_and_archetypes.md`
**Agent context:** `fair4ai-eval-agent` (GitHub, branch `fair4ai-eval-agent-v2`) — an LLM agent that answers **135 form items** from dataset metadata and emits per-item `response`/`evidence`/`notes` plus a `summary` with FAIR score estimates
**Prepared:** 2026-07-23 · **Author:** Eric Sokol

---

## ⭐ Current State — updated 2026-07-26

> *Progress banner (maintained across iterations). The analysis below (§1–§7) is the
> **original 2026-07-23 baseline** against checklist v20260722/v20260723 and is kept
> verbatim for the record. The latest re-scored findings are **appended at the end** in
> **§8 — Gap Analysis Re-Run (2026-07-26)**. Read this banner for where things stand;
> read §8 for the detail; read §1–§7 for the baseline.*

**Instrument evaluated now:** `DRAFT AI-ready checklist_v20260724.csv` (96 items, 15 cols)
**+ `RATING_RUBRIC.md`** (meets / partial / does not meet / N/A + N/A rule + per-
criteria-type guidance). Framed as an **evaluation instrument, not a metadata template**.

**Headline change since baseline:** the baseline's central blocker was *"free text,
duplicates, and single-boolean flags make items unanswerable from structured evidence, so
the agent cannot score consistently."* Three of those are now substantially resolved:

- **G09 duplicates → ✅ resolved** (R1, in v20260723, preserved in v20260724).
- **G10 metadata-level not encoded → ✅ resolved** (R3 `Applies-at-level` on every row).
- **G06/G07 free-text bias/use → 🟡 mitigated for *scoring*** — the rubric makes free-text
  items consistently rateable (with required `evidence`) instead of unscorable. Structured
  enum *enforcement* was deliberately **not** pursued (design choice; see FD-1). The
  concern shifts from "the instrument can't score this" to "the dataset discloses this in
  prose, rated partial/meets" — which is the intended behavior.

**Coverage moved** (instrument-sufficiency re-score, §8.2): all three baseline 🔴 cells in
the section×archetype matrix are cleared — **A1 Data-Structure 🟡→🟢**, **A1 & A6
Guidance-&-Recommendations 🔴→🟡**, **A3 Provenance 🔴→🟡** — leaving one red cell (A1 ×
Source Data, awaiting the deferred sampling/sensor fields). In the triangle view, the last
🔴 (A6 Question vertex; A1 Model vertex) both lift to 🟡.

**Overall verdict now:** **🟡 Partial → pilot-*validated* for automated scoring.** As of
2026-07-26 the pilot has been run (see **§9**) and the *scoring-mechanism* blocker is
**retired**: the agent produces consistent, evidence-backed ratings and scores are now
**deterministic and reproducible** (a Python tool, not the agent's judgement). The remaining
insufficiency is **content coverage** for model-centric users (A1: sampling, sensor,
annotation-provenance — Phase 2 / R6–R9), not the ability to score. By archetype:
**A4/A5/A7 → 🟢**, **A2/A3/A6 → clean 🟡**, **A1 → 🟡 (up from 🔴)**.

**Done since this banner was first written** (see §9 and `PROGRESS.md` Iteration 5): the
NEON Beetles pilot ran end-to-end (**G15 closed — measured**); reproducible 0–1 scoring was
added (**R16**, a `FAIR4AI category` mapping column + `compute_fair4ai_scores.py` + a
`fair4ai-scoring` skill); and the finding that **the v2 agent already rates
meets/partial/does-not-meet/N/A with evidence** means R14's "align the form `options`" was a
non-issue (that belonged to the archived v1 form). **Still open:** (1) reclassify the
deferred P1/P2 gaps as *instrument gaps* vs *dataset-disclosure gaps* (**G14**, **R15**);
(2) pilot a second, contrasting repository to test cross-dataset consistency.

---

## 1. Executive Summary

The current FAIR4AI-Bio checklist (v20260722) is a strong foundation: eight coherent sections, most items mapped to at least one of EML, DataCite, Schema.org (SOSO), or Croissant, and an explicit four-level metadata model (dataset · sampling event · occurrence · media/annotation).

Evaluated against seven archetypes (A1–A7) drawn from the Q–D–M Triangle, the checklist is **partially sufficient**. It is closest to adequate for **data stewards (A4)** and **applied researchers/educators with modest ML needs (A2, A5, A7)**, and furthest from adequate for **model-centric users (A1, plus the agentic side of A3/B2)** and **policy/reporting users (A6)** who need machine-actionable defensibility signals.

**Overall sufficiency: 🟡 Partial** — ready for pilot, human-in-the-loop evaluation of individual datasets, but **not yet ready to drive consistent, automated AI-readiness scoring** by the `fair4ai-eval-agent` across archetypes.

The agent design sharpens *why*. Because the agent answers each of 135 items from metadata and must attach an **evidence** string, the binding constraint is no longer "is the field present?" but "**can this item be answered, from structured evidence, with a controlled-vocabulary response?**" Free-text items, single-boolean readiness flags, and un-consolidated duplicates each degrade the agent's precision and inter-run consistency.

**Seven themes account for most gaps:**
1. Free-text where **structured/enumerated** fields are needed (bias, risks, limitations, recommended/out-of-scope use).
2. Under-specified **"machine-ready" / "task-ready"** flags (single global booleans, no per-task/per-modality decomposition, no operational definition).
3. Weak **record-/event-level** modeling (label & annotation provenance, identification confidence, per-record license).
4. Sparse **sensor/instrumentation** metadata for non-tabular modalities (extension pointer only).
5. **Sampling semantics** under-specified (design type, effort, detectability, true-absence vs. missing).
6. **Derived-dataset provenance** defined but not consistently required; no license-compatibility rollup.
7. **Roundtripping** (user→provider feedback / downstream-use log) barely modeled — a stated FAIR4AI-Bio priority.
   *(Plus a cross-cutting eighth: **duplicates/redundancies** already flagged for consolidation but not yet reconciled, which injects scoring noise into the agent.)*

Thirteen prioritized recommendations (P0–P2) are in §4; a phased roadmap is in §5; the overall verdict is in §6.

---

## 2. Coverage Matrix

Rows = the eight checklist sections. Columns = the seven archetypes (A1–A7).

**Legend:** 🟢 Adequate — sufficient as drafted · 🟡 Partial — covers some but not all needs; gaps meaningful · 🔴 Missing — does not adequately support this archetype · ⚪ N/A — not primarily relevant to this archetype's core decisions.

| Checklist section | A1 Model Dev | A2 Applied Researcher | A3 Synthesis Sci | A4 Data Steward | A5 Conservation | A6 Policy/Reporting | A7 Educator/Student |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 1. General Information | 🟡 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 |
| 2. Data Structure | 🟡 | 🟢 | 🟢 | 🟢 | 🟢 | ⚪ | 🟢 |
| 3. Source Data | 🔴 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| 4. Data Processing | 🟡 | 🟡 | 🟡 | 🟢 | 🟡 | ⚪ | ⚪ |
| 5. Data Quality | 🟡 | 🟡 | 🟡 | 🟢 | 🟡 | 🟡 | 🟡 |
| 6. Guidance & Recommendations | 🔴 | 🟡 | 🟡 | 🟡 | 🟡 | 🔴 | 🟡 |
| 7. Data Access | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟢 |
| 8. Provenance | 🟡 | 🟢 | 🔴 | 🟢 | 🟢 | 🟢 | 🟢 |

**Reading the matrix.** No section is uniformly red and no archetype uniformly green. The heaviest red/yellow concentration is the **model-centric column (A1)** and the **Source Data** and **Guidance & Recommendations** rows — precisely the sections that must carry sampling semantics and use-case guidance. The cleanest column is **A4 (Data Steward)**, because the checklist was authored from a data-stewardship perspective. Sections 2 (Data Structure) and 7 (Data Access) are strongest across personas, reflecting mature Croissant/Schema.org mappings.

### 2.1 Triangle-vertex coverage

The same content folded onto Q–D–M vertices gives a complementary view:

| Archetype | Question vertex | Data vertex | Model vertex |
|---|:--:|:--:|:--:|
| A1 Model Developer | 🟡 | 🟡 | 🔴 |
| A2 Applied Researcher | 🟢 | 🟡 | 🟡 |
| A3 Synthesis Scientist | 🟡 | 🟡 | 🟡 |
| A4 Data Steward | 🟢 | 🟢 | 🟡 |
| A5 Conservation | 🟡 | 🟢 | ⚪ |
| A6 Policy/Reporting | 🔴 | 🟢 | ⚪ |
| A7 Educator/Student | 🟢 | 🟢 | 🟡 |

The **Question vertex** is weakest for policy/reporting (A6), because "does this dataset answer my policy question?" requires structured recommended-use and out-of-scope statements the checklist currently leaves as free text. The **Model vertex** is weakest for model-centric users (A1), because task-readiness is a single global flag rather than a per-task, per-modality assertion.

---

## 3. Gap Analysis

Gaps are numbered **G01–G13**. Each records affected archetypes, affected vertex, whether the fix is publisher-provided or repository-inferable, and gap type (new field / refinement / scoring). An **agent impact** note ties each gap to the `fair4ai-eval-agent` behavior.

### G01 — "Machine-ready" and "task-ready" are single booleans
- **Description.** `Is machine ready?` and `Is task ready` are flagged `auto` outcomes but are not decomposed by modality or ML task, and "machine-ready" has no operational definition (the checklist notes already flag it as ambiguous; ES: "should we make an additional field for ML use case?"). A dataset can be ready for image classification but not object detection.
- **Affected archetypes.** A1 (primary), A2, A3, B2 (agentic).
- **Vertex.** Model. · **Publisher vs. repository.** Repository-inferable (with rules). · **Type.** Refinement + scoring.
- **Agent impact.** Without an operational definition and enumerated options, the agent cannot answer consistently; the FAIR/AI-ready score becomes non-reproducible across runs.

### G02 — Sampling design and detectability are under-specified
- **Description.** Source Data captures data-source type and (via extension) sensor metadata, but lacks structured fields for sampling **effort**, **detectability**, **design type** (targeted/random/stratified), and **non-detection semantics** (true absence vs. missing data).
- **Affected archetypes.** A1, A2, A5, and any occupancy/SDM workflow.
- **Vertex.** Data → Question. · **Publisher-provided.** · **Type.** New field(s).
- **Agent impact.** Effort/detectability currently hide inside a free-text "resolution information" cell — unparseable; the agent cannot surface detection-corrected suitability.

### G03 — Annotation and label provenance are dataset-level only
- **Description.** `Labeling/re-labeling` is a dataset-level field. Model-centric users need **per-annotation** provenance: annotator (human/model/consensus), timestamp, model version if model-assisted, and confidence.
- **Affected archetypes.** A1, A3, B1 (camera-trap), D3.
- **Vertex.** Data → Model. · **Publisher-provided.** · **Type.** New field + metadata-level shift.
- **Agent impact.** The agent can only report a dataset-level yes/no; it cannot verify label trustworthiness the way M1/M2 require.

### G04 — Taxonomic-backbone metadata are informal
- **Description.** Controlled vocabulary is recommended and taxonomy is called out in the overview, but there are no dedicated fields for **backbone identifier, backbone version, resolution date, synonym-handling policy**.
- **Affected archetypes.** A1 (biodiversity foundation models), A3, A5, A6.
- **Vertex.** Data → Question. · **Publisher-provided.** · **Type.** New field.
- **Agent impact.** Backbone drift between snapshots is invisible to the agent; two "compatible" datasets may be silently mis-joined.

### G05 — Sensor / instrumentation metadata are an extension pointer only
- **Description.** `Sensor Metadata (link)` points to an external extension (`fair_drones`) but the checklist does not define the **minimum sensor fields** that must be resolvable (make, model, calibration date, sample rate, spectral bands, gain, bit depth, channels).
- **Affected archetypes.** A1 (M1, M2), A2 (Q3), B1.
- **Vertex.** Data → Model. · **Publisher-provided.** · **Type.** New (structured) fields.
- **Agent impact.** A dangling link is not evaluable evidence; the agent returns "not found" even when a linked resource exists.

### G06 — Bias, risks, and limitations are free text
- **Description.** All three are recommended, all map only to `dataset/introduction` + DataCite `description[Other]`, all unstructured. Agentic and policy users need **enumerable** bias/risk/limitation **types with severity** (geographic, temporal/seasonal, observer, class-imbalance, detectability).
- **Affected archetypes.** A1 (M3 agents), A6 (primary), A2, A5, A7.
- **Vertex.** Question + Data. · **Publisher-provided.** · **Type.** New structured fields + controlled vocabularies.
- **Agent impact.** Free-text bias is the single largest hallucination risk for the agent's "weaknesses" summary.

### G07 — Recommended-use and out-of-scope-use are free text
- **Description.** Same shape as G06. Agentic and policy users need a **structured list of tasks-in-scope and tasks-out-of-scope** mapped to a controlled vocabulary (`sc:educationalUse` is only a partial fit). No single "recommended questions this dataset can/cannot answer" field exists.
- **Affected archetypes.** A1, A5, A6 (primary), A7.
- **Vertex.** Question + Model. · **Publisher-provided.** · **Type.** New structured fields.
- **Agent impact.** The agent cannot route a dataset to a task (M3's core function) without an enumerated task scope.

### G08 — Derived-dataset provenance defined but not enforced consistently
- **Description.** Provenance models source DOIs, source producers, and source checksums, but several items are `core` **only in the Derived-dataset scope** and silent for non-derived datasets. Synthesis workflows also need a **license-compatibility rollup** and **cross-source dedup** across sources.
- **Affected archetypes.** A3 (primary), A1, A6.
- **Vertex.** Data. · **Publisher-provided; some repository-inferable.** · **Type.** New field (license-compat rollup, dedup) + policy tightening.
- **Agent impact.** For aggregates (TreeOfLife-200M-style), the agent cannot compute a redistributable-or-not verdict.

### G09 — Duplicates and redundancies pending consolidation
- **Description.** The checklist itself flags multiple duplicates in its `Keep/remove recommendation` column: Summary/Content/Abstract; annotation-scope file-format / dataset-structure / data-instances vs. their Data Structure counterparts; Unit Consistency vs. units-translated; QA/QC-completed vs. real-time-vs-QC vs. quality procedures; `/data processing steps done` appearing in both Completeness and Consistency.
- **Affected archetypes.** All (via scoring reliability); A4 primary.
- **Vertex.** Cross-cutting. · **Repository-inferable (curation task).** · **Type.** Refinement.
- **Agent impact.** Duplicate items make the same evidence answer two-to-three form questions, inflating apparent coverage and destabilizing the FAIR score. **This is prerequisite cleanup.**

### G10 — Metadata level is declared but not enforced per field
- **Description.** The overview states a good dataset should provide metadata at dataset/event/occurrence/media levels, but **no CSV column encodes the level** for each item. Model and synthesis users need to know at which level each field is expected.
- **Affected archetypes.** A1, A3, D1, D3.
- **Vertex.** Data. · **Repository (schema change) + publisher.** · **Type.** Schema refinement.
- **Agent impact.** The agent cannot tell whether "missing" means "absent at dataset level but present per-record" — a systematic false-negative source.

### G11 — Versioning, change logs, and update semantics are thin
- **Description.** Timeliness is captured, but there is no structured field for **version identifier, prior-version link, change type** (schema-breaking/additive), **download date**, or **version type** (snapshot/rolling/frozen). Forecasting (Q3) and derived synthesis (A3) both need these.
- **Affected archetypes.** A2 (Q3), A3, A1, B2.
- **Vertex.** Data → Model. · **Publisher-provided.** · **Type.** New structured fields.
- **Agent impact.** The agent cannot detect that a re-evaluated dataset changed since last scoring — breaks the iterate-and-re-score loop.

### G12 — Roundtripping / user-feedback channel not modeled
- **Description.** NOTES calls out "roundtripping" as feedback flow from users back to providers. The checklist has `Reporting Issues` (→ `sc:discussionUrl`) but no structured field for **issue-tracker URL, contribution policy, downstream-use log, or model-card linkage** (`sc:trainedOn`) back to the provider.
- **Affected archetypes.** A2 (Q3 primary), A3, D3, and all D/M personas.
- **Vertex.** Data ← Model / Data ← Question. · **Publisher-provided.** · **Type.** New field(s).
- **Agent impact.** The agent cannot record or verify that a dataset has downstream AI/ML uses — the roundtrip edge is invisible to automated scoring.

### G13 — Machine-actionable license semantics beyond SPDX
- **Description.** SPDX is captured under License, but **license compatibility across aggregated sources, per-record vs. dataset-level license, and derived-work permissions** (redistribution of trained models, of subsampled records) are not modeled.
- **Affected archetypes.** A1 (redistribution of trained weights), A3 (compat rollup), D3 (per-record).
- **Vertex.** Data → Model. · **Publisher; some repository-inferable via SPDX rules.** · **Type.** New fields + rules.
- **Agent impact.** The agent can read one SPDX id but cannot answer "can I legally train and release on this aggregate?"

### 3.1 Reconciliation with prior work
*(Per workflow Step 6; classified as Reinforced / Extended / Novel.)*

| Gap | Classification | Basis |
|---|---|---|
| G01, G07 | **Reinforced** | Echoes the Croissant `cr:conformsTo` discussion and FAIR4ML task-typing; matches prior `PERSONAS_and_GAP_ANALYSIS` gaps G1/G2/Q1. |
| G02, G04 | **Reinforced** | Echoes prior FAIR4AI-Bio workshop discussions on sampling semantics and taxonomic backbone (Q2/Q4/D4). |
| G03, G10 | **Extended** | Prior analyses noted metadata-level ambiguity (G5, M2); here it is tied to specific archetypes and to agent false-negatives. |
| G05 | **Reinforced** | Matches the `fair_drones` / sensor-extension track already recognized in the checklist. |
| G06, G08, G13 | **Extended** | The Datasheets-for-Datasets tradition covered bias/risks qualitatively; here the requirement is **structured and evidence-locatable** for the agent (D2/D3, Q3). |
| G09 | **Reinforced** | The checklist already annotates duplicates for removal; prior analysis G4 flagged the same. |
| G11, G12 | **Novel** | Versioning depth (version type, change logs) and roundtripping (downstream-use log, model-card linkage) have not previously received first-class checklist treatment; elevated here because the agent's iterate-and-re-score loop and the FAIR4AI-Bio mission both depend on them. |

*Preliminary agent results (per the ASLO/FARR-RCN presentation decks) reported that GPT-4o "had mixed success finding and interpreting metadata," with an open question of "improve agent? or metadata?" This gap analysis answers: **both**, but the highest-leverage metadata fixes are G01, G06, G07, G09, and G10 — the ones that convert free text and duplicates into evaluable, structured evidence.*

---

## 4. Prioritized Recommendations

Scored on **Impact** (# archetypes helped / 7), **Triangle** (# vertices improved / 3), **Importance** for AI/ML readiness (H/M/L), and **Effort** (H/M/L). Priority: **P0** (do now) · **P1** (next) · **P2** (later).

| # | Recommendation | Addresses | Impact | Triangle | Import. | Effort | Priority |
|---|---|---|:--:|:--:|:--:|:--:|:--:|
| R1 | Execute the `Keep/remove` column: consolidate all flagged duplicates and finalize one canonical item per concept | G09 | 7/7 | 3 | H | L | **P0** |
| R2 | Decompose `task-ready` into a **structured list of ML tasks × modality** (image/audio/tabular/sensor) with a per-task boolean; give `machine-ready` an operational definition (e.g., "passes Croissant validator against the declared task profile") | G01 | 6/7 | 2 | H | M | **P0** |
| R3 | Add an explicit **`applies-at-level`** tag (dataset/event/occurrence/media) to every checklist item | G10 | 6/7 | 3 | H | L | **P0** |
| R4 | Move **bias / risks / limitations** from free text to structured, enumerated lists with severity and a controlled vocabulary (geographic, temporal, observer, class-imbalance, detectability) | G06 | 6/7 | 2 | H | M | **P0** |
| R5 | Structure **recommended-use / out-of-scope-use** as controlled-vocabulary task lists; add a paired "recommended questions this dataset can/cannot answer" field | G07 | 5/7 | 2 | H | M | **P0** |
| R6 | Elevate **sensor/instrumentation metadata** from an extension pointer to a defined **minimum sensor block** (make, model, calibration date, sample rate/spectral bands, gain, bit depth, channels) | G05 | 4/7 | 2 | H | M | **P1** |
| R7 | Add **taxonomic-backbone** fields: identifier, version, resolution date, synonym policy | G04 | 5/7 | 2 | H | L | **P1** |
| R8 | Add structured **sampling-design** fields: design type, effort, detectability, true-absence vs. missing-data flag | G02 | 5/7 | 2 | H | M | **P1** |
| R9 | Add **record-level annotation-provenance** fields: annotator type (human/model/consensus), timestamp, model version, confidence; add a **split-strategy** enum (random / spatial-block / temporal / taxonomic-holdout / other) | G03 | 4/7 | 2 | H | H | **P1** |
| R10 | Add a structured **versioning block**: version ID, prior-version link, change type, download date, version type (snapshot/rolling/frozen) | G11 | 4/7 | 2 | M | L | **P1** |
| R11 | Add **license-compatibility rollup** + per-record license + derived-work-permission fields | G13 | 3/7 | 2 | M | M | **P2** |
| R12 | Formalize **derived-dataset provenance rules**: make source DOI + checksum + license required for any derived package; add cross-source dedup method | G08 | 3/7 | 2 | M | L | **P2** |
| R13 | Add a **roundtripping / feedback block**: issue-tracker URL, contribution policy, downstream-use log, model-card linkage (`sc:trainedOn`); promote `AI/ML Usage History` from recommended to core | G12 | 3/7 | 2 | M | L | **P2** |

**Rationale for the P0 set (R1–R5).** These five share three properties: (a) they are already latent in the checklist (duplicates flagged, ambiguity noted, structured tasks proposed); (b) they **unblock automated scoring by the `fair4ai-eval-agent` across all archetypes** — turning free text and duplicates into enumerable, evidence-bearing items; and (c) their effort is low-to-medium relative to impact. R3 in particular is a schema change that finally operationalizes the "cross-cutting design principle" the overview already commits to, and it directly removes the agent's dataset-vs-record false-negative problem.

---

## 5. Roadmap

Phased plan folding the recommendations into working-group sprints. Each phase ends with a checklist snapshot and a re-scored coverage matrix so cell transitions (🔴→🟡→🟢) are tracked against the agent's output.

### Phase 0 — Cleanup & Structural Foundations (0–2 months)
- **R1** Consolidate duplicates (Summary/Content/Abstract; Data Structure vs. annotation-scope duplicates; unit-consistency; QA/QC vs. real-time-vs-QC vs. quality procedures).
- **R3** Add `applies-at-level` tags to every item; publish a level-by-level view.
- **Deliverable:** `v1.0-clean` checklist + regenerated schema mappings + regenerated `form_ai_checklist_automated.csv` for the agent. Re-run the agent on the NEON Beetles dataset to confirm scoring stabilizes.

### Phase 1 — Machine-Actionability for AI-Readiness (2–5 months)
- **R2** Structured task-ready by task × modality + operational "machine-ready" definition.
- **R4** Structured bias / risks / limitations with controlled vocabulary + severity.
- **R5** Structured recommended-use / out-of-scope-use + recommended-questions field.
- **Deliverable:** `v1.1` with a machine-readable **"AI-readiness card"** per dataset. Pilot the agent on 3–5 datasets spanning NEON, EDI, GBIF, and a Hugging Face–hosted corpus; compare agent vs. human scoring (the project's stated evaluation loop).

### Phase 2 — Sampling & Model-Facing Semantics (5–9 months)
- **R6** Minimum sensor block (aligned with `fair_drones` / sensor extension).
- **R7** Taxonomic-backbone fields. · **R8** Sampling-design fields.
- **R9** Record-level annotation-provenance + split-strategy enum (requires R3 level-tagging).
- **Deliverable:** `v1.2` with **archetype-specific evaluation profiles** (A1, A2, A5 first).

### Phase 3 — Versioning, Licensing, Roundtripping (9–12 months)
- **R10** Versioning block. · **R11** License compatibility & derived-work permissions. · **R12** Enforced derived-dataset provenance rules. · **R13** Roundtripping / feedback block.
- **Deliverable:** `v2.0` candidate — ready for external community review and to underpin an **agentic dataset-discovery service** (persona M3 / B2 use case).

### Phase 4 — Governance & Sustainability (12+ months)
- Publish a level-tagged JSON-LD schema and Croissant profile; establish a versioning cadence for the checklist itself; stand up an issue tracker and formal contribution policy (dogfoods R13).

### Continuous
- After each sprint, re-run the agent and re-score the coverage matrix; report cell transitions at each FAIR4AI-Bio quarterly update. Circulate the persona set and ask each working-group member to nominate a real dataset mapping to one persona; use those as fixed test cases.

---

## 6. Overall Sufficiency Assessment

**Verdict: 🟡 Partial** — sufficient for pilot, human-driven evaluation of individual datasets; **insufficient for archetype-consistent, automated AI-readiness scoring** by the `fair4ai-eval-agent`.

The checklist is **strong along the Data ↔ Model structural edge** (Sections 2, 7, 8 — mature Schema.org / Croissant / DataCite / EML mappings), **weaker along the Data ↔ Question scientific edge** (Sections 3, 6), and **weakest at the Data ↔ Roundtrip governance edge** (only two recommended items today).

**By archetype:**
- **A4 Data Steward — 🟢 Near-sufficient.** Reflects data-stewardship priorities and is usable today, subject to R1 cleanup.
- **A5 Conservation, A7 Educator/Student — 🟡 Sufficient with minor extensions** (R4, R5). Both are well served by a plain-language, structured recommended-use block.
- **A2 Applied Researcher — 🟡 Sufficient** for many scientific-validity questions, but sampling design (R8) and versioning (R10) are needed for forecasting workflows (Q3).
- **A3 Synthesis Scientist — 🟡 Sufficient** for citation/provenance today, but license-compatibility rollup (R11) and enforced derived-dataset rules (R12) are needed to make outputs redistributable at scale.
- **A6 Policy/Reporting — 🟡 Sufficient** for narrative reports, insufficient for machine-readable defensibility until R4, R5, R10 land.
- **A1 AI/ML Model Developer — 🔴 Insufficient** for automated ingestion until R2, R6, R8, R9 land. **Largest gap, highest strategic importance** for FAIR4AI-Bio.

**Meta-observation.** The checklist already contains its own gap analysis in the `Duplicate of / redundancy` and `Keep/remove recommendation` columns. Acting on those alone (R1) would raise coverage across every archetype and stabilize the agent's score — it should be treated as **prerequisite work before any schema expansion.**

**Bottom line.** With the P0 set (R1–R5) in hand, the checklist moves to **🟢 for A4/A5/A7** and to a clean **🟡 for A2/A3/A6**. Reaching **🟢 for A1** requires all of Phases 1 and 2. The strategic bet — that the checklist can drive **agentic dataset discovery and evaluation** — depends most on **R2, R3, R4, R5, R9, and R13**; everything else is scaffolding. The single most important reframing from the agent design is that the checklist must evolve from *fields a human fills in* to **items an agent can answer from structured, cited evidence.**

---

## 7. Appendix: Method Notes
- Personas and archetypes are defined in the companion `personas_and_archetypes.md`.
- Coverage-matrix ratings are qualitative, assigned by mapping each archetype's **critical checklist sections** against the current checklist's field-level definitions, `Required` status, and `Use-case scope`.
- Gap IDs (G01–G13) and Recommendation IDs (R1–R13) are stable anchors for issue trackers and subsequent versions; each recommendation maps to one gap except where noted (R2→G01, R4→G06, R5→G07, R9→G03).
- Agent behavior is inferred from the `fair4ai-eval-agent` README (135-item form; per-item `response`/`evidence`/`notes`; JSON/CSV outputs; per-facet FAIR score estimates; metadata sources: Schema.org JSON-LD, NEON API, EML, Croissant, and URL-scraped landing pages).
- Prior-analysis reconciliation (§3.1) is coarse; a finer traceability matrix to FAIR4AI workshop outputs and to Croissant / FAIR4ML issues should be produced in Phase 0.

---
---

# 8. Gap Analysis Re-Run — v20260724 + `RATING_RUBRIC.md`

**Re-run date:** 2026-07-26 · **Author:** Eric Sokol (with Claude Code)
**Instrument evaluated:** `DRAFT AI-ready checklist_v20260724.csv` (96 items, 15 columns)
**+ companion `RATING_RUBRIC.md`** (level definitions, NA rule, per-criteria-type guidance)
**Baseline compared against:** §1–§7 above (v20260722/v20260723, prepared 2026-07-23)

*This section is **appended, not a replacement** — §1–§7 remain the baseline of record.
Gap IDs (G01–G13) and Recommendation IDs (R1–R13) keep their meanings from §3–§4;
new items introduced here continue the sequence (G14–G15, R14–R15).*

---

## 8.1 What changed in the instrument since the baseline

The baseline scored a **metadata-template** draft. Since then the instrument was rebuilt
(v20260723 script) and hand-reviewed (v20260724) into an **evaluation instrument**, and a
**rating rubric** was authored (2026-07-25). Net changes that affect the score:

1. **R1 executed — duplicates consolidated** (G09). One canonical item per concept;
   removes the double/triple-counting that inflated apparent coverage and destabilized the
   FAIR score.
2. **R3 executed — `Applies-at-level` on every row** (G10). Each item declares
   dataset / event / occurrence / media-annotation, so "missing" no longer conflates
   "absent at dataset level" with "present per-record."
3. **R2 structurally kept, definitionally reverted.** The row split (`Supported ML Tasks`
   + `Benchmark / Leaderboard results`) survives, so task-readiness is no longer a single
   global boolean; the per-task×modality *enum* was intentionally dropped (FD-1).
4. **R4/R5 reframed to rubric-assessed.** The enumerated-list *language* stays in the item
   definitions; the enforcement columns are gone. Items are now rated meets/partial/does-
   not-meet/N/A rather than validated against a fixed vocabulary.
5. **New: `RATING_RUBRIC.md`.** Supplies the standardized answer space (four levels), the
   **evidence requirement** for positive ratings, and the **N/A rule keyed to `Use-case
   scope`**. This is the piece that converts free-text and scope-conditional items from
   "unscorable / hallucination-prone" into "consistently rateable with a cited basis."

**Consequence for how we read the score:** the re-run measures **instrument sufficiency**
— can the checklist + rubric produce a consistent, defensible rating for each archetype's
needs? — which must be distinguished from **dataset readiness** (does a given dataset
disclose the thing). The baseline conflated the two; separating them is the main
conceptual result of this re-run (see G14).

---

## 8.2 Re-scored coverage matrix (instrument sufficiency)

Same legend as §2 (🟢 Adequate · 🟡 Partial · 🔴 Missing · ⚪ N/A). **Bold** = changed
from the baseline matrix in §2.

| Checklist section | A1 Model Dev | A2 Applied | A3 Synthesis | A4 Steward | A5 Conserv. | A6 Policy | A7 Educator |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 1. General Information | 🟡 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 |
| 2. Data Structure | **🟢** | 🟢 | 🟢 | 🟢 | 🟢 | ⚪ | 🟢 |
| 3. Source Data | 🔴 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| 4. Data Processing | 🟡 | 🟡 | 🟡 | 🟢 | 🟡 | ⚪ | ⚪ |
| 5. Data Quality | 🟡 | 🟡 | 🟡 | 🟢 | 🟡 | 🟡 | 🟡 |
| 6. Guidance & Recommendations | **🟡** | 🟡 | 🟡 | 🟡 | 🟡 | **🟡** | 🟡 |
| 7. Data Access | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟢 |
| 8. Provenance | 🟡 | 🟢 | **🟡** | 🟢 | 🟢 | 🟢 | 🟢 |

**Cell transitions and why:**
- **A1 × Data Structure 🟡→🟢** — G09 (duplicate file-format/data-instances rows) and G10
  (level ambiguity) both resolved; structure is now unambiguously level-tagged and
  de-duplicated, which is exactly what a model developer needs to ingest.
- **A1 × Guidance & Rec 🔴→🟡** — the `Supported ML Tasks` split makes task-readiness a
  *list* rather than one flag, and the rubric lets the (still free-text) use/limitation
  items be rated consistently with evidence. Capped at 🟡: no per-task×modality readiness
  and no operational "machine-ready" threshold (G01 open).
- **A6 × Guidance & Rec 🔴→🟡** — policy/reporting defensibility no longer depends on
  enum-structured use statements; the rubric provides a defensible, evidence-cited rating
  of whatever recommended-use / out-of-scope prose exists. Capped at 🟡 until versioning
  (R10) lands for auditability.
- **A3 × Provenance 🔴→🟡** — the derived-dataset provenance items (Provenance Tracking,
  Source Data Producers, citation of subsumed datasets, Source data DOI/checksums) are all
  present in v20260724, and the rubric's NA rule cleanly scopes them to derived datasets.
  Under the evaluation-instrument framing, "defined but not enforced" (the baseline's
  complaint) is no longer a defect — it is rated per dataset. Capped at 🟡 until the
  license-compatibility rollup (R11) lands.

**Result:** the three baseline 🔴 cells that were *scoring/structure* problems are cleared.
The **one remaining 🔴 — A1 × Source Data** — is a genuine *content* gap (sampling design
G02, sensor block G05); the rubric can rate the prose that exists, but the fields a model
developer needs to judge detection-corrected suitability are deferred to Phase 2 (R6, R8).

### 8.2.1 Triangle-vertex re-score

| Archetype | Question | Data | Model |
|---|:--:|:--:|:--:|
| A1 Model Developer | 🟡 | 🟡 | **🟡** |
| A2 Applied Researcher | 🟢 | 🟡 | 🟡 |
| A3 Synthesis Scientist | 🟡 | 🟡 | 🟡 |
| A4 Data Steward | 🟢 | 🟢 | 🟡 |
| A5 Conservation | 🟡 | 🟢 | ⚪ |
| A6 Policy/Reporting | **🟡** | 🟢 | ⚪ |
| A7 Educator/Student | 🟢 | 🟢 | 🟡 |

Both baseline 🔴s clear: **A1 Model 🔴→🟡** (task-readiness is now a rated list, not a lone
boolean) and **A6 Question 🔴→🟡** (recommended-use is now assessable). No vertex remains
🔴 — the instrument can now *ask and rate* something meaningful at every vertex for every
archetype; depth (not presence) is the remaining issue.

---

## 8.3 Gap status (G01–G13) against v20260724 + rubric

| Gap | Baseline | Now | Basis |
|---|:--:|:--:|---|
| G01 Machine/task-ready booleans | 🔴 | 🟡 **mitigated** | Row split (task = list) + rubric assessability. **Open:** operational "machine-ready" threshold (candidate: passes Croissant validator vs. declared profile) and per-task×modality decomposition — the latter *deliberately* deferred (FD-1). |
| G02 Sampling design / detectability | 🔴 | 🔴 **open** | R8 deferred (P1). Rubric can rate sampling prose but the structured fields (design, effort, detectability, true-absence) don't exist. |
| G03 Annotation/label provenance | 🔴 | 🔴 **open** | R9 deferred (P1). Still dataset-level only. |
| G04 Taxonomic-backbone fields | 🔴 | 🔴 **open** | R7 deferred (P1). |
| G05 Sensor/instrumentation block | 🔴 | 🔴 **open** | R6 deferred (P1). Still an extension pointer. |
| G06 Bias/risks/limitations free text | 🔴 | 🟡 **mitigated (scoring)** | Rubric makes these consistently rateable with required evidence; enum enforcement dropped by design (FD-1). Residual is a *dataset-disclosure* gap, not an instrument gap. |
| G07 Recommended/out-of-scope use free text | 🔴 | 🟡 **mitigated (scoring)** | Same treatment as G06. |
| G08 Derived-provenance not enforced | 🔴 | 🟡 **reframed** | Items present + rubric NA-scopes them to derived datasets; "enforcement" replaced by per-dataset rating. **Open:** license-compat rollup + cross-source dedup (→ R11/G13). |
| G09 Duplicates pending consolidation | 🔴 | 🟢 **resolved** | R1 executed (v20260723), preserved in v20260724. |
| G10 Metadata level not encoded | 🔴 | 🟢 **resolved** | R3 `Applies-at-level` populated on every row. |
| G11 Versioning / change semantics | 🔴 | 🔴 **open** | R10 deferred (P1/Phase 3). |
| G12 Roundtripping / feedback channel | 🔴 | 🔴 **open** | R13 deferred (P2). `Reporting Issues` item exists; downstream-use log / model-card linkage do not. |
| G13 License semantics beyond SPDX | 🔴 | 🔴 **open** | R11 deferred (P2). License + machine-readable-license items exist; compatibility rollup and per-record license do not. |

**Two resolved (G09, G10), four mitigated/reframed by the rubric (G01, G06, G07, G08),
seven still open content gaps (G02–G05, G11–G13)** — and every open one is a Phase-2/3
recommendation already tracked in `PROGRESS.md` §3, not a surprise.

---

## 8.4 New gaps surfaced by the reframing

### G14 — Instrument-gap vs. dataset-disclosure-gap are conflated *(conceptual; the main new finding)*
- **Description.** The baseline gaps mixed two different things: (a) the *instrument* lacks
  a way to ask/rate something (a real instrument gap), and (b) the *dataset* doesn't
  disclose something the instrument already asks (a dataset-readiness observation the
  rubric now handles as a *rating*, no instrument change needed). Now that the rubric
  exists, G06/G07 are mostly type (b) — the instrument asks, the rubric rates, done — while
  G02/G03/G04/G05 are genuinely type (a) — the instrument can't even ask with enough
  structure to be useful to A1.
- **Why it matters.** It re-prioritizes the roadmap: type-(a) gaps need *new rated
  criteria*; type-(b) "gaps" need *nothing further from the instrument* and should stop
  being counted against it. This is the difference between the baseline's "🔴 insufficient
  for automated scoring" and this re-run's "🟡 pilot-ready."
- **Type.** Reclassification / scoring. · **Vertex.** Cross-cutting. → **R15.**

### G15 — Rubric defined but not yet validated with the agent
- **Description.** `RATING_RUBRIC.md` specifies the four-level `options` vocabulary and the
  evidence/N/A rules, but the `fair4ai-eval-agent` form's `options` column has **not** been
  aligned to it, and **no pilot** has confirmed the agent produces consistent ratings +
  citable evidence under the rubric (esp. for the reverted free-text items it was *not*
  designed around).
- **Why it matters.** The entire "pilot-ready" upgrade in this re-run is a *prediction*
  until a run on a real dataset (NEON Beetles) confirms inter-run consistency.
- **Type.** Validation. · **Vertex.** Cross-cutting (agent-facing). → **R14.**

---

## 8.5 Recommendation status & additions

Baseline R1–R13 status is tracked in `PROGRESS.md` §3 (R1 ✅, R3 ✅, R2 🟡 partial, R4/R5
🟡 rubric-only, R6–R13 ⏳ deferred). This re-run confirms that split and adds two:

| # | Recommendation | Addresses | Priority | Notes |
|---|---|---|:--:|---|
| **R14** | Align the agent form's `options` column to the rubric's four levels; **pilot on NEON Beetles** and compare inter-run consistency + evidence quality against a human rating of the same dataset | G15 | **P0-next** | This is the immediate next action (`PROGRESS.md` §5 step 3). Validates the "pilot-ready" claim. |
| **R15** | Reclassify the deferred P1/P2 gaps as **instrument gaps** (need new rated criteria: G02–G05, G11–G13) vs. **dataset-disclosure gaps** (handled by rating, no instrument change: residual G06/G07). Fold the labels into the roadmap and the `PROGRESS.md` R-table | G14 | P1 | Low effort; sharpens what "add to the checklist" actually means under the evaluation-instrument framing. |

**No change** to the deferred recommendations' priorities: R6–R9 (Phase 2 content for A1)
remain the highest-leverage *instrument* work; R10–R13 (Phase 3) remain later. The rubric
did not remove any of them — it removed the *scoring-mechanism* objection that sat on top
of them.

---

## 8.6 Updated overall sufficiency assessment

**Verdict: 🟡 Partial — now pilot-ready for automated scoring** (baseline was 🟡 Partial —
*not* ready for automated scoring). The distinction is the point of this re-run.

- The baseline's binding constraint — *"free text, duplicates, and single-boolean flags
  make items unanswerable from structured evidence"* — is **substantially retired**:
  duplicates gone (R1/G09), level encoded (R3/G10), and free-text items now consistently
  rateable with cited evidence (rubric / G06/G07).
- The **remaining insufficiency is content coverage, not scoring capability.** A1 (model
  developer) still can't get sampling (G02), sensor (G05), or record-level annotation
  provenance (G03) from the instrument — Phase-2 work (R6–R9).

**By archetype (instrument sufficiency):**
- **A4 Steward, A5 Conservation, A7 Educator — 🟢.** Usable now.
- **A2 Applied, A3 Synthesis, A6 Policy — clean 🟡.** Scoring-ready; each needs one
  Phase-2/3 content block (sampling/versioning; license-compat; versioning-for-audit).
- **A1 Model Developer — 🟡 (up from 🔴).** Scoring mechanism no longer blocks it; the
  Source-Data content gap (the lone remaining 🔴 cell) does. Still the largest and
  highest-strategic-value remaining gap.

**Bottom line.** The checklist has crossed from *"fields a human fills in"* toward *"items
an agent can rate from cited evidence."* The rubric was the missing half of that
transition; the remaining work is **domain content for model-centric ingestion (R6–R9)**
plus a **validation pilot (R14)** to convert this re-run's predicted uplift into a measured
one.

---

## 9. Scoring + Pilot Validation (2026-07-26 — R14, R16)

*This section records the **measured** result that §8 predicted. It closes G15 and adds two
pieces of machinery — a FAIR4AI-dimension mapping column and a deterministic scoring tool.*

### 9.1 What was built (R16 — reproducible quantitative scoring)

The prior scoring was the agent's subjective `X/10 — rationale` per dimension, which is not
reproducible. It was replaced with a deterministic pipeline:

- **`FAIR4AI category` column** added to the checklist (→ `DRAFT AI-ready
  checklist_v20260726.csv`, 16 cols). Every one of the 96 items is mapped to one or more of
  the **five FAIR4AI dimensions** — Findable, Accessible, Interoperable, Reusable, AI-ready —
  pipe-separated when an item serves several (user's "allow multiple" decision). This records
  which dimension an item *counts toward*; it is **not** an enum-enforcement column (FD-1
  preserved). Dimension mention counts across the 96 items: Reusable 50, AI-ready 21,
  Findable 20, Accessible 16, Interoperable 13.
- **`scripts/compute_fair4ai_scores.py`** (agent repo, stdlib-only): `meets → 1`,
  `partial → 0.5`, `does not meet → 0`, `N/A → excluded`. Per-dimension score = mean of that
  dimension's scored items (a multi-mapped item counts in *each* listed dimension). Overall =
  **equal-weight** mean of the scored dimensions (an all-N/A dimension → `null`, omitted).
  All values 0–1 (1 = "most FAIR4AI"), rounded to 3 dp; idempotent.
- **`fair4ai-scoring` skill** wraps the tool; the `/evaluate-dataset` command now invokes it
  instead of eyeballing scores. Each response carries its `fair4ai_category` verbatim so the
  score is computed purely from the eval JSON.

### 9.2 Pilot — NEON Ground Beetles (DP1.10022.001)

Ran the full 96-item evaluation from the NEON product API metadata (the landing-page
schema.org JSON-LD is JS-rendered and was **not** retrievable, so format items were rated
conservatively — a real limitation to note for future pilots). Result:

| | Findable | Accessible | Interoperable | Reusable | **AI-ready** | **Overall** |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| **Score (0–1)** | 0.824 | 0.833 | 0.833 | 0.622 | **0.556** | **0.733** |
| scored items | 17 | 15 | 12 | 37 | 18 | — |

Status distribution: **45 meets · 18 partial · 16 does not meet · 17 N/A** (of 96).

### 9.3 Did it match the prediction? (validation checks)

- **(a) Free-text items rated with evidence, not skipped** — the bias/risk/limitation/use
  items (G06/G07) all received a status with a cited-evidence string. ✅ (G06/G07 mitigation
  confirmed in practice.)
- **(b) NA rule fired on scope/modality mismatch, not on tier** — N/A on the derived-dataset
  provenance block (primary dataset), the Text/NLP language item, experimental-design,
  ML-split, sensor-metadata, gridding, anonymization, secure-access, and the CARE-governance
  items; **no `All use cases` item was N/A**. ✅
- **(c) Core gaps surfaced as recommendations** — no funder/ORCID/contact, no issue-reporting,
  no supported-ML-task list / usage guidance / AI-ML usage history, no checksums, license not
  SPDX. These are exactly the model-centric and attribution gaps the archetypes flagged. ✅
- **(d) AI-ready is the weak dimension** — **ai_ready 0.556 vs the FAIR dimensions
  0.622–0.833** reproduces the project thesis ("FAIR ≠ AI-ready"). It also *agrees with* the
  earlier subjective evaluation of this same dataset (ai_ready 6/10 ≈ 0.6), which is a good
  reproducibility signal. Note the reproducible number (0.556) is **higher** than the generic
  "≈0.3–0.4" baseline in the agent's CLAUDE.md — because NEON beetles genuinely documents
  labeling provenance, missing-data flagging, and limitations; the granular item-level method
  gives it fair credit where the round "3–4/10" did not.
- **(e) Reproducible** — re-running the scorer (`--dry-run`) reproduces every number
  identically; 0 response-invariant violations (evidence present on every meets/partial;
  recommendation present exactly on partial/does-not-meet, empty on meets/N/A). ✅

### 9.4 Findings feeding back into the loop

- **R14 was partly a non-issue.** The v2 agent *already* rates the four levels with evidence;
  the "align the form `options`" task belonged to the archived **v1** form, not this agent.
  The real R14 value was the pilot itself, now done. **G15 closed (measured).**
- **The metadata-retrieval ceiling is now the practical bottleneck**, not the instrument. The
  JS-rendered landing page blocked the schema.org JSON-LD; several format/interoperability
  items would likely rate higher with it. Future pilots should pull structured metadata from
  an API/EML/DataCite endpoint rather than the HTML landing page.
- **Next:** pilot a second, contrasting dataset (GBIF or EDI/LTER) to test cross-repository
  scoring consistency; and act on **G14/R15** (instrument-gap vs dataset-disclosure-gap
  reclassification of the deferred P1/P2 gaps).
