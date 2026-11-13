# Distinguishing AI-FAIR and AI-Ready from FAIR

## AI-FAIR Working Definitions

AI-FAIR extends FAIR standards with AI specific requirements:

1. Data/metadata can be queried _without_ downloading large files or specialized file types.  
2. Ontology used can be queried with synonyms from other ontologies.  
3. Content/context of the data point is extractable: occurrence-based vs image-based.

### Extended Definitions

**AI-ready Data:** Data that are ready to be included in AI infrastructure at scale.

**AI-enabled Data:** Data and/or metadata that has been augmented using AI, specifically for the purpose of being AI-ready.

**AI-FAIR Data:** Data that are FAIR enough for AI to be used in making data fully “AI-Ready”.

### AI-FAIR Metadata Criteria

The four key criteria necessary for AI-FAIR data, which enable the Derived categories (defined [below](#ai-fair-derived-categories)). For more details, please see [our paper](https://arxiv.org/abs/2611.03327).

1. **Structural:** Use, e.g., I need this info to be able to download and plug into a modeling pipeline (does NOT guarantee scientific validity of model).
    - Required for **ML-ready**
2. **Scientific:** Information about the data, context necessary to understand it and use it to draw scientifically valid conclusions.
    - This + ML-ready = **AI-ready for task**
3. **Provenance:** Information needed for appropriate citation, round-tripping, etc.
    - Traceable requirement—this enables further building on what is provided, e.g., allowing for extension beyond the specified tasks (when scientific is filled), opening the door for round-tripping (bringing value back to original source), etc.
    - Required for **traceable**
4. **Governance:** Includes CARE/Governance requirements + occurrence date/date of observation (see strikethrough note in category).
    - Required for **ethical/CARE compliant** standard

#### AI-FAIR Derived Categories

- **ML-ready:** All structural fields are filled in and then it is machine ready ***for the specified tasks***. Data can be ingested into a pipeline, does not guarantee scientific validity.
- **AI-ready for task:** List of tasks for which dataset is machine-ready; what the dataset was engineered to do (e.g., train-test split for CV species ID model), could be used for something else, but that may require extra processing, this is ***what it’s designed for***. 
- **Traceable:** Whether the dataset's origin can be followed back to its source(s) via persistent identifiers, forming an ***unbroken provenance chain***.
- **Ethical CARE Compliance:** appropriately documented for allowed vs restricted uses, proper attribution.

--

## AI-Ready Working Distinction

Setting a "dividing line" to distinguish AI-ready from FAIR4AI.

1. We use the term **AI-ready** to indicate that data are such that they can be included in AI infrastructure at scale.

2. Appropriately formatted documentation regarding distribution information and other values required for plugging the data into a standard model pre-processing pipeline is provided.

These should _not_ be taken to mean that the data are plug-and-play, but they may be. We provide some examples below to help clarify.

### Example distinctions

- Processing and standardization are _not_ required, but information about whether or not the data have been processed or standardized in some manner and ***how*** the processing or standardization was done _is_ required.

- Data distribution should be included in usable form (e.g., long tail on this value, simplistic idea: stratify on `y = long_tail_value`). Alternatively, splits may already be provided.

## Additional Considerations

- Inclusion of model provenance for generated data.
- Rate limiting information from data providers for server profiling (similar to what we did with [distributed-downloader](https://github.com/Imageomics/distributed-downloader)). If data can be streamed from the source, this is essential to success.
