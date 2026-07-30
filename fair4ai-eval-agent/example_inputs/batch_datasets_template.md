# Datasets to evaluate

A sample **Markdown** input for `/batch-evaluate-datasets`. The skill parses the
dataset name + URL out of any of the layouts below (table, bullets, or bare links)
and normalizes them into a standard `batch_datasets_<date>.csv` in the run folder.
The two datasets here are the same as `batch_datasets_template.csv`, so either file
produces the same normalized list.

## As a table

| Dataset | URL | Submitter | Notes |
|---------|-----|-----------|-------|
| NEON Ground Beetles | https://data.neonscience.org/data-products/DP1.10022.001 | Eric Sokol (esokol@battelleecology.org) | NEON Ground Beetles |
| TreeOfLife-200M | https://huggingface.co/datasets/imageomics/TreeOfLife-200M | Elizabeth Campolongo (campolongo.4@osu.edu) | TreeOfLife-200M image dataset |

## Or as bullets (equivalent — pick one layout)

- NEON Ground Beetles — https://data.neonscience.org/data-products/DP1.10022.001
- TreeOfLife-200M — https://huggingface.co/datasets/imageomics/TreeOfLife-200M
