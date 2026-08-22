# TreeOfLife-200M Landing Page
Source: https://huggingface.co/datasets/imageomics/TreeOfLife-200M
Retrieved: 2026-08-21

## Overview
The **imageomics/TreeOfLife-200M** dataset is hosted on Hugging Face by the HDR Imageomics Institute. It has 37 likes and 189 organization members.

## Key Metadata
- **DOI:** `doi:10.57967/hf/8980`
- **License:** cc0-1.0 (public domain dedication)
- **Size:** 100M–1B (specifically **233M rows**)
- **Languages:** English, Latin
- **Modalities:** Image, Text
- **Format:** parquet
- **Tasks:** Image Classification, Zero-Shot Classification
- **Tags:** biology, image, imageomics, animals, plants, fungi (+8 more)
- **Compatible Libraries:** Datasets, pandas, Polars (+1)

## Dataset Structure
Single subset ("default") with one split ("train"), totaling 233M rows. Columns include:
- `uuid`, `source_url`, taxonomic ranks (`kingdom`, `phylum`, `class`, `order`, `family`, `genus`, `species`)
- `scientific_name`, `common`, `data_source`, `publisher`, `basis_of_record`, `img_type`
- `source_id`, `shard_filename`, `shard_file_path`, `base_dataset_file_path`

## Data Sources
The dataset aggregates biodiversity images from multiple providers, primarily:
- **GBIF** (via iNaturalist.org, observation.org, museums)
- **EOL** (Encyclopedia of Life)
- **BIOSCAN**

Publishers include natural history museums (e.g., "Natural History Museum," "MNHN," "Naturalis Biodiversity Center"), universities, and citizen science platforms.

## Records Coverage
Records span kingdoms including Animalia, Plantae, Fungi, and Archaeplastida, with a `basis_of_record` field distinguishing "HUMAN_OBSERVATION," "PRESERVED_SPECIMEN," and "MACHINE_OBSERVATION."
