# Hugging Face API Dataset Record
Source: https://huggingface.co/api/datasets/imageomics/TreeOfLife-200M
Retrieved: 2026-08-21

**TreeOfLife-200M** (`imageomics/TreeOfLife-200M`)

- **Author:** imageomics
- **License:** cc0-1.0
- **Languages:** English (en), Latin (la)
- **Downloads:** 16,378 | **Likes:** 37
- **Created:** 2025-05-27 | **Last modified:** 2026-05-29
- **DOI:** 10.57967/hf/8980

**Overview:** The dataset contains 233 million images spanning 933,798 taxa. According to the description, it is the "largest and most diverse public ML-ready dataset for computer vision models in biology at release."

**Data sources:** Combines images and metadata from four biodiversity providers — GBIF, EOL (Encyclopedia of Life), BIOSCAN-5M, and FathomNet.

**Tasks:** image-classification, zero-shot-classification

**Purpose:** Used to train BioCLIP 2 and BioCLIP 2.5 Huge. The version shown here "completes the dataset cleaning process" and fixes an issue involving Observation.org occurrences that were previously missing.

**Structure:** Includes a catalog parquet file, metadata (Darwin finches, EOL manifests, FathomNet), resolved taxa parquet files partitioned by source (bioscan, eol, fathomnet, gbif), and precomputed text embeddings for BioCLIP 2 and 2.5.

**Storage used:** ~119.9 GB
