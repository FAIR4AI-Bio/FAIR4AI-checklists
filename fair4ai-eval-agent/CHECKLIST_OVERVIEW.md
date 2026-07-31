# FAIR4AI-Bio Dataset Checklist Overview: Summary of main sections

**Purpose:** This checklist evaluates biodiversity, ecology, and environmental science datasets for AI-enabled science. It extends the FAIR principles (Findable, Accessible, Interoperable, Reusable) with requirements specific to machine learning workflows — because FAIR is necessary but not sufficient for AI-ready data.  

The checklist is organized into nine sections, each targeting a distinct dimension of dataset quality. Each item is mapped to existing metadata standards (EML, DataCite, Schema.org, Croissant) to enable machine-readable compliance and partial automation.

---

## 1. General Information
*What the dataset is and how to find it.*

Information for a first-pass.
Standard bibliographic metadata: title, creators, publisher, date, abstract, keywords. Includes links to the dataset repository, associated paper(s), and related datasets. A data dictionary or codebook is expected to define all variables. The key AI-facing addition here is an explicit flag for machine-readiness — does the dataset conform to a structured, machine-actionable format?

---

## 2. Data Structure
*How the data are physically organized.*

Describes file formats, dataset organization (e.g., tabular, image directories, shards), individual file descriptions, the features/variables present, and overall technical specifications (size, record count). For AI use, formats should be open and machine-readable, with clear documentation of how records, files, and assets relate to each other. Biodiversity datasets commonly mix occurrence tables, media files, and annotation files — each needs its own structural description.

---

## 3. Source Data
*Where the dataset came from and how it was collected.*

Covers the data source type (field survey, remote sensing, eDNA, etc.), curation rationale, and whether the dataset is part of a larger collection. Critically for AI use: instrumentation and sensor metadata (make, model, placement, calibration) and sampling methods (design, effort, detectability, spatial/temporal resolution) must be documented. These "sampling semantics" determine whether a model trained on the data will generalize — a gap rarely addressed by standard FAIR metadata.

---

## 4. Data Processing
*What was done to the dataset before it reached its current form.*

Documents transformations applied after collection: unit standardization, spatial gridding, gap-filling (and the method used), data anonymization, outlier removal, and labeling/re-labeling. The most AI-critical item in this section is train/validation/test split definitions — splits must be documented to prevent data leakage and enable reproducible benchmarking. The method of labeling (human expert, crowd-sourced, model-assisted) must also be recorded as annotation provenance.

---

## 5. Data Quality
*How reliable and complete the data are.*

Evaluates four dimensions:
- **Completeness** — are all expected records present? Have required QA/QC steps been finished?
- **Consistency** — are units compatible across records? Are controlled vocabularies (e.g., a taxonomic backbone) used consistently?
- **Integrity** — are quality procedures documented? Has the dataset been peer-reviewed?
- **Timeliness** — is the data raw or quality-controlled? Is the update schedule known?

For ecology/biodiversity AI, consistency around taxonomy is especially important: the backbone used, the date of resolution, and how synonyms are handled all affect whether records from different sources can be merged safely.

---

## 6. Guidance & Recommendations
*What the data should and should not be used for.*

Documents known **biases, risks, and limitations** — including sampling biases (geographic, seasonal, observer), class imbalances, and non-detections (true absences vs. missing data). Records supported AI/ML tasks and any prior AI/ML usage history. Includes experimental design context if the data came from a designed study. This section operationalizes the "Datasheet for Datasets" tradition: intended use, out-of-scope use, and known failure modes.

---

## 7. Data Access
*How users obtain and use the data.*

Covers delivery options (direct download, API, cloud access, rate limits), format openness (open vs. proprietary, multiple format availability), and **license** — including whether the license is machine-readable (SPDX identifier preferred). Security and privacy controls are documented here: restricted-access tiers, sensitive data flags, and conditions of access. License compatibility across aggregated sources is an explicit concern for derived biodiversity datasets.

---

## 8. Provenance
*Where the dataset came from and who is responsible for it.*

Records the full citation for the dataset itself (authors, ORCIDs, DOI, checksums) and, for derived datasets, the chain back to source data (source DOIs, source producers, checksums of constituent files). Documents the processing platform and software used.

---

## 9. Data Governance
*e.g., Ethical/CARE considerations*

Based on the CARE Data Governance specification published with IEEE in 2025.
Documents ethical and CARE governance items: storage conditions, permission to collect observations, the agent who granted permission, and the Indigenous peoples or communities whose territories or knowledge are implicated. These governance fields are not optional add-ons — they determine legal and ethical reusability of the dataset.

---  

## Cross-cutting design principle

Each section operates at one of four metadata levels that must be kept distinct: **dataset/package**, **sampling event**, **occurrence/sample record**, and **media asset or annotation**. A single flat metadata record cannot adequately describe all four. An AI-ready biodiversity dataset should provide metadata at each applicable level, with uncertainty quantified explicitly (georeference uncertainty, identification confidence, label provenance) and sensitive-species or privacy constraints flagged before any reuse occurs.
