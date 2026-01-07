# Distinguishing FAIR4AI and AI-Ready from FAIR

## FAIR4AI Working Definitions

FAIR_4AI_ extends FAIR standards with AI specific requirements 

1. Data/metadata can be queried _without_ downloading large files or specialized file types.  
2. Ontology used can be queried with synonyms from other ontologies.  
3. Content/context of the data point is extractable: occurrence-based vs image-based.

### Extended Definitions

**AI-ready Data:** Data that are ready to be included in AI infrastructure at scale.

**AI-enabled Data:** Data and/or metadata that has been augmented using AI, specifically for the purpose of being AI-ready.

**FAIR4AI Data:** Data that are FAIR enough for AI to be used in making data fully “AI-Ready”.

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
