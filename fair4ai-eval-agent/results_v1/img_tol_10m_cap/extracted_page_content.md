---
license: cc-by-sa-4.0
language:
- en
- la
pretty_name: TreeOfLife-10M Captions
task_categories: 
- image-classification
- zero-shot-classification
- text-to-image
- question-answering
tags:
- biology
- image
- animals
- plants
- fungi
- CV
- evolutionary biology
- multimodal
- clip
- biology
- species
- taxonomy
- knowledge-guided
- imbalanced
- captions
size_categories: 1M<n<10M
description: "This dataset consists of generated captions, Wikipedia-derived descriptions, and format examples for the TreeOfLife-10M. These captions were generated using InternVL3-38B based on biological contexts that help the model generate more accurate captions. It was used to train BioCAP, a CLIP-based model."
configs:
- config_name: "sample captions"
  data_files: "format_example.parquet"
- config_name: "wiki descriptions"
  data_files: "wiki_description.parquet"
- config_name: "TOL-10M captions"
  data_files: "uuid_caption_description.parquet"
  default: true
---

# Dataset Card for TreeOfLife-10M Captions

This dataset consists of generated captions, Wikipedia-derived descriptions and format examples for the [TreeOfLife-10M](https://huggingface.co/datasets/imageomics/TreeOfLife-10M). These captions were generated using [InternVL3-38B](https://huggingface.co/OpenGVLab/InternVL3-38B-AWQ) based on biological contexts that help the model generate more accurate captions. It was used to train [BioCAP](https://huggingface.co/imageomics/biocap), a CLIP-based model.

## Dataset Details

### Dataset Description

- **Curated by:**  Ziheng Zhang, Xinyue Ma, Arpita Chowdhury, Elizabeth G Campolongo, Matthew J Thompson, Net Zhang, Samuel Stevens, Hilmar Lapp, Tanya Berger-Wolf, Yu Su, Wei-Lun Chao, Jianyang Gu
- **Languages:** English, Latin
- **Homepage:** https://imageomics.github.io/biocap
- **Repository:** [BioCAP](https://github.com/Imageomics/biocap)
- **Paper:** [BioCAP: Exploiting synthetic captions beyond labels in biological foundation models](https://arxiv.org/abs/2510.20095)

This dataset is comprised of captions for the images in [TreeOfLife-10M](https://huggingface.co/datasets/imageomics/TreeOfLife-10M) that were generated using [InternVL3 38B](https://huggingface.co/OpenGVLab/InternVL3-38B-AWQ). Specifically, we use biological knowledge as contexts to improve the quality and relevance of generated captions. This is through a process that extracts visual descriptions of taxa from Wikipedia, then provides sample captions (at most three per taxonomic class) as context for generating image-level captions. The full workflow is provided in the [BioCAP](https://github.com/Imageomics/biocap/blob/main/BioCAP-pipeline.md) repo, and all the visual descriptions and captions generated are provided in this dataset for reproducibility.


### Supported Tasks and Leaderboards

Image Classification, Zero-shot and few-shot Classification, text-to-image retrieval, and content-based querying for biological images.


## Dataset Structure

This dataset contains three pieces:
1. Format Examples: the sample captions (three species per taxonomic class) for the MLLM to use as a model in generating captions.
2. Derived Wikipedia Visual Information: the visual descriptions of species from Wikipedia. We provide these for reproducibility purposes, as Wikipedia pages are not versioned.
3. Image Captions: the TreeOfLife-10M image captions generated with the MLLM. 

```
/dataset/
    format_example.parquet
    wiki_description.parquet
    uuid_caption_description.parquet
```


###  1 & 2. Wikipedia and Format Examples 

Reference data for biological descriptions and formatting standards.

#### Files
- **`wiki_description.parquet`** (24MB): Processed Wikipedia articles containing visual descriptions. These are shared to ensure reproducibility and reusability since Wikipedia is not version-controlled.
- **`format_example.parquet`** (93KB): Examples of properly formatted biological descriptions to guide MLLM's caption generation.

#### Format Example Structure
- Columns: 
    - `class`: the taxonomic class of the species. Each class represents one row of the CSV.
    - `format_example`: example visual biology-based caption for a species of the class. Note that all three species are in a single row of the CSV (they are numbered 1 through 3).
- Contains detailed visual descriptions organized by taxonomic class.
- Examples include:
  - **Insecta**: Orchid Mantis, Rosy Maple Moth, Emerald Ash Borer
  - **Magnoliopsida**: Passion Flower, Venus Flytrap

#### Description Format
Each class contains numbered examples with detailed morphological descriptions:
```
1. The Orchid Mantis, Hymenopus coronatus, displays a body of white and pale pink,
   with flattened, lobed legs that mimic the petals of a flower, positioned amidst green foliage.
```

### 3. UUID Caption and Description Match

Complete UUID-caption-description mappings for all images in [TreeOfLife-10M dataset](https://huggingface.co/datasets/imageomics/TreeOfLife-10M). This file can be used to map the generated captions and Wikipedia-derived descriptions to their associated images from TreeOfLife-10M.

#### Files
- **`uuid_caption_description.parquet`** (1.8GB): A single comprehensive parquet file containing all mappings.
    - Contains UUID, caption, and description (if available) for every image in the TreeOfLife-10M dataset.
    - Generated captions for all 10 million biological images.
    - Wikipedia-derived descriptions are included in the third column when available.

#### Structure
- Three columns:
    - `uuid`: Unique identifier matching images in TreeOfLife-10M
    - `caption`: MLLM-generated image-specific caption
    - `description`: Wikipedia-derived species description (when available)
- Organized in a single parquet file for efficient storage and processing.

#### Data Access

To reproduce the complete BioCAP training dataset:

1. **Download the base dataset from:** https://huggingface.co/datasets/imageomics/TreeOfLife-10M (be sure to read their [reproduction instructions](https://github.com/Imageomics/bioclip/blob/main/docs/imageomics/treeoflife10m.md#reproduce-treeoflife-10m)).

2. **Use UUID caption and description match:**
   - Load the parquet file `uuid_caption_description.parquet`
   - Match UUIDs from TreeOfLife-10M images with generated captions.
   - Combine to create the complete training dataset with enhanced captions.

The `uuid_caption_description.parquet` file provides the essential bridge between the original TreeOfLife-10M images and the enhanced captions and descriptions used for [BioCAP](https://huggingface.co/imageomics/biocap) training.

### Data Splits

This is a training dataset. See the [evaluation section](https://huggingface.co/imageomics/biocap/blob/main/README.md#evaluation) of the BioCAP model card for the existing test sets used in evaluation. 

## Dataset Creation

### Curation Rationale

Though we can find species-level descriptions for many organisms, it is significantly harder to find image-level descriptions&mdash;even more so if we want those captions to be biologically meaningful. This dataset was constructed to evaluate both the ability of existing models to generate meaningful image-level captions (when provided biological context) and to further evaluate the impact of such captions on the biological abilities of models trained with them.

### Source Data

Images and taxonomic labels were sourced from the [TreeOfLife-10M dataset](https://huggingface.co/datasets/imageomics/TreeOfLife-10M). We used [Wikipedia](https://www.wikipedia.org/) to source the species-level visual descriptions for these taxa due to its breadth of coverage and ease of access.

#### Data Collection and Processing

The taxonomic labels from TreeOfLife-10M were filtered to unique taxa before feeding into the [Wiki Data Scraping and Filtering pipeline](https://github.com/Imageomics/biocap/blob/main/BioCAP-pipeline.md). Where genus-species pairs were duplicated within unique 7-rank strings (cross-kingdom matched names, known as _hemihomonyms_), we checked against the full string, deferring to the appropriate kingdom, to disambiguate the returned Wikipedia page options.

#### Who are the source data producers?

This dataset used visual descriptions sourced from [Wikipedia](https://www.wikipedia.org/) as part of prompting an MLLM to generate captions for images sourced from the [TreeOfLife-10M dataset](https://huggingface.co/datasets/imageomics/TreeOfLife-10M) using their associated taxonomic labels from that dataset. See the [TreeOfLife-10M dataset sources section](https://huggingface.co/datasets/imageomics/TreeOfLife-10M#source-data) for more details.

### Annotations

We use the taxonomic labels from [TreeOfLife-10M](https://huggingface.co/datasets/imageomics/TreeOfLife-10M) for both obtaining the visual descriptions from Wikipedia and for training the model. The visual information is determined through particular keywords and MLLM extraction/evaluation. This visual information is then used to create sample captions (format examples) for three species per taxonomic class. The captions are generated by providing these format examples for the taxonomic class and asking InternVL3 38B to provide an image-specific caption following that model. For more details, please see the Method section of [our paper](https://arxiv.org/abs/2510.20095).

#### Annotation process

Taxonomic labels come from the TreeOfLife-10M dataset (details in [their annotation process section](https://huggingface.co/datasets/imageomics/TreeOfLife-10M#annotation-process)).
See steps 1 & 2 of the [BioCAP pipeline](https://github.com/Imageomics/biocap/blob/main/BioCAP-pipeline.md) for details on the caption generation, starting with Wikipedia scraping.


## Considerations for Using the Data

We provided biological context (sourced from Wikipedia) to the model in an effort to ground the generation of image-specific captions in biological knowledge. As with any AI-generated text, we caution that these captions were not generated by taxonomic experts or biologists, though we endeavored to ground them in biological descriptions.


## Licensing Information

Captions are shared under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), since text used to help generate them (from [Wikipedia](https://wikipedia.org/)) is shared under this license.

## Citation

Please cite both the dataset and our paper, if you use this dataset in your research.

**Data**
```
@misc{TOL-10M-Cap2025,
  author = {Ziheng Zhang and Xinyue Ma and Arpita Chowdhury and Elizabeth G Campolongo and Matthew J Thompson and Net Zhang and Samuel Stevens and Hilmar Lapp and Tanya Berger-Wolf and Yu Su and Wei-Lun Chao and Jianyang Gu},
  title = {{TreeOfLife-10M Captions (Revision c048cd2)}},
  year = {2025},
  url = {https://huggingface.co/datasets/imageomics/TreeOfLife-10M-Captions},
  doi = {10.57967/hf/6801},
  publisher = {Hugging Face}
}
```

**Paper**
```
@article{zhang2025biocap,
  title    = {Bio{CAP}: Exploiting Synthetic Captions Beyond Labels in Biological Foundation Models},
  author   = {Ziheng Zhang and Xinyue Ma and Arpita Chowdhury and Elizabeth G Campolongo and Matthew J Thompson and Net Zhang and Samuel Stevens and Hilmar Lapp and Tanya Berger-Wolf and Yu Su and Wei-Lun Chao and Jianyang Gu},
  year     = {2025},
  eprint   = {2510.20095},
  archivePrefix={arXiv},
  primaryClass={cs.CV},
  url={https://arxiv.org/abs/2510.20095}
}

```

Please be sure to also cite the original data source(s):

```
@misc{wikipedia,
  author       = {{Wikipedia contributors}},
  title        = {Wikipedia, The Free Encyclopedia},
  year         = {2025},
  url          = {https://en.wikipedia.org/},
  note         = {Accessed: August 2025}
}
```

[TreeOfLife-10M Citation Information](https://huggingface.co/datasets/imageomics/TreeOfLife-10M#citation-information)

## Acknowledgements

We would like to thank Wasila Dahdul, Zhiyuan Tao, Yifan Liu, Fangxun Liu, Shuheng Wang, Ziqi Li, David Carlyn, Quang-Huy Nguyen, Yintie Lei, and Junke Yang for their help with the human evaluation, and the [Imageomics Team](https://imageomics.osu.edu/about/team) for their constructive feedback.

We sincerely thank PlantID.net (Bruce Homer-Smith and contributors to PlantID.net), as well as the Cornell Lab of Ornithology for providing
access to their biological media collections. The data made our retrieval evaluation possible.

This work was supported by the [Imageomics Institute](https://imageomics.org), which is funded by the US National Science Foundation's Harnessing the Data Revolution (HDR) program under [Award #2118240](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2118240) (Imageomics: A New Frontier of Biological Information Powered by Knowledge-Guided Machine Learning).

Our research is also supported by resources from the [Ohio Supercomputer Center](https://ror.org/01apna436).

Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.
