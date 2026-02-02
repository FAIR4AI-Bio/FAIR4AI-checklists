---
configs:
- config_name: default
  data_files:
  - split: train
    path: "dataset/catalog.parquet"
license: cc0-1.0
language:
- en
- la
pretty_name: TreeOfLife-200M
task_categories: 
- image-classification
- zero-shot-classification
tags:
- biology
- image
- imageomics
- animals
- evolutionary biology
- CV
- multimodal
- clip
- biology
- species
- taxonomy
- knowledge-guided
- imbalanced
size_categories:
- 100M<n<1B
description: "With nearly 214 million images representing 952,257 taxa across the tree of life, TreeOfLife-200M is the largest and most diverse public ML-ready dataset for computer vision models in biology at release. This dataset combines images and metadata from four core biodiversity data providers: Global Biodiversity Information Facility (GBIF), Encyclopedia of Life (EOL), BIOSCAN-5M, and FathomNet to more than double the number of unique taxa covered by TreeOfLife-10M, adding 50 million more images than BioTrove (and nearly triple the unique taxa). TreeOfLife-200M also increases image context diversity with museum specimen, camera trap, and citizen science images well-represented. Our rigorous curation process ensures each image has the most specific taxonomic label possible and that the overall dataset provides a well-rounded foundation for training BioCLIP 2 and future biology foundation models."
---


# Dataset Card for TreeOfLife-200M

With nearly 214 million images representing 952,257 taxa across the tree of life, TreeOfLife-200M is the _largest_ and _most diverse_ public ML-ready dataset for computer vision models in biology at release. This dataset combines images and metadata from four core biodiversity data providers: Global Biodiversity Information Facility ([GBIF](https://gbif.org)), Encyclopedia of Life ([EOL](https://eol.org)), [BIOSCAN-5M](https://github.com/bioscan-ml/BIOSCAN-5M), and [FathomNet](https://www.fathomnet.org/) to more than double the number of unique taxa covered by [TreeOfLife-10M](https://huggingface.co/datasets/imageomics/TreeOfLife-10M), adding 50 million more images than [BioTrove](https://huggingface.co/datasets/BGLab/BioTrove) (and nearly triple the unique taxa). TreeOfLife-200M also increases image context diversity with museum specimen, camera trap, and citizen science images well-represented (see [Image Types](#image-types-gbif-only)). Our rigorous [curation process](#data-curation-and-processing) ensures each image has the most specific taxonomic label possible and that the overall dataset provides a well-rounded foundation for training [BioCLIP 2](https://huggingface.co/imageomics/bioclip-2) and future biology foundation models.

## Dataset Details

### Dataset Description

- **Curated by:** Jianyang Gu, Samuel Stevens, Elizabeth G. Campolongo, Matthew J. Thompson, Net Zhang, Jiaman Wu, Andrei Kopanev, and Alexander E. White
- **Homepage:** https://imageomics.github.io/bioclip-2/
- **Repository:** [TreeOfLife-toolbox](https://github.com/Imageomics/TreeOfLife-toolbox)
- **Paper:** [BioCLIP 2: Emergent Properties from Scaling Hierarchical Contrastive Learning](https://doi.org/10.48550/arXiv.2505.23883)


### Supported Tasks and Leaderboards

Image Classification, Zero-shot and few-shot Classification.


## Dataset Contents

```
/dataset/
    catalog.parquet
    embeddings/
      txt_emb_species.json
      txt_emb_species.npy
    metadata/
        Darwin-finches.csv
        eol_metadata/
            media_manifest.csv
            taxon.tab
        fathom_metadata.csv
        provenance.parquet   # For full Dataset
        resolved_taxa/       # product of TaxonoPy
            source=bioscan/
            source=eol/
            source=fathomnet/
            source=gbif/
```

The `embeddings/` directory contains the [BioCLIP 2](https://huggingface.co/imageomics/bioclip-2) text embeddings for all 190,988,120 images with full taxonomic labels in the TreeOfLife-200M dataset. See [`embeddings/README.md`](embeddings/README.md) for more information.


To avoid republishing existing datasets or interfering with original data source providers' ability to track use of their data, we provide all metadata here with step-by-step reproduction instructions in the [GitHub repository](https://github.com/Imageomics/TreeOfLife-toolbox/tree/main/docs#treeoflife200m-dataset-download-guide) to download the images and recreate the proper webdataset structure. This process will produce a collection of files named `shard-######.tar` in a `train` folder with which to work.

Inside each shard is a collection of images (named `<uuid>.jpg`), for which each has the following files:
```
<uuid>.com.txt
<uuid>.common_name.txt
<uuid>.jpg
<uuid>.sci.txt
<uuid>.sci_com.txt
<uuid>.scientific_name.txt
<uuid>.taxon.txt
<uuid>.taxonTag.txt
<uuid>.taxonTag_com.txt
<uuid>.taxon_com.txt
<uuid>.taxonomic_name.txt
```

### Data Instances

Each image in this dataset is matched to the [7-rank Linnean taxonomy](https://www.britannica.com/science/taxonomy/The-Linnaean-system) and common name of the subject of the image (where available). Examples of these text types is provided below. 89% (190,988,120) of the images have full taxonomic labels (for more context, see discussion on labeling challenges in biodiversity data under [Considerations for Use](#bias-risks-and-limitations)). In addition to the biodiversity introduced (952,257 unique taxa), these images also span a variety of settings (or "images types"), the three main categories we highlight being museum specimen, camera trap, and citizen science images. Counts for these and more specific museum specimen subcategories (as used in [processing](#data-curation-and-processing)) are provide in a table below.

#### Text Types
| Text Type | Example |
| ---- | -------- |
| Common name | Narrow-leaved meadow-grass |
| Scientific name | _Poa angustifolia_ |
| Taxonomic label | _Plantae Tracheophyta Liliopsida Poales Poaceae Poa angustifolia_ |


### Image Types (GBIF only)
| Image Type | Number of Images |
| :-------------------------- | :--------: |
|Camera-trap                                     |617.8K        |
|Citizen Science                                 |151M        |
|Museum Specimen: Fungi                          |599.5K        |
|Museum Specimen: Insect                         |7.9M          |
|Museum Specimen: Invertebrate Zoology           |1.7M          |
|Museum Specimen: Microbiology                   |38.7K         |
|Museum Specimen: Plant                          |39.7M         |
|Museum Specimen: Uncategorized                  |1M          |
|Museum Specimen: Vertebrate Zoology - Amphibians|36.2K         |
|Museum Specimen: Vertebrate Zoology - Birds     |435.3K        |
|Museum Specimen: Vertebrate Zoology - Fishes    |199.7K        |
|Museum Specimen: Vertebrate Zoology - Mammals   |129.1K        |
|Museum Specimen: Vertebrate Zoology - Others    |137K        |


### Data Fields

**catalog.parquet**
 - `uuid`: unique identifier for the image in this dataset, created at time of download.
 - `source_url`: URL from which the image was downloaded, used to preview image in viewer.
 - `kingdom`: kingdom to which the subject of the image belongs (`Animalia`, `Plantae`, `Fungi`, `Chromista`, `Protozoa`, `Bacteria`, `Viruses`, `Archaea`, and less than 1% unresolved cases, e.g., `Metazoa` and `incertae sedis`).
 - `phylum`: phylum to which the subject of the image belongs.
 - `class`: class to which the subject of the image belongs.
 - `order`: order to which the subject of the image belongs.
 - `family`: family to which the subject of the image belongs.
 - `genus`: genus to which the subject of the image belongs.
 - `species`: species to which the subject of the image belongs; note that this is the specific epithet.
 - `scientific_name`: `<Genus> <species>`  of the subject of the image, or most specific taxonomic rank available.
 - `common`: vernacular name associated with the subject of the image where available. Common name is sourced from GBIF vernacular names provided in the [GBIF Backbone Taxonomy](https://doi.org/10.15468/39omei).
 - `data_source`: source from which the record was obtained (`gbif`, `eol`, `bioscan`, or `fathomnet`).
 - `publisher`: the organization or entity that published the data (exclusive to GBIF records).
 - `basisOfRecord`: basis of the record (e.g., `PRESERVED_SPECIMEN`, `HUMAN_OBSERVATION`, `MACHINE_OBSERVATION`; exclusive to GBIF records).
 - `img_type`: the type of the associated image or its subject (e.g., `Museum Specimen: Fungi`, `Citizen Science`, `Camera-trap`), as defined by our processing (exclusive to GBIF records; EOL, BIOSCAN, and FathomNet images are all classified as `Unidentified).
 - `source_id`: unique identifier for the image used by the source.
    - **Note:** for GBIF, this is `gbifID` which is unique to the _occurrence_ containing the image. For EOL, this is `<EOL Content ID>_<EOL Page ID>`, the first of which is not a persistent identifier.
 - `shard_filename`: name of shard containing the image.
 - `shard_file_path`: filepath of the shard containing the image.
	- ex: `200M_v1.1/224x224/shards/shard-00123.tar`
- `base_dataset_file_path`: filepath of the parquet file in the dataset containing the image.
	- ex: `data/source=gbif/server=observation.org/data_7c3169bf-9670-4c03-86e7-c6d31436bb33.parquet`


**provenance.parquet:** Provenance metadata for the full dataset.
 - `uuid`: unique identifier for the image in this dataset, created at time of download.
 - `source_id`: unique identifier for the image used by the source. 
    - **Note:** for GBIF, this is `gbifID` which is unique to the _occurrence_ containing the image. For EOL, this is `<EOL Content ID>_<EOL Page ID>`, the first of which is not a persistent identifier.
 - `data_source`: source from which the record was obtained (`gbif`, `eol`, `bioscan`, or `fathomnet`).
 - `source_url`: URL from which image was downloaded.
 - `license_name`: name of license attached to the image (eg., `cc-by`).
 - `copyright_owner`: copyright holder for the image, filled with `not provided` if no copyright owner was provided. 
 - `license_link`: URL to the listed license, left null in the case that `license_name` is `No known copyright restrictions`.
 - `title`: title provided for the image, filled with `not provided` if no title was pro

**Darwin-finches.csv:** File for Darwin's finches embedding space evaluation completed in [paper](https://doi.org/10.48550/arXiv.2505.23883). Images are a represenative subset of the 18 species known as "Darwin's Finches" sampled from TreeOfLice-200M for this evaluation. Common names are from [Avibase](https://avibase.bsc-eoc.org/avibase.jsp).
 - `uuid`: unique identifier for the image in this dataset, links to other TreeOfLife-200M metadata.
 - `scientific_name`: scientific name of the species.
 - `filepath`: `<scientific_name>/<uuid>.jpg` the expected filepath to the images when calling them from a directory with the images organized in subfolders determined by the scientific name of the bird in the image.
 - `common_name`: common name used by Avibase for the species.
 - `group`: the "group" to which the bird belongs ('tree finches', 'warbler finches', 'ground finches', 'cactus finches', 'vampire finch', 'Cocos finch', or 'vegetarian finch'), as determined by name and the paper, Lamichhaney, S., Berglund, J., Almén, M. _et al_. Evolution of Darwin’s finches and their beaks revealed by genome sequencing. _Nature_ **518**, 371–375 (2015). https://doi.org/10.1038/nature14181.

      **`group` image counts:**
      | group name | number of images |
      | :------- | --: |
      | ground finches      | 180 |
      | tree finches        | 145 |
      | cactus finches      | 133 |
      | warbler finches     | 100 |
      | Cocos finch         | 50 |
      | vegetarian finch    | 50 |
      | vampire finch       | 19 |


#### EOL-specific Files

**media_manifest.csv:** File with license, source, and copyright holder associated to each image from EOL listed in `catalog.parquet` and `provenance.parquet`; use `<EOL Content ID>_<EOL Page ID>` to match on `source_id` for `provenance.parquet`. Remaining columns are
  - `EOL content ID`: unique identifier within EOL database for images sourced from [EOL](https://eol.org). Note that EOL content IDs are not stable.
  - `EOL page ID`: identifier of page from which images from EOL are sourced. Note that an image's association to a particular page ID may change with updates to the EOL (or image provider's) hierarchy. However, EOL taxon page IDs are stable.
  - `Medium Source URL`: URL pointing to source of image.
  - `EOL Full-Size Copy URL`: URL to access the full-sized image; this is the URL from which the image was downloaded for this dataset (see [Initial Data Collection and Normalization](#initial-data-collection-and-normalization) for more information on this process).
  - `License Name`: name of license attached to the image (e.g., `cc-by`).
  - `Copyright Owner`: copyright holder for the image, filled with `not provided` if no copyright owner was provided. 

**taxon.tab:** Tab-delimited file with taxonomic information for EOL images based on EOL page IDs. 
  - `taxonID`: unique identifier for the file.
  - `source`: often `<source>:<id>` where the source corresponds to the domain of the `furtherInformationURL`. The ID likely corresponds to an ID at the source.
  - `furtherInformationURL`: URL with more information on the indicated taxon.
  - `acceptedNameUsageID`: `taxonID` for the name accepted to represent this entry. Less than a third of these are non-null
  - `parentNameUsageID`: `taxonID` of taxonomic rank above the indicated `taxonRank` in the hierarchy (eg., the `taxonID` of the genus `Atadinus` for the `Atadinus fallax (Boiss.) Hauenschild` entry).
  - `scientificName`: scientific name associated with the EOL page (`<canonicalName> <authority>`, authority as available).
  - `taxonRank`: lowest rank of the taxonomic tree indicated (eg., `genus` or `species`), occasionally not indicated, even for accepted names.
  - `taxonomicStatus`: whether the name is accepted by EOL or not (`accepted` or `not accepted`, correspond to existence of non-null `eolID` or `acceptedNameUsageID` entry, respectively).
  - `datasetID`: generally corresponds to the source identified in `source` column.
  - `canonicalName`: the name(s) associate with the `taxonRank` (eg., `<Genus> <species>` for species).
  - `authority`: usually name of person who assigned the name, with the year as available.
  - `eolID`: the EOL page ID (only non-null when `taxonomicStatus` is accepted by EOL).
  - `Landmark`: numeric values, meaning unknown, mostly null.
  - `higherClassification`: labeling in the EOL Dynamic Hierarchy above the `taxonRank` (eg., `Life|Cellular Organisms|Eukaryota|Opisthokonta|Metazoa|Bilateria|Protostomia|Ecdysozoa|Arthropoda|Pancrustacea|Hexapoda|Insecta|Pterygota|Neoptera|Endopterygota|Coleoptera|Adephaga|Carabidae|Paussus`).


#### FathomNet Specific File
**fathom_metadata.csv:** Metadata file with FathomNet images identifiers and associated bounding boxes. This is required to fetch FathomNet images since there are multiple bounding boxes used from some images to generate final TreeOfLife-200M images.
 - `uuid`: unique identifier to match to `catalog` and `provenance` parquet files.
 - `x`,`y`: together these columns give the reference coordinate from which to construct the bounding boxes.
 - `width`: width in pixels of bounding box the image came from.
 - `height`: height in pixels of bounding box the image came from.
This file is required along with `provenance.parquet` to fetch all the FathomNet images since some are pulled from bounding boxes around different creatures in the same base image.

### Data Splits

This entire dataset was used for training the model. 
We used 11 biologically-relevant datasets for various species classification tests of the model trained on this dataset; they are described (briefly) and linked to below.


#### Test Sets

[BioCLIP 2](https://huggingface.co/imageomics/bioclip-2) was tested on the same 10 biologically-relevant benchmarks as [BioCLIP](https://huggingface.co/imageomics/bioclip#testing-data), though we used [NABirds](https://dl.allaboutbirds.org/nabirds) in place of [Birds 525](https://www.kaggle.com/datasets/gpiosenka/100-bird-species), since the latter is no longer available online. We also curated [IDLE-OO Camera Traps](https://huggingface.co/datasets/imageomics/IDLE-OO-Camera-Traps).

 - [NABirds](https://dl.allaboutbirds.org/nabirds): 48K images of the 400 most common North American birds (based on observation counts), with at least 100 images per species. Includes age and sex annotations that we used for evaluation.
 - [Meta-Album](https://paperswithcode.com/dataset/meta-album): Specifically, we used the Plankton, Insects, Insects 2, PlantNet, Fungi, PlantVillage, and Medicinal Leaf datasets.
 - [Rare Species](https://huggingface.co/datasets/imageomics/rare-species): Balanced benchmark dataset with 400 species (30 images per species) listed under 5 [IUCN Red List](https://www.iucnredlist.org/) categories (Near Threatened, Vulnerable, Endangered, Critically Endangered, and Extinct in the Wild).
 - [IDLE-OO Camera Traps](https://huggingface.co/datasets/imageomics/IDLE-OO-Camera-Traps): A new benchmark we curated from a combination of 5 different LILA BC camera trap datasets with image-level labels. These were filtered to contain only images with a single species of animal in frame.

Additional hierarchical structure and embedding space evaluation was done using images of Darwin's Finches sourced from the training data (in `metadata/Darwin-finches.csv`). These species are not evenly represented in the dataset, so 12 of them have 50 images each, but the remaining six species (_Geospiza propinqua_, _Geospiza acutirostris_, _Camarhynchus psittacula_, _Geospiza septentrionalis_, _Camarhynchus pauper_, _Camarhynchus heliobates_) have between 8 and 33 representative images (listed in decreasing order).

Other non-species classification tasks were also used for testing, and are described in the [BioCLIP 2](https://huggingface.co/imageomics/bioclip-2) model card and [our paper](https://doi.org/10.48550/arXiv.2505.23883).

## Dataset Creation

### Curation Rationale

TreeOfLife-200M was curated for the purpose of training a biological foundation model. In particular, we aimed to increase the both the biodiversity of available training data (i.e., from that available in [TreeOfLife-10M](https://huggingface.co/datasets/imageomics/TreeOfLife-10M)) and the raw number of images available (i.e., from that of [BioTrove](https://huggingface.co/datasets/BGLab/BioTrove)). We also performed extensive data curation beyond that used for either of these training datasets: aligning taxonomic labels, removing images of labels or folders associated to specimens, removing noisy citizen science and camera trap images, and ensuring no identifiable humans are in the images (more info below).

We have expanded coverage across the 2.14M described species estimated by [The International Union for Conservation of Nature (IUCN)](iucnredlist.org) as of [March 2025](https://nc.iucnredlist.org/redlist/content/attachment_files/2025-1_RL_Table_1a.pdf), with particularly strong representation of threatened species (77.1% of species across threatened categories are represented in TreeOfLife-200M). This coverage and the implications are discussed in greater detail in [our paper](https://doi.org/10.48550/arXiv.2505.23883).

### Source Data

TreeOfLife-200M is composed of images from the following four core data providers:

1. Global Biodiversity Information Facility ([GBIF](https://gbif.org)), which is a major biological data aggregator cataloging biodiversity data from citizen science sources (e.g., [iNaturalist](https://www.inaturalist.org/)), museum collections (e.g., from the [Smithsonian Institution](https://www.si.edu/), [Museum national d'Histoire naturelle](https://www.mnhn.fr/fr)), and camera trap collections (e.g., from the [Research Institute for Nature and Forest (INBO)](https://www.vlaanderen.be/inbo/en-gb/homepage/)). 
  - GBIF provides a [DOI](https://doi.org/10.15468/dl.bfv433) for the occurrence snapshot we downloaded (GBIF occurrence 2024-05-01 snapshot with filter `"occurrenceStatus": "PRESENT"` (DOI: https://doi.org/10.15468/dl.bfv433)). 
  - This manifest was further filtered for only `Still Images`, those with `gbifID` and `identifier`, and those not labeled as images of text documents prior to download. 
    - Note: there is only one category (`"basisOfRecord": "MATERIAL_CITATION"`) that describes images of textual documents (these are a particular type of document that describes species).
  - Further filtereing and processing steps are described below.

2. Encyclopedia of Life ([EOL](https://eol.org)): Another large biological data aggregator (greatest source of biodiversity in [TreeOfLife-10M](https://huggingface.co/datasets/imageomics/TreeOfLife-10M)). 
  - EOL does not have a versioned release like GBIF, so recreating this dataset requires use of `metadata/eol_metadata/media_manifest.csv` and `metadata/eol_metadata/taxon.tab` (this is just if one wants to reproduce our process, the provided `catalog` and `provenance` parquets are sufficient to reproduce a copy of the dataset).
    - Media manifest was downloaded from "image list URL: https://eol.org/data/media_manifest.tgz" (at [image list](https://opendata.eol.org/dataset/images-list/resource/f80f2949-ea76-4c2f-93db-05c101a2465c)). Taxonomy (`taxon.tab`) from "EOL Dynamic Hierarchy Active Version URL: https://editors.eol.org/uploaded_resources/00a/db4/dh21.zip" (at [dataset](https://opendata.eol.org/dataset/tram-807-808-809-810-dh-v1-1/resource/00adb47b-57ed-4f6b-8f66-83bfdb5120e8)).
  - Images used for the [Rare Species dataset](https://huggingface.co/datasets/imageomics/rare-species) were removed from this collection (by MD5) to avoid data leakage.
  - Further filtereing and processing steps are described below.

3. [BIOSCAN-5M](https://github.com/bioscan-ml/BIOSCAN-5M): Collection of primarily insect specimen images, hand-labeled by experts. Other Arthropoda classes account for 2% of the 5M images. 93% of the images in the dataset are _not_ labeled to the species level. 
  - This dataset was ready to use, and we followed access instructions in [their repository](https://github.com/bioscan-ml/BIOSCAN-5M?tab=readme-ov-file#dataset-access) (specifically downloading through the [Google Drive link](https://drive.google.com/drive/u/1/folders/1Jc57eKkeiYrnUBc9WlIp-ZS_L1bVlT-0)). 
  - The inclusion of this data just required aligning the taxon labels with those of the other datasets (following the [Annotation Process](#annotation-process), described below).

4. [FathomNet](https://www.fathomnet.org/): Collection of expert-annotated images of undersea creatures; this dataset focuses on a habitat instead of a clade.
  - This dataset required fetching image metadata through their [API](https://fathomnet-py.readthedocs.io/en/latest/api.html#module-fathomnet.api.images) to generate a manifest, then a second pass to fetch bounding boxes for each image.
  - From these, "concepts" were extracted and [GNVerifier](https://github.com/gnames/gnverifier) was utilized to obtain the relevant taxonomic information.
    - Extracted taxonomic information required alignment (as described in [Annotation Process](#annotation-process), below).
  - Focal species were retrieved from each image following download using [distributed-downloader](https://github.com/Imageomics/distributed-downloader). 
    - Images with multiple focal species had each extracted into its own image utilizing the bounding box annotations, hence the inclusion of a `fathom_metadata` CSV to fetch all images. The process is described, with specific instructions, in [TreeOfLife-toolbox/docs/FathomNet_download_README](https://github.com/Imageomics/TreeOfLife-toolbox/blob/main/docs/FathomNet_download_README.md).

Both BIOSCAN-5M and FathomNet were included to help improve coverage of under-represented and highly diverse branches of the tree of life (_Insecta_ is one of the most diverse classes and creatures that dwell in the ocean are much less commonly represented). 
The total number of dataset-wide taxonomic hierarchies that are _uniquely_ contributed by each core data provider is provided below, with their total number of images contributed to exemplify this point.

| Provider | Unique Taxa | Images |
| :---- | :---: |  :---: |
| GBIF | 586,898 | 203.5M |
| EOL | 48,748 | 5.3M |
| BIOSCAN-5M | 2,900 | 5.2M |
| FathomNet | 251 | 37.9K |

### Data Curation and Processing

During download (with [distributed-downloader](https://github.com/Imageomics/distributed-downloader)), each image's size is checked: first that it is sufficiently large (224 pixels or more on shortest side) and excluded if not, and then the image is resized, if necessary, so that its largest side does not exceed 720 pixels. A hash of both the original and the resized image is recorded, and the hash of the original image is compared across the dataset to avoid introducing duplicate images. The metadata is still recorded, so that no information is lost (images may be uploaded to one site with more or less information than to another).

The taxonmic alignment process, which was applied to _all_ source data, is described below in [Annotations](#annotations). The remaining processing was focused on (1) ensuring image quality and (2) eliminating duplication and data leakage, and is described below.

**1. Ensuring Image Quality**

We noted the varied [image types](#image-types-gbif-only) included in the GBIF snapshot, above. The three main types (musuem specimen, camera trap, and citizen science images) each require special filtering processes to avoid introducing noisy data. 

***Musuem specimen collections*** are often photographed with both specimens and their associated text documents (e.g., labels, folders, tags) under the same occurrence. All images under a single occurrence share metadata, there is no distinction for the subject of the image. These images of text were filtered through a nearest-centroid classifier spanning 25 fine-grained subtypes; 11 collection areas (Fungi, Insect, Invertebrate Zoology, Microbiology, Plant, Uncategorized, and five classes of Vertebrate Zoology: Amphibians, Birds, Fishes, Mammals, Others) inspired by the [Smithsonian Institution's collection categories](https://collections.nmnh.si.edu/search/), each further subdivided to classes such as preserved or fossil specimen, as labed by GBIF `basisOfRecord`. We manually curate an 8.5K set of examples on which to fit the classifier, which predicts a subtype for all museum images. All non-organismal images are then removed.

***Camera trap occurrences*** are first filtered to only those with 15 images or less. [MegaDetector](https://github.com/microsoft/CameraTraps) is then applied to each occurrence to distinguish those with animals in them from "empty" frames. We remove these to avoid labeling a creature's habitat as the creature, particularly since we are training a foundation model for the full tree of life, meaning that plants are of interest in their own right and should not be mislabeled as animals. 
  - Context: Some occurrences include large-volume camera-trap sequences, with up to 10,000 images. These occurrences have a single taxonomic label applied across all images, though there are different taxa (e.g, the first few frames had a duck, while later images have a swan, another a goose, but the label for all is a duck). In these cases, Megadetector often misclassifies empty frames or detects animals that do not match the intended taxa, leading to false positives. To reduce the risk of introducing such noise while still capturing relevant biodiversity, we filter the dataset to include only occurrences with 15 images or fewer.

Finally, images within ***citizen science occurrences*** are tested for similarity, and the mean pair-wise [BioCLIP](https://huggingface.co/imageomics/bioclip) embedding distance is used to determine whether they fall into one of three categories: (1) those that are overly distinct (this can happen when images of different species are uploaded to the same observation), (2) those that exhibit "expected" variation, and (3) those that are exceedingly similar (this can occur when images from a single camera trap are uploaded to one observation). The images in (1) are removed (bottom 5th percentile), those in (2) are retained, and those in (3) are run through the camera trap processing described above.

We run [MTCNN](https://github.com/timesler/facenet-pytorch) on all images from GBIF and EOL to detect and remove images containing identifiable human faces. BIOSCAN-5M and FathomNet Database do not have images with human faces requiring filtering.

**2. Eliminating Duplication and Data Leakage**

As noted above, MD5 hashes are taken of every image on download. This are highly sensitive, in that variation by a single pixel will result in a different hash between two images. Thus, these are used for an initial filter across all images to avoid duplication and the introduction of test set images (e.g., those from [Rare Species](https://huggingface.co/datasets/imageomics/rare-species) that were sourced from [EOL](eol.org)) into the training data. The next step is to check for test images by metadata; however, this is not always viable, as existing benchmarks do not always retain the connection to their orignal source data in a manner allowing this. We thus take perceptual [PDQ hashes](https://github.com/facebook/ThreatExchange/tree/main/pdq) of every test image and all images from GBIF and EOL (with `Medium Source URL` from Flickr--these methods are _not_ effective on museum specimen images), removing those with distance less than 10 from the training data.

The code for all of these processing steps, along with further details, is provided in [TreeOfLife-toolbox](https://github.com/Imageomics/TreeOfLife-toolbox).


### Annotations
We standardized the taxonomic labels provided by the four core data providers to conform to a uniform [7-rank Linnean](https://www.britannica.com/science/taxonomy/The-Linnaean-system) structure. 

 #### Kingdom Counts
| Kingdom | Number of Images |
| :-------------------------- | :--------: |
|Animalia                            |102591559|
|Plantae                             |101881537|
|Fungi                               |7556801  |
|Chromista                           |530234   |
|Protozoa                            |184809   |
|Bacteria                            |59109    |
|Viruses                             |8587     |
|Archaea                             |70       |

#### Annotation process

Taxonomic labels (kingdom, phylum, etc.) were standardized across the various data sources using the [`TaxonoPy` package](https://github.com/Imageomics/TaxonoPy) that we designed (in consultation with taxonomists) for this purpose. The `TaxonoPy` algorithm works to match each unique taxonomic string to the GBIF Backbone, Catalogue of Life, and OpenTree hierarchies (in that order). See [`TaxonoPy`](https://github.com/Imageomics/TaxonoPy) for more details on this process.

#### Who are the annotators?

The taxonomic labels provided by the four core data providers (GBIF, EOL, BIOSCAN-5M, and FathomNet) were fed into TaxonoPy for standardization.

### Personal and Sensitive Information

None: These images come from existing, public biodiversity data repositories, and no GPS locations for the species in the images are included. We further used [MTCNN](https://github.com/timesler/facenet-pytorch) on all images downloaded from GBIF and EOL to filter out identifiable images of people. There are no images with people in the BIOSCAN-5M or FathomNet Database to filter.


## Considerations for Using the Data

We hope this dataset (and the model trained with it) can aid in conservation efforts and biodiversity research.

### Bias, Risks, and Limitations

This dataset is imbalanced in its representation of various species with the greatest representation available for those in the phyla _Tracheophyta_, _Arthropoda_, and _Chordata_. The long-tailed distribution exhibited by taxonomic rank is to be expected working with biodiversity data, and results from both an imbalance in the availability of images and actual variance in class diversity. 
For instance, TreeOfLife-200M has a balanced representation between plants and animals (at the kingdom level), but animals represent a larger proportion of described species. Additionally, [IUCN](iucnredlist.org) estimates 2,139,242 _described_ species as of [March 2025](https://nc.iucnredlist.org/redlist/content/attachment_files/2025-1_RL_Table_1a.pdf), the vast majority of which are invertebrates. Though described invertebrates outnumber vertebrates 20 to one, more than double the number of vertebrates have been evaluated (64K vertebrates to only 29K invertebrates) due to lack of available information. 

![Graph displaying counts for most represented taxonomic classes, emphasizes imbalance](https://huggingface.co/datasets/imageomics/TreeOfLife-200M/resolve/main/visuals/taxa-class-imgs-most.png)

Overall, 89% of images have full taxonomic labels. As discussed above, most of this gap is more indicative of the lack of consensus or available granularity in labeling, rather than missing information. BIOSCAN-5M is a good example of this, as the label granularity is still limited for insects (_Insecta_, one of the most diverse classes in the tree of life). In our resolved taxa for BIOSCAN-5M, 95.97% of images are labeled to the family level but only 30.78% and 6.81% of the images have genus or species indicated, respectively. This is a persistent challenge in species identification and part of the reason that large biological foundation models trained with taxonomic hierachies are useful. We highlight these taxonomic coverage limitations for a better understanding of both the data and our motivation, but do not wish to diminish the impact of our coverage of nearly 868K unique taxa labeled to the level of species; it far surpasses the species diversity of other well-known biological datasets. 

We note also that our taxonomic resolution ([`TaxonoPy`](https://github.com/Imageomics/TaxonoPy)) resulted in less than 1% unresolved cases, e.g., `Metazoa` instead of `Animalia` or `incertae sedis` for kingdom:
| Unresolved Kingdom | Number of Images |
| :-------------------------- | :--------: |
|incertae sedis               |1060535  |
|Archaeplastida               |33923    |
|Metazoa                      |24858    |
|NULL                         |5253     |


### Recommendations

It is always important to understand the data with which one is working and take each dataset's uniqueness into account. Some considerations for TreeOfLife-200M:
 - If using this dataset as more than just a training dataset (i.e., for validation or testing) be sure to keep `source_id` distinct across splits.
   - In these circumstances, it would also good to keep in mind that this dataset has a long-tail distribution (as one would expect from biological data).
 - As noted above, there are some unresolved/misaligned kingdoms. Depending on one's use-case, these may be dropped or another attempt at re-alignment might be made (for instance with an updated version of [`TaxonoPy`](https://github.com/Imageomics/TaxonoPy), as we intend to add profiles to address these outliers).

## Licensing Information

The data (images and text) contain a variety of licensing restrictions mostly within the CC family. Each image and text in this dataset is provided under the least restrictive terms allowed by its licensing requirements as provided to us (i.e, we impose no additional restrictions past those specified by licenses in the license file).

All BIOSCAN-5M images are licensed under Creative Commons Attribution 3.0 Unported ([CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)).

FathomNet: All FathomNet images and annotations are shared under Creative Commons Attribution-Non Commercial-No Derivatives 4.0 International license ([CC BY-NC-ND](https://creativecommons.org/licenses/by-nc-nd/4.0/), more details on their [terms](https://database.fathomnet.org/fathomnet/#/license)).

EOL and GBIF images contain a variety of licenses ranging from [CC0](https://creativecommons.org/publicdomain/zero/1.0/) to [CC BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/). The [GBIF occurrence snapshot](https://doi.org/10.15468/dl.bfv433) is licensed under [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC)](https://creativecommons.org/licenses/by-nc/4.0/)

For license and citation information by image, see our [provenance file](https://huggingface.co/datasets/imageomics/TreeOfLife-200M/blob/main/metadata/provenance.parquet).

This dataset (the compilation) has been marked as dedicated to the public domain by applying the [CC0 Public Domain Waiver](https://creativecommons.org/publicdomain/zero/1.0/). However, images are often licensed under different terms (as noted above).


## Citation
If you use this dataset in your research, please cite both it and our associated paper, as well as the constituent datasets (source data providers).

**BibTeX:**

**Data**
```
@dataset{treeoflife_200m,
  title = {{T}ree{O}f{L}ife-200{M} (Revision a8f38b4)}, 
  author = {Jianyang Gu and Samuel Stevens and Elizabeth G Campolongo and Matthew J Thompson and Net Zhang and Jiaman Wu and Andrei Kopanev and Zheda Mai and Alexander E. White and James Balhoff and Wasila M Dahdul and Daniel Rubenstein and Hilmar Lapp and Tanya Berger-Wolf and Wei-Lun Chao and Yu Su},
  year = {2025},
  url = {https://huggingface.co/datasets/imageomics/TreeOfLife-200M},
  doi = {10.57967/hf/6786},
  publisher = {Hugging Face}
}
```

Please also cite our paper:

```
@article{gu2025bioclip,
  title = {{B}io{CLIP} 2: Emergent Properties from Scaling Hierarchical Contrastive Learning}, 
  author = {Jianyang Gu and Samuel Stevens and Elizabeth G Campolongo and Matthew J Thompson and Net Zhang and Jiaman Wu and Andrei Kopanev and Zheda Mai and Alexander E. White and James Balhoff and Wasila M Dahdul and Daniel Rubenstein and Hilmar Lapp and Tanya Berger-Wolf and Wei-Lun Chao and Yu Su},
  year = {2025},
  eprint={2505.23883},
  archivePrefix={arXiv},
  primaryClass={cs.CV},
  url={https://arxiv.org/abs/2505.23883},
}
```

Please be sure to also cite the original data sources and all constituent parts as appropriate.

### Source Data Providers

**GBIF:**
```
@misc{GBIF-DOI,
  doi = {10.15468/DL.BFV433},
  url = {https://doi.org/10.15468/dl.bfv433},
  keywords = {GBIF, biodiversity, species occurrences},
  author = {GBIF.org},
  title = {{GBIF} Occurrence Download},
  publisher = {The Global Biodiversity Information Facility},
  month = {May},
  year = {2024},
  copyright = {Creative Commons Attribution Non Commercial 4.0 International}
}
```

**EOL:** 
```
@misc{eol,
    author = {{Encyclopedia of Life (EOL)}},
    url = {https://eol.org},
    note = {Accessed August 2024}
}
```

**BIOSCAN-5M:**
```
@inproceedings{gharaee2024bioscan5m,
    title={{BIOSCAN-5M}: A Multimodal Dataset for Insect Biodiversity},
    booktitle={Advances in Neural Information Processing Systems},
    author={Zahra Gharaee and Scott C. Lowe and ZeMing Gong and Pablo Millan Arias
        and Nicholas Pellegrino and Austin T. Wang and Joakim Bruslund Haurum
        and Iuliia Zarubiieva and Lila Kari and Dirk Steinke and Graham W. Taylor
        and Paul Fieguth and Angel X. Chang
    },
    editor={A. Globerson and L. Mackey and D. Belgrave and A. Fan and U. Paquet and J. Tomczak and C. Zhang},
    pages={36285--36313},
    publisher={Curran Associates, Inc.},
    year={2024},
    volume={37},
    url={https://proceedings.neurips.cc/paper_files/paper/2024/file/3fdbb472813041c9ecef04c20c2b1e5a-Paper-Datasets_and_Benchmarks_Track.pdf},
}
```

**FathomNet:**
```
@article{katija_fathomnet_2022,
	title = {{FathomNet}: {A} global image database for enabling artificial intelligence in the ocean},
	volume = {12},
	issn = {2045-2322},
	shorttitle = {{FathomNet}},
	url = {https://www.nature.com/articles/s41598-022-19939-2},
	doi = {10.1038/s41598-022-19939-2},
	number = {1},
	urldate = {2025-05-13},
	journal = {Scientific Reports},
	author = {Katija, Kakani and Orenstein, Eric and Schlining, Brian and Lundsten, Lonny and Barnard, Kevin and Sainz, Giovanna and Boulais, Oceane and Cromwell, Megan and Butler, Erin and Woodward, Benjamin and Bell, Katherine L. C.},
	month = sep,
	year = {2022},
	pages = {15914},
}
```

For license and citation information by image, see our [provenance file](https://huggingface.co/datasets/imageomics/TreeOfLife-200M/blob/main/dataset/metadata/provenance.parquet).


## Acknowledgements

We would like to thank Zhiyuan Tao, Shuheng Wang, Ziheng Zhang, Zhongwei Wang, and Leanna House for their help with the TreeOfLife-200M dataset, Charles (Chuck) Stewart, Sara Beery, and other [Imageomics Team](https://imageomics.osu.edu/about/team) members for their constructive feedback and Sergiu Sanielevici, Tom Maiden, and TJ Olesky for their dedicated assistance with arranging the necessary computational resources.

We are grateful to Kakani Katija and Dirk Steinke for helpful conversations regarding use and integration of FathomNet and BIOSCAN-5M, respectively, as well as Stephen Formel and Markus Döring for GBIF. We thank Marie Grosjean for comparative methods for filtering citizen science images and Dylan Verheul for assistance with acquiring images from Observation.org from GBIF. We thank Suren Byna for a helpful conversation on early dataset design decisions. We thank Doug Johnson for his collaboration in hosting this large dataset on the Ohio Supercomputer Center research storage file system.

This work was supported by the [Imageomics Institute](https://imageomics.org), which is funded by the US National Science Foundation's Harnessing the Data Revolution (HDR) program under [Award #2118240](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2118240) (Imageomics: A New Frontier of Biological Information Powered by Knowledge-Guided Machine Learning).

Our research is also supported by resources from the [Ohio Supercomputer Center](https://ror.org/01apna436).

Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.


## Dataset Card Authors 

Elizabeth G. Campolongo
