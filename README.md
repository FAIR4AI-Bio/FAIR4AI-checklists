# FAIR4AI-checklists
FAIR4AI Working Group repo for organization, planning, and development.

## Dataset Evaluation Agent

**[`fair4ai-eval-agent/`](fair4ai-eval-agent/)** — Current agent (v2): a platform-agnostic AI agent that evaluates datasets for AI-readiness using the FAIR4AI-Bio checklist. Works with Claude Code, GitHub Copilot, and ChatGPT. See [`fair4ai-eval-agent/README.md`](fair4ai-eval-agent/README.md) for setup instructions.

`fair4ai-eval-agent-v1/` — Archived Python script agent (OpenAI/Azure/Anthropic). Superseded by v2.

## Current Resources/Drafts:

- [Definitions_FAIR4AI_AI-ready.md](Definitions_FAIR4AI_AI-ready.md)
    - Living document for defining FAIR4AI and AI-ready. 
    - Currently established as resource to help distinguish as we consider which elements of the [checklist](https://docs.google.com/spreadsheets/d/16WuJzLLMpovZs_iyWflq_eMhykMRaw9tNvGXOEmsabU/edit?gid=1026025652#gid=1026025652) are sufficient for FAIR, FAIR4AI, and AI-ready. 
    - This is meant to build on the [FAIR4AI Working Definitions from 0.5 Workshop](https://docs.google.com/document/d/1fLf9ZAhGEBTPgTCkOraE6H9G-2e2TDyBpPpXi2HoZ6k/edit?usp=sharing), which includes comments from Workshop 0.5 and notes for this group (see tabs on the sidebar).
- [DRAFT AI-Ready Checklist](https://docs.google.com/spreadsheets/d/16WuJzLLMpovZs_iyWflq_eMhykMRaw9tNvGXOEmsabU/edit?usp=sharing)
    - Based on combining the Imageomics [Data Card](https://imageomics.github.io/Imageomics-guide/wiki-guide/Data-Checklist/) and [Metadata](https://imageomics.github.io/Imageomics-guide/wiki-guide/Metadata-Checklist/) checklists[^1] with the [ESIIP Checklist](https://esip.figshare.com/articles/online_resource/Checklist_to_Examine_AI-readiness_for_Open_Environmental_Datasets/19983722/1?file=35578457)[^2].
- [AI-Readiness Defined Slides](https://docs.google.com/presentation/d/1FAXOJedUSOotnXn5984DOtGX62bLaR33PzgLOEDbUh4/edit?usp=sharing)
    - Presentation prepared for the 0.5 workshop to provide a common understanding/reference upon which to base our conversations.

[^1]: For context, the Imageomics metadata checklist is mostly a generalized version of the Data Card checklist. They fit in the [Imageomics Project Lifecycle](https://imageomics.github.io/Imageomics-guide/wiki-guide/Digital-Product-Lifecycle/) as part of the iterative process of filling out a dataset card and updating on GitHub with checklists in the GitHub project repo issue.

[^2]: There is also a [newer version on GitHub](https://github.com/ESIPFed/data-readiness/blob/main/checklist-published/ai-ready-data-checklist-v.1.0.md). I believe we incorporated both.

## Guiding Questions and Considerations

- What is the distinction between FAIR and FAIR4AI?
    - Is this different when thinking about biodiversity data?
    - How does it vary by data type/modality?
- What is the distinction between FAIR4AI and AI-Ready?
- What are the requirements and expectations for data providers as compared to users?

### Potential Answers or Framing

FAIR4AI is to the point that it can be fed into a pipeline to have an output ready to put into a model. This can be the "AI-enabled" step.

We are working from the idea that AI-Ready is meant as this data can be fed directly into a model, so data need not be published in this format, just in a format that it is "reasonable" to get there. An example being the [TreeOfLife-200M dataset](https://huggingface.co/datasets/imageomics/TreeOfLife-200M) is not AI-Ready, but using existing pipelines (once all data is downloaded), it can be transformed into the webdataset format used to train [BioCLIP 2](https://huggingface.co/imageomics/bioclip-2). Under this definition, the constituent parts of TreeOfLife-200M are not FAIR4AI.
