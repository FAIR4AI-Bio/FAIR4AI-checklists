# TreeOfLife-200M Dataset Card
Source: https://huggingface.co/datasets/imageomics/TreeOfLife-200M/raw/main/README.md
Retrieved: 2026-08-21

## TreeOfLife-200M Overview

**Scale:** 233 million images representing 933,798 taxa—described as the "largest and most diverse" ML-ready biology computer vision dataset at release.

**Data Sources (4 providers):**
| Provider | Unique Taxa | Images |
|----------|------------|--------|
| GBIF | 569,225 | 222.6M |
| EOL | 48,508 | 5.2M |
| BIOSCAN-5M | 3,042 | 5.2M |
| FathomNet | 251 | 37.9K |

**Purpose:** Training biology foundation models, specifically BioCLIP 2 and BioCLIP 2.5 Huge.

**Key Contents:**
- `catalog.parquet` with taxonomic fields (kingdom through species), common names, source metadata
- Text embeddings for both models
- Provenance metadata, EOL-specific files, and FathomNet bounding-box data

**Curation Highlights:**
- Taxonomic standardization via the `TaxonoPy` package to a 7-rank Linnean structure
- Image quality filtering (museum specimen classifier, MegaDetector for camera traps, similarity checks for citizen science)
- Human face removal via MTCNN
- Duplication/data-leakage elimination using MD5 and PDQ hashes

**Coverage:** About 89.74% of images have full taxonomic labels; strong representation of threatened species (~70.38%).

**Licensing:** The compilation is dedicated to the public domain under CC0, but individual images carry varied licenses (CC0 to CC BY-NC-SA, CC BY-NC-ND for FathomNet, CC BY 3.0 for BIOSCAN-5M).

**Tasks:** Image classification, zero-shot and few-shot classification.
