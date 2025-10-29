# FAIR4AI-checklists
FAIR4AI Working Group repo for organization, planning, and development.

## Current Resources/Drafts:

- [FAIR4AI Working Definitions and Comments from Workshop 0.5](https://docs.google.com/document/d/1fLf9ZAhGEBTPgTCkOraE6H9G-2e2TDyBpPpXi2HoZ6k/edit?usp=sharing)
- [DRAFT AI-Ready Checklist](https://docs.google.com/spreadsheets/d/16WuJzLLMpovZs_iyWflq_eMhykMRaw9tNvGXOEmsabU/edit?usp=sharing)
- [AI-Readiness Defined Slides](https://docs.google.com/presentation/d/1FAXOJedUSOotnXn5984DOtGX62bLaR33PzgLOEDbUh4/edit?usp=sharing)

## Guiding Questions and Considerations

- What is the distinction between FAIR and FAIR4AI?
    - Is this different when thinking about biodiversity data?
    - How does it vary by data type/modality?
- What is the distinction between FAIR4AI and AI-Ready?
- What are the requirements and expectations for data providers as compared to users?

### Potential Answers or Framing

FAIR4AI is to the point that it can be fed into a pipeline to have an output ready to put into a model. This can be the "AI-enabled" step.

We are working from the idea that AI-Ready is meant as this data can be fed directly into a model, so data need not be published in this format, just in a format that it is "reasonable" to get there. An example being the [TreeOfLife-200M dataset](https://huggingface.co/datasets/imageomics/TreeOfLife-200M) is not AI-Ready, but using existing pipelines (once all data is downloaded), it can be transformed into the webdataset format used to train [BioCLIP 2](https://huggingface.co/imageomics/bioclip-2). Under this definition, the constituent parts of TreeOfLife-200M are not FAIR4AI.
