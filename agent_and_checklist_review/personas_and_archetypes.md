# FAIR4AI-Bio: Personas and Archetypes

**Primary artifact:** `DRAFT AI-ready checklist – Schema Mapping_v20260722.csv` (8 sections, ~135 evaluable items)
**Framework:** Question–Data–Model (Q–D–M) Triangle (per `NOTES_workflow.md`)
**Reference:** `CHECKLIST_OVERVIEW.md` (General Information · Data Structure · Source Data · Data Processing · Data Quality · Guidance & Recommendations · Data Access · Provenance)
**Companion document:** `gap_analysis_results.md`
**Prepared:** 2026-07-23 · **Author:** Eric Sokol

---

## 1. Purpose and Framing

This document defines the user **personas** and consolidated **archetypes** used to stress-test the FAIR4AI-Bio checklist. Personas are drawn deliberately from across the Question–Data–Model Triangle so that the checklist can be evaluated against workflows in which different vertices dominate.

**Triangle recap.**

- **Question vertex** — the scientific, management, policy, or educational question driving the work (e.g., *Where will an invasive species spread? Can we identify species from images? How will productivity change? Which areas should be prioritized?*).
- **Data vertex** — the datasets themselves (occurrences, images, audio, sensor time series, remote-sensing products, habitat models).
- **Model vertex** — the AI/ML method or pipeline (species distribution models, CV classifiers, bioacoustic recognizers, foundation models, LLM/agentic tools, forecasting models).

The checklist evaluates the **Data vertex** and its two outward-facing edges — **Data ↔ Question** (are the data *scientifically* suitable to answer the question?) and **Data ↔ Model** (are the data *structurally* suitable to be ingested by the AI/ML software?) — plus a third **roundtripping** edge (does feedback and benefit flow from users back to the data provider?). A dataset can be "AI-ready" for one triangle configuration and unsuitable for another; persona coverage must therefore span **question-centric, data-centric, model-centric, and balanced** workflows.

**How the checklist will be used (agent context).** Per the `fair4ai-eval-agent` design in the project GitHub repo, the checklist is operationalized as a **machine-readable form** (`form_ai_checklist_automated.csv`: `position, section, title, description, question_type, options, required`) that an LLM agent answers by reading dataset metadata (Schema.org JSON-LD, EML, DataCite, ML Croissant, or metadata scraped from repository landing pages at NEON, DataONE, Zenodo, Dryad, Hugging Face, etc.). The agent returns, **per item**, a `response` (from `options`), an `evidence` string citing the source metadata, and `notes`; it then rolls up a `summary` with strengths, weaknesses, per-facet **FAIR score estimates**, and recommendations. This has a direct consequence for persona design: personas are not only human end-users — one persona (**M3**) *is* the agent — and every persona's needs must ultimately be expressible as **structured, evidence-bearing form items** rather than free text.

**Representative data providers considered:** NEON, EDI, LTER, GBIF, iNaturalist, NatureServe, Hugging Face–hosted biodiversity corpora (TreeOfLife-200M, BIOSCAN-5M, KABR), and derived cloud-native products.

---

## 2. Personas

Each persona has a structured header capturing the fields called out in the NOTES workflow (data types, task, software/environment, primary requirements, pain points) followed by a one-paragraph vignette. Persona IDs use a provider/vertex convention: **Q** = question-centric, **D** = data-centric, **M** = model-centric, **B** = balanced.

### 2.1 Question-Centric Personas
*Entry point is a specific scientific, management, or policy question. Data is a means to an end; models are tools.*

#### Q1 — Species Distribution Modeler (Intermediate–Advanced)
- **Triangle emphasis:** Question > Data ≈ Model
- **Providers:** GBIF, iNaturalist, NEON, NatureServe
- **Data types:** occurrence records, environmental covariates (WorldClim, MODIS, NEON AOP)
- **Task:** fit and evaluate SDMs / ecological niche models to predict range shifts under climate scenarios
- **Software:** R (`dismo`, `ENMeval`, `terra`, `sdmTMB`), Python (`elapid`, `pyimpute`), Google Earth Engine
- **Primary requirements:** documented sampling bias, detectability, controlled taxonomic vocabulary **with a resolution date**, coordinate uncertainty, open machine-readable licenses permitting redistribution of derived products
- **Pain points:** GBIF aggregates hide provider-specific sampling design; presence-only vs. presence–absence is rarely encoded; taxonomic-backbone drift between snapshots silently invalidates prior training runs

Rosa is a landscape-ecology postdoc modeling range shifts of a threatened salamander across the southeastern US. She pulls GBIF-mediated occurrences and NEON small-mammal data, joins them to NEON AOP hyperspectral products in GEE, and trains a MaxEnt-plus-boosted-regression ensemble. Before download she needs to know which records are presence-only vs. presence–absence, the taxonomic backbone and its resolution date, and whether the license permits publishing the trained model. She re-runs analyses whenever a GBIF snapshot changes but has no reliable way to detect *what* changed.

#### Q2 — Conservation Practitioner / Reserve Planner (Applied)
- **Triangle emphasis:** Question > Data > Model
- **Providers:** NatureServe, GBIF, state Natural Heritage programs, NEON
- **Data types:** species range polygons, occurrence points, habitat-suitability rasters, protected-area boundaries
- **Task:** prioritize parcels for acquisition; Marxan / Zonation systematic conservation planning
- **Software:** ArcGIS Pro, QGIS, `prioritizr` (R), Zonation, Marxan
- **Primary requirements:** rank-defensible provenance ("who says this species is here, when, how confidently?"), sensitive-species obfuscation flags, license terms compatible with government reporting, explicit out-of-scope-use statements
- **Pain points:** endangered-species coordinates must be masked but the mechanism is inconsistent across sources; derived NatureServe products lack the chain back to constituent observations; auditors ask questions requiring both dataset- and record-level provenance

Dev works for a regional land trust in the Southern Rockies. He stacks NatureServe Element Occurrences, GBIF-mediated iNaturalist research-grade observations, and NEON plot data into a reserve-design analysis. Because results are defended before a board and used to justify federal grant match, every input needs a stable citation, a clear license, and documented biases so he can write a defensible methods section. He builds no novel ML — he is a heavy consumer of models and predictions.

#### Q3 — Ecological Forecasting Scientist (Advanced)
- **Triangle emphasis:** Question > Model > Data
- **Providers:** NEON, EDI, LTER, remote-sensing archives
- **Data types:** near-real-time sensor time series, phenology observations, EFI forecasting-challenge data
- **Task:** iterative forecast → observe → update (EFI-style forecasting)
- **Software:** R (`neonUtilities`, `neon4cast`, `fable`), Python (`sktime`), Stan, cloud batch schedulers
- **Primary requirements:** documented latency between observation and publication; versioned/streaming updates with change logs; unambiguous QA/QC-flag semantics; machine-readable schema so pipelines don't break on new columns
- **Pain points:** provisional vs. quality-controlled data are hard to tell apart programmatically; upstream sensor swaps are not surfaced in metadata; pipelines must re-train on demand

Amara runs an aquatic-forecasting group contributing to the EFI NEON Forecasting Challenge. Her Docker pipeline pulls dissolved-oxygen and chlorophyll data every 24 h, fits a state-space model, and submits a probabilistic forecast. She needs a machine-readable signal for "is this record raw, provisional, or QC'd?" and needs to know when the schema last changed so her code doesn't silently fail. She actively feeds ambiguous-flag reports back to NEON — the roundtripping loop is real to her.

#### Q4 — Policy / Reporting Analyst (Applied)
- **Triangle emphasis:** Question >> Data > Model
- **Providers:** GBIF, NatureServe, national biodiversity portals
- **Data types:** aggregated indicators, national checklists, protected-area coverage statistics
- **Task:** GBF (Kunming-Montréal) monitoring, IPBES contributions, state-of-the-environment reporting
- **Software:** Excel, R (`bdvis`, `finch`), Power BI / Tableau
- **Primary requirements:** traceable citations for every number, defensible sampling framework, transparent bias disclosure, clear recommended-use and out-of-scope-use statements
- **Pain points:** the analyst takes the blame if a headline number is wrong; needs plain-language risks/limitations and machine-actionable citations

Ines works in a national biodiversity monitoring office producing annual indicators against GBF Target 4 (species-at-risk trends). Her outputs are read by ministers, so every number must trace to a citable dataset with a stable DOI and a written limitations statement. She rarely trains models but consumes others' predictions and must defend them.

### 2.2 Data-Centric Personas
*Primary work object is the data itself — curating, harmonizing, and preparing it for downstream reuse.*

#### D1 — Repository Data Curator / Information Manager (Intermediate–Advanced)
- **Triangle emphasis:** Data >> Question, Model
- **Providers:** EDI, NEON, GBIF nodes, LTER Information Managers
- **Data types:** the full catalog — tabular observations, sensor archives, images, controlled vocabularies
- **Task:** metadata review, EML/DataCite validation, DOI minting, congruence checking, sensitive-taxa flagging
- **Software:** EML validators, `EMLassemblyline` (R), DataCite XML tooling, custom ingest pipelines
- **Primary requirements:** fully specified controlled vocabularies; explicit metadata **level** (dataset/event/occurrence/media); CARE governance fields; version/checksum handling; operational definitions of "machine-ready" and "quality procedures"
- **Pain points:** many AI-readiness checklists conflate dataset- and record-level fields; curators need clear required-vs-recommended guidance and consolidation of duplicated items

Sam is the Information Manager for an LTER site. Every incoming package must pass congruence checks, receive a DOI, and be flagged for sensitive taxa before publication. Sam implements AI-readiness downstream, so vague terms ("machine-ready," "quality procedures") without operational definitions create real work.

#### D2 — Synthesis Scientist (Intermediate–Advanced)
- **Triangle emphasis:** Data > Question > Model
- **Providers:** multi-source — GBIF + EDI + LTER + NEON + literature-mined data
- **Data types:** harmonized occurrence, trait, phylogenetic, and environmental data
- **Task:** build derived synthesis products (BioTIME-style time series, trait databases)
- **Software:** R (`taxize`, `rgbif`, `traitdataform`), Python (`pygbif`, DuckDB), Snakemake / Nextflow
- **Primary requirements:** full provenance chain to constituent sources (DOIs + checksums); license compatibility across aggregated sources; taxonomic backbone with resolution date; controlled vocabularies
- **Pain points:** aggregating a hundred datasets is a license-compatibility puzzle; downstream users must cite constituents, but derived-dataset provenance is inconsistently modeled

Marisol assembles a continental freshwater-invertebrate trait database from EDI, GBIF, and published literature. Her output is a derived dataset she wants to publish with a citable DOI and a machine-readable provenance graph showing every source. She needs the checklist to answer: what are the source DOIs, what are their licenses, and can I redistribute?

#### D3 — Community-Science Platform Manager (Applied)
- **Triangle emphasis:** Data > Question ≈ Model
- **Providers:** iNaturalist, eBird, community platforms
- **Data types:** user-submitted images, audio, occurrences, community IDs/votes
- **Task:** moderate, validate, and expose research-grade data; enforce sensitive-species obfuscation
- **Software:** platform-native tooling, Darwin Core Archive exports, GBIF IPT
- **Primary requirements:** label provenance (who identified it, when, with what confidence); CARE / Indigenous governance; sensitive-taxon obfuscation; machine-readable **per-record** license
- **Pain points:** labels change over time as identifications are revised; downstream ML users need annotation provenance, but the checklist is dataset-level, not record-level

Kai manages a community-science platform integrating with GBIF. Records flow from users → community IDs → research-grade → GBIF export. AI/ML users want to know how labels were produced and whether they can trust them, but this metadata lives at the record level the current checklist barely models.

### 2.3 Model-Centric Personas
*Primary work object is the AI/ML model. Data is fuel; the workflow is defined by what a training loop (or an agent) expects.*

#### M1 — Computer Vision / Foundation-Model Engineer (Advanced)
- **Triangle emphasis:** Model >> Data > Question
- **Providers:** Hugging Face (TreeOfLife-200M, BIOSCAN-5M, iNat21), GBIF media, FathomNet
- **Data types:** large image corpora with hierarchical taxonomic labels, WebDataset / Parquet shards
- **Task:** pre-train and fine-tune vision foundation models (BioCLIP, DINOv2); fine-tune CV classifiers for species ID
- **Software:** PyTorch, torchvision, `webdataset`, HF `datasets`, Croissant loaders
- **Primary requirements:** Croissant conformance; explicit train/val/test splits **with a documented split strategy**; shard-level file descriptions; per-source licenses; taxonomic backbone with resolution date; machine-readable, **per-task** "task-ready" flag; checksum manifests
- **Pain points:** datasets claim "ML-ready" but lack splits, checksums, or documented label provenance; license mixing in aggregates blocks downstream release of trained weights

Wren is a research engineer training a bio foundation model. She only ingests datasets with a valid Croissant JSON-LD file, documented splits, and per-source licenses. She wants a single boolean — "is this task-ready for image classification?" — *plus* the machinery to verify it.

#### M2 — Bioacoustics / Audio ML Researcher (Advanced)
- **Triangle emphasis:** Model > Data > Question
- **Providers:** Xeno-Canto (via GBIF), Macaulay Library, ARBIMON, NEON bioacoustics pilots
- **Data types:** variable-length audio clips, spectrograms, weak/strong labels, deployment metadata
- **Task:** train BirdNET-style recognizers; adapt to new taxa/geographies
- **Software:** PyTorch, torchaudio, `opensoundscape`, Kaldi-style pipelines
- **Primary requirements:** sensor metadata (make/model/gain/sample rate/bit depth/channels); deployment metadata (mount height, habitat); sampling design (targeted vs. passive); timezone-aware timestamps; label confidence
- **Pain points:** almost none of the checklist's sensor-metadata pointers are populated in practice; audio-specific fields live outside dataset-level metadata

Ren is training a passive-acoustic recognizer for Neotropical anurans. The model's scientific validity depends on knowing recorder settings and mount geometry; without them, the model overfits to sensor artifacts.

#### M3 — LLM / Agentic Workflow Developer (Advanced) *(this persona is the `fair4ai-eval-agent` itself)*
- **Triangle emphasis:** Model >> Question > Data
- **Providers:** any — the model is agnostic; **the metadata is the product**
- **Data types:** dataset metadata records themselves (EML, DataCite, Croissant, Schema.org JSON-LD, landing-page meta tags)
- **Task:** build agents that discover, evaluate, score, and route datasets to appropriate downstream tasks — precisely the `fair4ai_agent.py` use case (read metadata → answer 135 form items with evidence → emit JSON/CSV + FAIR score estimate)
- **Software:** LangChain, LlamaIndex, MCP servers, Claude Code, custom RAG; OpenAI/Azure/Anthropic backends
- **Primary requirements:** JSON-LD / Croissant-serialized metadata; stable identifiers; "task-ready" and "machine-ready" as **machine-actionable booleans**; explicit out-of-scope statements; controlled vocabularies rather than free text; each checklist item phrased as an **answerable question with enumerated `options`** and a resolvable evidence locus
- **Pain points:** current checklists describe fields *humans* should fill in, not fields *agents* can reason over; free-text abstracts are not enough — agents need structured tasks, structured biases, structured licenses, and a defined evidence path or they hallucinate; ambiguous/duplicated items produce inconsistent scores across runs

Theo builds an agentic dataset-discovery service for an ecology institute — the operational embodiment of the FAIR4AI eval agent. His agent must answer, in seconds: "Given this scientific question, find candidate datasets, verify licenses, and check that splits and taxonomy match." Every unstructured field is a failure point, and every duplicated item is a source of scoring noise.

### 2.4 Balanced Personas
*Operate meaningfully at all three vertices, typically because the job spans field ecology, data handling, and applied modeling.*

#### B1 — Applied Wildlife Biologist (Intermediate)
- **Triangle emphasis:** Question ≈ Data ≈ Model
- **Providers:** NEON, GBIF, state-agency data, camera-trap consortia (Wildlife Insights, WildTrax)
- **Data types:** camera-trap images, species-detection outputs, GPS telemetry
- **Task:** population estimation, occupancy modeling with model-assisted labels
- **Software:** R (`unmarked`, `spOccupancy`), Wildlife Insights UI, MegaDetector, torch for fine-tuning
- **Primary requirements:** label provenance (human / model / model+review); sampling design (camera placement, effort); sensor metadata; clear license for redistributing images and derived counts
- **Pain points:** mixing model-labeled and human-labeled records without provenance breaks occupancy estimates; sensor metadata is critical but rarely documented at dataset level

Nadia runs a state-level carnivore monitoring program blending field data, MegaDetector-assisted detections, and hand-verified subsets. She both consumes and produces data, and needs the checklist to support annotation provenance and sampling design equally well.

#### B2 — Ecology Postdoc Using Agentic Tools (Intermediate–Advanced)
- **Triangle emphasis:** Question ≈ Data ≈ Model, with Model growing fast
- **Providers:** NEON, EDI, GBIF, remote-sensing archives
- **Data types:** multi-modal — sensor time series, tabular observations, images
- **Task:** exploratory analysis and forecasting assisted by LLM coding agents (Claude Code, GitHub Copilot)
- **Software:** R + Python + VS Code + Claude Code + Google Earth Engine
- **Primary requirements:** metadata an agent can parse; canonical example code; discoverable APIs with documented rate limits; machine-readable licenses; unambiguous versioning
- **Pain points:** agents hallucinate schemas when metadata is free text; discovery is hard without JSON-LD; the human pays the cost of every ambiguous field

Priya (the example in NOTES, extended) uses Claude Code to draft the first pass of every analysis. When checklist fields are structured, her agent works; when they are free text, she has to intervene. She is a leading indicator of where the checklist must go for AI-mediated science.

#### B3 — Educator / Student / Citizen Scientist (Beginner–Intermediate)
- **Triangle emphasis:** Question > Model > Data
- **Providers:** iNaturalist, GBIF, NEON EDU resources, NatureServe Explorer
- **Data types:** small curated teaching subsets, occurrence maps, precomputed indicators
- **Task:** class projects, capstone analyses, citizen-science contributions, learning ML basics
- **Software:** Jupyter, RStudio, spreadsheets, iNat mobile app
- **Primary requirements:** plain-language abstract (Schema.org `sc:abstract`); clear recommended use; accessible formats (CSV first); clear licensing; a strong out-of-scope statement so classroom conclusions aren't misleading
- **Pain points:** full metadata records are overwhelming; students need a short summary and a task list they can understand

Ana teaches an undergraduate biodiversity-data class. Her students need datasets they can *understand*, not just consume. Discoverability, plain-language descriptions, and clear "do not use for X" statements matter more than Croissant conformance.

---

## 3. Archetypes

Personas consolidate into **seven archetypes (A1–A7)** matching the NOTES workflow. Each specifies triangle emphasis, primary concern, representative personas, and the checklist sections most critical to it.

### A1 — AI/ML Model Developer
- **Triangle emphasis:** Model > Data > Question
- **Primary concern:** training-ready, reproducible datasets
- **Personas:** M1, M2, M3, and the model-facing side of B1/B2
- **Critical checklist sections:** Data Structure (formats, features, technical specs, splits) · Data Processing (splits, labeling, gap-filling) · Source Data (instrumentation, sensor metadata, resolution) · Data Access (machine-readable format, API, cloud, SPDX license) · Provenance (checksums, derived-dataset chain)

### A2 — Applied Researcher / Model User
- **Triangle emphasis:** Question ≈ Data ≈ Model
- **Primary concern:** scientific validity of derived inferences
- **Personas:** Q1, Q3, B1, B2
- **Critical checklist sections:** Source Data (sampling design, instrumentation) · Data Quality (all four dimensions) · Guidance & Recommendations (bias, limitations, experimental design) · General Information (data dictionary, keywords, task-ready)

### A3 — Synthesis Scientist
- **Triangle emphasis:** Data > Question > Model
- **Primary concern:** harmonization and licensed reuse across sources
- **Personas:** D2, and parts of D1
- **Critical checklist sections:** Provenance (derived-dataset fields, DOIs, checksums) · Data Quality (controlled vocabulary, consistency) · Data Access (license, SPDX, license compatibility) · Source Data (data source, curation rationale)

### A4 — Data Steward / Information Manager
- **Triangle emphasis:** Data >> Question and Model
- **Primary concern:** metadata quality, governance, publishability
- **Personas:** D1, D3
- **Critical checklist sections:** all, especially General Information (standard metadata, references) · Provenance (citation, ORCID, CARE governance) · Data Access (license, security/privacy) · Data Quality (integrity, timeliness)

### A5 — Conservation Practitioner
- **Triangle emphasis:** Question > Data > Model
- **Primary concern:** decision support and defensibility
- **Personas:** Q2, and the applied side of Q4
- **Critical checklist sections:** Guidance & Recommendations (bias, limitations, recommended/out-of-scope use) · Data Access (license, sensitive-data flags) · Provenance (citation, agent-granting-permission for CARE) · Source Data (sampling design)

### A6 — Policy / Reporting User
- **Triangle emphasis:** Question >> Data > Model
- **Primary concern:** defensibility, transparency, traceable citations
- **Personas:** Q4
- **Critical checklist sections:** General Information (references, related dataset, paper) · Guidance & Recommendations (bias, limitations, out-of-scope) · Provenance (citation, source data, DOI) · Data Quality (peer review, integrity)

### A7 — Educator / Student / Citizen Scientist
- **Triangle emphasis:** Question > Model > Data
- **Primary concern:** accessibility, learnability, safe use
- **Personas:** B3
- **Critical checklist sections:** General Information (short summary, keywords, data dictionary) · Data Access (open format, direct download, license) · Guidance & Recommendations (recommended use, out-of-scope) · Data Quality (completeness, peer review)

---

## 4. Cross-Cutting Observations

Three observations shape the companion gap analysis:

1. **The checklist operates almost entirely at the dataset/package level.** Several archetypes (A1, A2, A3, and the D3-driven side of A4) need metadata at the **sampling-event, occurrence, and media/annotation** levels — a fact the checklist's "cross-cutting design principle" acknowledges but does not operationalize per item.

2. **"Machine-ready" and "task-ready" are single booleans.** Model-centric archetypes (A1, and the model side of A2/B2) need a **per-task, per-modality** readiness signal (e.g., "ready for image classification," "ready for bioacoustic recognition," "ready for occupancy modeling"), which the `Is task ready` field points at but does not yet structure.

3. **The agent turns "who fills the field" into "can the field be evaluated from evidence."** Because the `fair4ai-eval-agent` answers each item from metadata and must attach an `evidence` string, every free-text item is a place where the agent either fails silently or hallucinates. Persona **M3** therefore reframes the entire checklist: the target state is a form of **structured, enumerable, evidence-locatable** items with controlled-vocabulary `options`. This directly motivates the P0/P1 recommendations in `gap_analysis_results.md`.

---

## 5. Persona → Archetype → Triangle Map (quick reference)

| Persona | Archetype | Primary vertex | Most critical edge |
|---|---|---|---|
| Q1 Species Distribution Modeler | A2 | Question | Data ↔ Question |
| Q2 Conservation Planner | A5 | Question | Data ↔ Question |
| Q3 Ecological Forecaster | A2 | Question | Data ↔ Model |
| Q4 Policy / Reporting Analyst | A6 | Question | Data ↔ Question (roundtrip citations) |
| D1 Repository Curator / IM | A4 | Data | Data (governance) |
| D2 Synthesis Scientist | A3 | Data | Data ↔ Provenance |
| D3 Community-Science Manager | A4 | Data | Data ↔ Model (record-level) |
| M1 CV / Foundation-Model Engineer | A1 | Model | Data ↔ Model |
| M2 Bioacoustics ML Researcher | A1 | Model | Data ↔ Model (sensor) |
| M3 LLM / Agentic Developer *(the agent)* | A1 | Model | Data ↔ Model (machine-actionable) |
| B1 Applied Wildlife Biologist | A2 | Balanced | all three |
| B2 Ecology Postdoc w/ Agents | A2 | Balanced | all three (Model rising) |
| B3 Educator / Student / Citizen | A7 | Balanced | Data ↔ Question (accessibility) |

*Gap analysis, coverage matrix, recommendations, roadmap, and overall sufficiency assessment are in the companion `gap_analysis_results.md`.*
