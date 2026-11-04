# Persona Development and Checklist Gap Analysis Workfow

This document describes the workflow used to perform FAIR4AI-Bio analyses and how to recreate them in a future chat session.

---
### Resources  
- link to google sheets version of checklist https://docs.google.com/spreadsheets/d/16WuJzLLMpovZs_iyWflq_eMhykMRaw9tNvGXOEmsabU/edit?gid=1881633771#gid=1881633771


---

# Project Context

The FAIR4AI-Bio project seeks to evaluate whether biodiversity and ecological datasets contain sufficient metadata, provenance, structure, documentation, and access information to support AI and machine learning workflows.

The primary artifact under evaluation is the FAIR4AI AI-readiness checklist.

This analysis always begins with the **current draft of the checklist provided by the user**. The checklist is treated as the authoritative starting point and may evolve between analyses.

The workflow consists of three major phases:

1. Checklist Review
2. Persona and Archetype Development
3. Persona-Driven Checklist Evaluation

---

# The Question–Data–Model Triangle

A central organizing concept for FAIR4AI-Bio is the **Question–Data–Model Triangle**.

The triangle recognizes that AI-readiness is not determined solely by the dataset.

Instead, AI-readiness emerges from the relationship among:

### Question

What scientific, management, educational, or policy question is being asked?

Examples:

- Where will an invasive species spread?
- Can we identify species from images?
- How will ecosystem productivity change?
- Which conservation areas should be prioritized?

### Data

What information is available?

Examples:

- Species occurrences
- Images
- Audio recordings
- Remote sensing products
- Sensor time series
- Habitat models

### Model

What AI/ML approach is being used?

Examples:

- Species distribution models
- Computer vision classifiers
- Bioacoustic recognition models
- Foundation models
- LLM-based synthesis tools
- Forecasting models

A dataset may be highly suitable for one combination of Question–Data–Model and completely unsuitable for another.

For this reason, persona development should intentionally span all three vertices of the triangle.

Importantly, the checklist focuses on the "data" vertext of the triangle and its relationships to the "question" vertext (i.e., are the data scientifically suitable to address the question) and the "model" vertex (i.e., is the data strcuturally suitable to be ingested by the AI/ML enabled software being used to address the question). An additional aspect to consider is "roundtripping" which involves the data provider (data vertex) receiving feedback from data users (i.e., flow of information or benefits from the other vertices to the "data" vertex)

---

# Phase 1 — Checklist Review

## Objective

Review the current draft FAIR4AI checklist supplied by the user.

## Inputs

The user provides:

- Current checklist draft
- Supporting schema mappings (if available)
- Previous gap analyses (if available)
- Existing FAIR4AI documentation (if available)

## Output

A structured understanding of:

- Checklist sections
- Definitions
- Required vs recommended fields
- Metadata mappings
- Intended evaluation scope

---

# Phase 2 — Persona and Archetype Development

## Objective

Develop personas that represent the diversity of users and workflows across the Question–Data–Model Triangle.

---

## Step 1 — Identify Representative Data Providers

Examples:

- NEON
- EDI
- LTER
- GBIF
- iNaturalist
- NatureServe

Additional providers may be added depending on project scope.

---

## Step 2 — Research User Communities

For each provider:

- Review documentation
- Review publications
- Review training materials
- Review APIs and software ecosystems
- Review AI/ML applications

---

## Step 3 — Build Triangle-Oriented Persona Framework

Each persona should explicitly represent one or more vertices of the Question–Data–Model Triangle.

Capture:

### User Context

- Role
- Organization type
- Skill level

### Question Context

- Scientific question
- Management question
- Policy question
- Educational question

### Data Context

- Data types used
- Data volume
- Metadata requirements
- Provenance requirements

### Model Context

- AI/ML methods
- Software platforms
- Computational environment
- Reproducibility requirements

### Pain Points

- Metadata gaps
- Access barriers
- Provenance issues
- Workflow bottlenecks

---

## Step 4 — Create Triangle-Balanced Personas

Instead of simply creating personas around repositories, intentionally create personas that emphasize different regions of the triangle.

### Question-Centric Personas

Users primarily motivated by a scientific or decision-making question.

Examples:

- Species distribution modeler
- Conservation planner
- Policy analyst

### Data-Centric Personas

Users primarily focused on data integration, stewardship, or reuse.

Examples:

- Information manager
- Repository curator
- Synthesis scientist

### Model-Centric Personas

Users primarily focused on AI/ML model development.

Examples:

- Computer vision engineer
- Foundation model developer
- Bioacoustics researcher

### Balanced Personas

Users operating across all three vertices.

Examples:

- Applied ecologist
- Wildlife biologist
- Environmental consultant

### Additional notes on generating personas:
Use webtools to research user personas relevant to the FAIR4AI-bio project. Research data users of NEON, the Environmental Data Initiative, the LTER, GBIF, iNat, and Natureserve to identify dataset typtes, use cases, research questions, and tools/software that can be used to generate personas. For the persona profiles, I will need you to Draft 1 paragraph for each data user persona. Research what criteria should would be useful to return in a person profile for each persona type. The persona profiles should include at least the type of data they are looking for or providing/managing, the type of task they are performing on or with the data, the type of software they will use to analyze or process the data, the data requirements they might have or want to communicate. 

### Here is an example uer persona:
**N1 – Aquatic Ecology Postdoc (Intermediate)**  
Priya is a postdoctoral researcher studying freshwater ecosystem dynamics across NEON sites. They primarily use NEON aquatic sensor time series (e.g., dissolved oxygen, temperature, chlorophyll) combined with watershed-scale data to build machine learning models that forecast harmful algal blooms. Their workflow spans R (neonUtilities, tidyverse) and Python (scikit-learn, PyTorch), often assisted by ChatGPT or Copilot for code generation. Priya needs consistent variable naming, machine-readable QA/QC flags, and clear provenance for sensor changes to ensure reliable training data. Their biggest pain points are inconsistent metadata across sites and uncertainty about which flagged data are safe to include in ML models.

---

## Step 5 — Consolidate Personas into Archetypes

Group personas into reusable archetypes.

### A1 — AI/ML Model Developer

Triangle emphasis:

- Model > Data > Question

Primary concern:

- Training-ready datasets

---

### A2 — Applied Researcher / Model User

Triangle emphasis:

- Question ≈ Data ≈ Model

Primary concern:

- Scientific validity

---

### A3 — Synthesis Scientist

Triangle emphasis:

- Data > Question > Model

Primary concern:

- Harmonization and reuse

---

### A4 — Data Steward / Information Manager

Triangle emphasis:

- Data >> Model and Question

Primary concern:

- Metadata quality

---

### A5 — Conservation Practitioner

Triangle emphasis:

- Question > Data > Model

Primary concern:

- Decision support

---

### A6 — Policy / Reporting User

Triangle emphasis:

- Question >> Data > Model

Primary concern:

- Defensibility and transparency

---

### A7 — Educator / Student / Citizen Scientist

Triangle emphasis:

- Question > Model > Data

Primary concern:

- Accessibility and learning

---

# Phase 3 — Checklist Evaluation

## Objective

Determine whether the checklist contains enough information to support dataset evaluation for each archetype and for representative Question–Data–Model combinations.

---

## Step 1 — Review Checklist Structure

Review:

- Categories
- Fields
- Definitions
- Metadata mappings
- Required status
- Use-case scopes

---

## Step 2 — Review Archetype Requirements

For each archetype summarize:

### Question Requirements

What decisions or scientific questions must be answered?

### Data Requirements

What data and metadata are required?

### Model Requirements

What AI/ML methods and software are involved?

---

## Step 3 — Build Coverage Matrix

Rows:

- Checklist sections

Columns:

- Archetypes

Ratings:

- Adequate
- Partial
- Missing
- Not Applicable

---

## Step 4 — Evaluate Triangle Coverage

For each archetype evaluate whether the checklist supports:

### Question Vertex

Can users determine whether the dataset supports their intended question?

### Data Vertex

Can users determine whether the dataset is scientifically and technically fit-for-use?

### Model Vertex

Can users determine whether the dataset supports the intended AI/ML workflow?

---

## Step 5 — Identify Gaps

For each gap record:

- Gap ID
- Description
- Affected archetypes
- Example personas
- Question/Data/Model vertex affected
- Publisher-provided vs repository-inferable
- New field vs refinement vs scoring issue

---

## Step 6 — Reconcile with Previous Analyses

Compare findings with:

- Previous gap analyses
- Croissant extensions
- FAIR4ML concepts
- FAIR4AI workshop outputs

Classify findings as:

- Reinforced
- Extended
- Novel

---

## Step 7 — Prioritize Recommendations

Score recommendations by:

### Impact

How many archetypes are affected?

### Triangle Coverage

How many vertices of the Question–Data–Model Triangle are improved?

### Importance

How critical is the issue for AI/ML readiness?

### Effort

How difficult is implementation?

Assign:

- P0
- P1
- P2

---

## Step 8 — Produce Deliverables

### Markdown Report

Includes:

- Executive summary
- Triangle description
- Archetypes
- Coverage matrix
- Gap analysis
- Recommendations
- Roadmap

### CSV Outputs

Includes:

- Coverage matrix
- Gap table
- Recommendations table

---

 To recreate this analysis:

> I have attached the current draft FAIR4AI checklist. Use that checklist as the primary artifact. Develop or update personas using the Question–Data–Model Triangle framework. Create archetypes spanning question-centric, data-centric, model-centric, and balanced workflows. Evaluate whether the checklist contains sufficient information to determine dataset suitability for each archetype. Then produce a coverage matrix, gap analysis, prioritized recommendations, roadmap, and overall sufficiency assessment. Produce two outputs: (1) a personas_and_archetypes.md document that includes the full persona and archetype descriptions, and (2) a gap_analysis_results.md document that includes the coverage matrix, gap analysis, prioritized recommendations, roadmap, and overall sufficiency assessment. The attached NOTES document and CHECKLIST_OVERVIEW document provide context. Review the documents in this github directory https://github.com/FAIR4AI-Bio/FAIR4AI-checklists/tree/fair4ai-eval-agent-v2/fair4ai-eval-agent which describes how I plan to use the checklist with an agent to evaluate datasets. Use this knowledge to guide recommended updates to the checklist. 