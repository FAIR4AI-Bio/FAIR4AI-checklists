---
license: cc-by-4.0
language:
- en
- la
pretty_name: "Beetles as Sentinel Taxa: Predicting drought conditions from NEON specimen imagery"
task_categories:
- image-feature-extraction
dataset_info:
  features:
  - name: file_path
    dtype: image
  - name: colorpicker_full_path
    dtype: image
  - name: scalebar_full_path
    dtype: image
  - name: SPEI_1y
    dtype: float64
  - name: SPEI_2y
    dtype: float64
  - name: SPEI_30d
    dtype: float64
  - name: public_id
    dtype: string
  - name: eventID
    dtype: int64
  - name: domainID
    dtype: int64
  - name: scientificName
    dtype: string
  - name: siteID
    dtype: string
  - name: collectDate
    dtype: string
  - name: relative_img_loc
    dtype: string
  - name: colorpicker_path
    dtype: string
  - name: scalebar_path
    dtype: string
  splits:
  - name: train
    num_bytes: 14289671472.3
    num_examples: 22370
  - name: validation
    num_bytes: 1742043556.572
    num_examples: 2486
  download_size: 15078112217
  dataset_size: 16031715028.872
tags:
- biology
- image
- animals
- CV
- beetles
- specimen
- ecology
- climate
- spei
- drought
- ml-challenge
- imageomics
- NEON
size_categories: 10K<n<100K
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
  - split: validation
    path: data/validation-*
description: "Images of pinned carabid beetle specimens collected by the National Ecological Observatory Network (NEON) from ecological sites across the U.S., along with associated metadata and drought severity indices (Standardized Precipitation Evapotranspiration Index (SPEI)). It was developed to for the second HDR ML Challenge, and is intended to support the development of machine learning models to predict environmental conditions&mdash;specifically drought status&mdash;from organismal traits captured in specimen imagery."
---


<!--
Image with caption (jpg or png):
|![Figure #](https://huggingface.co/datasets/imageomics/<data-repo>/resolve/main/<filepath>)|
|:--|
|**Figure #.** [Image of <>](https://huggingface.co/datasets/imageomics/<data-repo>/raw/main/<filepath>) <caption description>.|
-->

<!--
Notes on styling:

To render LaTex in your README, wrap the code in `\\(` and `\\)`. Example: \\(\frac{1}{2}\\)

Escape underscores ("_") with a "\". Example: image\_RGB
-->

# Dataset Card for Beetles as Sentinel Taxa: Predicting drought conditions from NEON specimen imagery

This dataset contains images of pinned carabid beetle specimens collected by the [National Ecological Observatory Network (NEON)](https://www.neonscience.org/) from ecological sites across the U.S., along with associated metadata and drought severity indices ([Standardized Precipitation Evapotranspiration Index (SPEI)](https://spei.csic.es/)). It was developed to for the [second HDR ML Challenge](https://www.nsfhdr.org/mlchallenge-y2), and is intended to support the development of machine learning models to predict environmental conditions—specifically drought status—from organismal traits captured in specimen imagery. 

## Dataset Details

### Dataset Description

- **Curated by:**  
    - Alyson East, University of Maine, Orono, ME, USA
    - Michael Belitz, Michigan State University, East Lansing, MI, USA
    - Leah Cotton, Arizona State University, Tempe, AZ, USA
    - Jacqueline Dominguez, Arizona State University, Tempe, AZ, USA
    - Isabelle Betancourt, National Ecological Observatory Network (NEON), Tempe, AZ, USA
    - S M Rayeed, Rensselaer Polytechnic Institute, Troy, NY, USA
    - Fangxun Liu, The Ohio State University, Columbus, OH, USA
    - David Carlyn, The Ohio State University, Columbus, OH, USA
    - Connor Kilrain, The Ohio State University, Columbus, OH, USA
    - Jiaman Wu, The Ohio State University, Columbus, OH, USA
    - Chandra Earl, National Ecological Observatory Network (NEON), Tempe, AZ, USA
    - Hilmar Lapp, Duke University, Durham, NC, USA
    - Kayla I. Perry, The Ohio State University, Wooster, OH, USA
    - Matthew J. Thompson, The Ohio State University, Columbus, OH, USA
    - Elizabeth G. Campolongo, The Ohio State University, Columbus, OH, USA
    - Wei-Lun Chao, The Ohio State University, Columbus, OH, USA
    - Eric R. Sokol, National Ecological Observatory Network (NEON), Boulder, CO, USA
    - Sydne Record, University of Maine, Orono, ME, USA
- **Homepage:** https://www.nsfhdr.org/mlchallenge-y2
- **Repository:** https://github.com/Imageomics/HDR-SMood-Challenge
<!-- - **Paper:**  TBD -->

This dataset contains high-resolution images and metadata for pinned specimens of carabid beetles collected across U.S. ecosystems by the [National Ecological Observatory Network (NEON)](https://www.neonscience.org/). Each image is linked to specimen-level metadata (e.g., collection date, site, taxonomic identification) and environmental context, including drought severity indicators ([Standardized Precipitation Evapotranspiration Index (SPEI)](https://spei.csic.es/)) calculated over multiple timescales using remote sensing data. This dataset is designed to support research on the relationship between ecological traits and climate stress, and is intended for training and evaluating machine learning models that predict environmental conditions-particularly drought status—from biological imagery. It was created for the Imageomics portion of the [second HDR ML Challenge](https://www.nsfhdr.org/mlchallenge-y2), which emphasizes model generalization across sites with different climates, land cover types, and beetle species pools. Not all available information is provided as part of the challenge, but it will be added at the end of the challenge to allow for broader use beyond the challenge. This includes smaller beetles, which were entirely excluded from the challenge, but will be added to this dataset later.

### Supported Tasks and Leaderboards

Leaderboard is available on the [Codabench Challenge page](https://www.codabench.org/competitions/9854#/results-tab).

## Dataset Structure

<!-- This section provides a description of the dataset fields, and additional information about the dataset structure such as criteria used to create the splits, relationships between data points, etc. -->

```
/dataset/
    color_and_scale_images/
        colorpicker_<colorpicker_id 1>.png
        colorpicker_<colorpicker_id 2>.png
        ...
        colorpicker_<colorpicker_id k>.png
        scalebar_<scalebarid 1>.png
        scalebar_<scalebarid 2>.png
        ...
        scalebar_<scalebarid k>.png
    data/
        train-00000-of-00029.parquet
        train-00001-of-00029.parquet
        ...
        train-00028-of-00029.parquet
        validation-00000-of-00004.parquet
        ...
        validation-00003-of-00004.parquet
    flattened_images/
        <img_id 1>.png
        <img_id 2>.png
        ...
        <img_id n>.png
    train.csv
    val.csv
```

### Data Instances

Each record in `train.csv` or `val.csv` corresponds to a single pinned carabid beetle specimen collected by [NEON](https://www.neonscience.org/) staff as part of the "Ground beetles sampled from pitfall traps" data product ([DP1.10022.001](https://data.neonscience.org/data-products/DP1.10022.001)). There are a maximum of 13 field season collection bouts per year, with carabids collected from no more than 10 plotIDs per bout. For data collected prior to 2018, each plot will yield no more than 4 samples per bout of collection, resulting in a maximum of 520 plot‐bouts per site per year. For collections 2018 and later, each plot yields a maximum of 3 samples within each bout. The number of individuals identified varies with the abundance of organisms at the site. Beetles were imaged in the trays in which they were pinned, which correspond to their taxonomic designations; individuals were cropped from the group images, and saved in `flatten_images/`. As a result of this imaging process, each color palette and scalebar image corresponds to more than one beetle image (alignment is described below).

Metadata include an identifier for a collection event (`eventID`), the date of the collection event (`collectDate`), an anonymized identifier of the domain (`domainID`) and site (`siteID`) where the collection event took place, taxonomic information (`scientificName`), unique beetle image identifier (`public_id`), a link to the beetle image file (`relative_img_loc`), a link to the color palette image (`colorpicker_path`), a link to the scale image (`scalebar_path`), and Standardized Precipication Evapotranspiratoin Index (SPEI) values that correspond with the location and time that the specimen was collected. The SPEI values were calculated for the 30 day (`SPEI_30d`), 1 year (`SPEI_1y`), and 2 year (`SPEI_2y`) time windows preceding the time of collection at each location for each beetle specimen in the dataset. 

The `train.csv` and `val.csv` files are to be used for training models for submission and reflect the information that will be given during testing sans `siteID`, `collectDate`, and the target variables `SPEI_30d`, `SPEI_1y`, and `SPEI_2y`. Please see the [challenge sample repository](https://github.com/Imageomics/HDR-SMood-Challenge-sample) for an example of how these were used in training the baseline submission.

The `data/` folder contains the dataset in parquet format, where `train` prefix indicates it corresponds to the images and metadata in `train.csv`, while `validation` corresponds to `val.csv`. These are rendered by the dataset viewer.

### Data Fields

Both `train.csv` and `val.csv` have the following columns.
| fieldName | description | dataType | relatedTerms |
|---|---|---|---|
| eventID | An (anonymized) identifier for the set of information associated with the event, which includes information about the place and time of the event | string | [DWC_v2009-04-24:eventID](http://rs.tdwg.org/dwc/terms/history/index.htm#eventID-2009-04-24)
| collectDate | Date of the collection event | dateTime | [DWC_v2009-04-24:eventDate](http://rs.tdwg.org/dwc/terms/history/index.htm#eventDate-2009-04-24)
| domainID | Unique identifier (anonymized) of the NEON domain | string | [DWC_v2009-04-24:locationID](http://rs.tdwg.org/dwc/terms/history/index.htm#locationID-2009-04-24)
| siteID | NEON site code (anonymized), each domain has 1-3 sites | string | [DWC_v2009-04-24:locationID](http://rs.tdwg.org/dwc/terms/history/index.htm#locationID-2009-04-24)
| scientificName | Scientific name, associated with the taxonID. This is the name of the lowest level taxonomic rank that can be determined | string | [DWC_v2009-04-24:scientificName](http://tdwg.github.io/dwc/terms/history/index.htm#scientificName-2009-09-21)
| public_id | Unique identifier for each beetle image | string  | |
| relative_img_loc | Beetle image location within the beetle images folder (flattened_images) | string | |
| colorpicker_path | Color card image location within the color card and scale images folder (color_and_scale_images) | string | |
| scalebar_path | Scale image location within the color card and scale images folder (color_and_scale_images) | string | |
| SPEI_30d | Target variable: SPEI calculated over a short timescale (1 month), reflecting short-term moisture conditions. | real | |
| SPEI_1y | Target variable: SPEI calculated over a medium timescale (1 year), reflecting seasonal precipitation patterns. | real | |
| SPEI_2y | Target variable: SPEI calculated over a long timescale (2 years), reflecting long-term hydrological conditions. | real | |



### Data Splits

| ![fictional map to visualize the data splits as described below (there are 1-3 sites per domain, where each domain represents a region that is reasonably climactically consistent)](https://huggingface.co/datasets/imageomics/sentinel-beetles/resolve/main/figures/fictional_map.png)|
|:--|
|**Figure 1.** Fictional depiction of data distribution and splits across domains. _Image was created with Microsoft CoPilot + manual editing_.|

Using the image above as a guide, the data has been split in the following way:

#### In-distribution v. Out-of-distribution
All domains were split into two sets: one for out-of-distribution (OOD) testing (see domains with purple sites) and one for in-distribution (ID) testing and training (see domains with blue and/or pink sites). Each domain represents a different region, so the OOD set may contain beetle species unique to that region not found in the ID set. 

#### Training v. Testing (ID)
All domains contain up to three sites where collection events of beetles took place. Each collection event is defined by when it took place (`collectDate`) and where (`siteID`). All ID domains were split based on their sites into training and testing (ID). If a domain only contained one site, then all events from that site were placed in training. If a domain contained more than one, then one site was held out for testing (ID) and all others were placed in training.

#### Training v. Validation
During our preliminary experiments we extract a validation set out of the training set for early stopping in training. This split is what is made publicly available in the `train.csv` and `val.csv` files for training and validation respectively.

#### Initial phase v. Challenge phase

The testing sets currently contain two subsets: an ID set (images from sites whose domain was seen in training), and an OOD set which has images from domains unique to the test set. Both the ID and OOD sets were split in half for the two phases of our competition. The initial (development) phase of the competition will evaluate all submitted models on one half only. These will be represented by the private files `seen_domain.csv` and `unseen_domain.csv` for ID and OOD, respectively. Around the end of the competition, we will also evaluate all submitted models on the other half, which is contained in the private files `seen_domain_challenge.csv` and `seen_domain_challenge.csv`.

The most metadata will be provided for the training dataset; `siteID`, `collectDate` and the target variables values will be redacted for the challenge dataset. Only images and unredacted metadata will be provided. The challenge will be to recover the target variable values for given collections of beetle images from given site-date combinations. All data will be released at the end of the challenge.

## Dataset Creation

### Curation Rationale
<!-- Motivation for the creation of this dataset. For instance, what you intended to study and why that required curation of a new dataset (or if it's newly collected data and why the data was collected (intended use)), etc. -->

Climate change is increasing the frequency and severity of drought events globally, posing significant threats to ecosystems, agriculture, water resources, and human societies (IPCC, 2022). Effective monitoring and prediction of drought conditions are crucial for mitigation and adaptation strategies. While traditional drought monitoring relies on meteorological and hydrological data, ecological indicators can provide complementary insights into ecologically significant on-the-ground impacts of water stress.
Insects, particularly ground beetles (Coleoptera: Carabidae), are well-established bioindicators due to their sensitivity to environmental changes (including moisture availability), high diversity, and relative ease of sampling (Lövei and Sunderland 1996; Rainio & Niemelä, 2003). This widespread beetle family has been used to evaluate changes in landscape and local environmental conditions following natural and anthropogenic disturbances, including climate change (Muller-Kroehling et al. 2014; Qiu et al. 2023) and drought (Weiss et al. 2024a,b). While responses to these disturbances can be captured by changes in their abundance and composition, morphological and ecological traits are increasingly used to characterize communities because they give insight into why species respond to change (Cadotte et al. 2015; Fountain-Jones et al. 2015; Moretti et al. 2017).

The National Ecological Observatory Network (NEON) provides unprecedented, standardized ecological data across the United States, including systematic collections of carabid beetles from diverse terrestrial ecosystems (Thorpe et al., 2016). These collections, housed in the NEON Biorepository, include high-resolution images of individual specimens. This dataset was curated for the Imageomics sub-challenge of the [Second HDR ML Challenge](https://www.nsfhdr.org/mlchallenge-y2) in partnership with NEON to leverage this unique resource for exploration of a novel approach to environmental monitoring. We hope that it will further serve the community for research beyond the challenge as well.

**Impact:** This challenge aims to:
- Develop novel AI/ML methods to detect ecologically significant drought from imagery data of a sentinel taxon (carabid beetles).
- Assess the potential of carabid beetles as fine-grained indicators of drought stress across different ecosystems and timescales.
- Promote the use of NEON data and stimulate interdisciplinary research between ecology, climate science, and machine learning.
- Contribute insights relevant to water resource management, agricultural planning, and biodiversity conservation under changing climate conditions.

**Novelty:** This competition presents several novel aspects:  
- **Image-based Environmental Prediction:** It moves beyond traditional species counts or abundance data, tasking participants with extracting ecologically relevant signals directly from images of preserved specimens to predict a key environmental variable (drought).
- **Phenotypic Trait Signal:** We hypothesize that subtle variations in beetle morphology (e.g., body size variation within or among species, fluctuating asymmetry as indicators of stress) captured in images may correlate with environmental conditions like drought (Orzack & Sober, 1994). This challenge encourages models that implicitly or explicitly learn these trait-environment linkages.
- **Out-of-Sample Generalization (Transferability):** A core novelty and challenge is testing model transferability. Models will be trained on data from specific NEON sites/biomes and tested on sites with distinct ecological characteristics and potentially different species pools. This directly addresses a critical question in ecological modeling and AI: can models generalize predictions to novel environments?
- **Multi-Timescale Drought Response:** By targeting the Standardized Precipitation Evapotranspiration Index (SPEI) calculated over short (30 day), medium (1 year), and long (2 year) timescales, the challenge will provide insights into which aspects of drought (e.g., short-term soil moisture deficits vs. long-term hydrological drought) are most strongly reflected in beetle communities and potentially their morphology, and over what timescales these ecological responses are most pronounced.

### Source Data

This dataset consists of images of _pinned_ carabid beetle specimens taken in 2025 at the NEON Biorepository by two interns (Leah Cotton and Jacqueline Dominguez). A subset of these images were taken at an earlier date by Michael Belitz, who provided his images for inclusion in this dataset. The interns were trained by Alyson East and supervised by both her and Isabelle Betancourt.


**IMPORTANT:** Only a subset of the specimens that are collected on a given plot-date combination are pinned. All taxa for which there are fewer than 10 individuals on a given plot-date are pinned. If there are 10 or more individuals on a particular plot-date combination, then the specimens are placed in bulk storage (not pinned) and not available for imaging (for the purposes of this project). Furthermore, this release of the data is not a representative sample of community or body size distributions (small beetles are specifically missing from this dataset due to imaging timeline and technical constraints).


#### Data Collection and Processing

**Specimen collection:**  
NEON beetle specimens were collected using pitfall traps—16 oz deli containers filled with 150 mL or 250 mL of propylene glycol. Three traps were deployed at 10 distributed base plots per site for two-week periods throughout the growing season. Traps were positioned at the East, West, and South edges of the plots (20 meters from center). After field collection, arthropod samples were sorted in the lab. Carabid beetles were identified to species where possible. A subset of these were pinned or pointed, and from those, some were forwarded for taxonomic review or DNA barcoding. Beetles are pinned in trays, and organized into these trays based on the taxonomic labeling, species identification, domain ID, and collection year. There are known instances of errors in tray organization where there are multiple species, years. or domains in one tray. Thus, inclusion in the same tray is usually, but not always indicative of matching taxonomy, collection year, or domain. Theses errors are corrected in the individual metadata records.

**Imaging workflow:** 

|![fictional drawer containing beetles of the same species, a color calibration card, and a scale. The beetles may be collected from separate events.](https://huggingface.co/datasets/imageomics/sentinel-beetles/resolve/main/figures/fictional_beetle_tray.png)|
|:--|
|**Figure 2.** Artificial depiction of a drawer containing one species of beetles with a color calibration card and a scalebar. _Image was created with Microsoft CoPilot + manual editing_. |


Beetles were imaged in bulk (by tray) with a color palette and scalebar included in the image for later standardization. As noted above, beetles from different events may be in the same trays and same event in different trays based on labeling, so use the `colorpicker_path` and `scalbar_path` indicators to ensure proper alignment. The scalebars were placed at the same height as the pinned specimens in the tray to ensure consistent distance from the camera.

Pinned beetle specimens were photographed using high-resolution cameras to capture full museum trays containing multiple specimens. Individual specimen images were extracted from these tray photos using a custom image processing pipeline based on object detection and instance cropping. This pipeline detects and isolates each beetle image with its bounding region, standardizes its dimensions, and assigns the associated sample ID (`public_id` in this dataset). The processing workflow and code are available at: [https://github.com/Imageomics/CarabidImaging](https://github.com/Imageomics/CarabidImaging) (**NOTE:** this repository will be made publicly available at the end of the challenge, since it contains information relating to the test data). Each extracted image was then linked to the individual metadata provided by the Biorepository.

**Metadata extraction:**  
Metadata for imaged specimens (filtered by `sampleID`) were downloaded using the [`neonUtilities` R package](https://cran.r-project.org/web/packages/neonUtilities/index.html) from the NEON data portal. These records include collection details, site codes, specimen identifiers, taxonomy, and geospatial context. Note that this information is intentionally ***excluded*** from or ***anonymized*** in the challenge data, but will be added back following the completion of the challenge.

**Drought variable processing:**  
SPEI (Standardized Precipitation Evapotranspiration Index) values were queried from the [GRIDMET Drought image collection](https://developers.google.com/earth-engine/datasets/catalog/GRIDMET_DROUGHT#description) using Google Earth Engine. These data were exported as tables and merged with specimen metadata by site coordinates and collection date. SPEI values represent conditions over three time windows: 30 days (short-term), 1 year (seasonal), and 2 years (long-term). GRIDMET pixel resolution is ~4 km × 4 km. For details, see Abatzoglou ([2012](https://doi.org/10.1002/joc.3413)).

**Site-level metadata:**  
NEON site metadata was retrieved on June 25, 2025 from NEON’s public [API](https://data.neonscience.org/data-api/) and exported via their field site metadata download: [NEON_Field_Site_Metadata_20250625](https://www.neonscience.org/field-sites/exports/NEON_Field_Site_Metadata_20250625). It represents a flattened subset of the full JSON objects returned by the API endpoint ([https://data.neonscience.org/api/v0/locations/sites](https://data.neonscience.org/api/v0/locations/sites)).


#### Who are the source data producers?

These metadata records correspond with specimens collected by [NEON](https://www.neonscience.org/) staff for the "Ground beetles sampled from pitfall traps" data product ([DP1.10022.001](https://data.neonscience.org/data-products/DP1.10022.001)), which are housed at the [NEON Biorepository](https://biorepo.neonscience.org/portal/).

The SPEI values were queried from the [GRIDMET Drought image collection](https://developers.google.com/earth-engine/datasets/catalog/GRIDMET_DROUGHT#description) for each NEON terrestrial site. Note the spatial resolution of pixels in the GRIDMET data product is spatial resolution of ~ 4 km x 4 km (16 km^2). See Abatzoglou ([2012](https://doi.org/10.1002/joc.3413)) for more details about this dataset.

Images were taken by interns Leah Cotton and Jacqueline Dominguez, under the direction of Alyson East and Isabelle Betancourt. A subset of these images were also taken by Michael Belitz with a Canon EOS Rebel T7.

### Annotations

All beetle metadata was provided by the NEON Biorepository. Taxonomic labels were provided by a mix of experts (museum curator with taxonomic expertise) and parataxonomists (domain field scientist).

### Personal and Sensitive Information

This dataset may include records of rare, threatened, or endangered carabid beetle species. To comply with local, state, and federal conservation laws and data sensitivity policies, scientific names for certain protected taxa have been intentionally obfuscated or generalized in the metadata (i.e., the genus may be provided without the species epithet). These measures are intended to reduce the risk of over-collection, disturbance, or exploitation of sensitive species or habitats. Users should be aware that species-level identifications may be incomplete or masked for specimens collected in jurisdictions where such protections are enforced.

## Considerations for Using the Data

This is a training dataset for an [ML Challenge](https://www.codabench.org/competitions/9854), whose goal is to recover SPEI values at the spatial resolution of a NEON site. The SPEI values are derived from remote sensing data and have a spatial resolution of ~ 4 x 4 km (16 km^2), which is similar in scale to the area of an entire NEON site. Individual beetles are collected from traps placed along 40 x 40 m plots arranged throughout the NEON site, stratified to represent the relative dominance of the available [National Land Cover Database (NLCD)](https://www.usgs.gov/centers/eros/science/national-land-cover-database) types at the site. In the metadata, individual beetle specimen records are mapped to the corresponding site-level information form a sampling event. Thus, the geospatial data correspond with the larger NEON site, and not the exact location at which the beetle specimen was collected. For this challenge, it is hypothesized that emergent properties of the beetle community at a site will be correlated with the site drought status. 


### Bias, Risks, and Limitations

This release of the data is not a representative sample of community or body size distributions for their sites. This dataset consists only of pinned specimens from the NEON Biorepository that were sufficiently large to not require adjustments within their boxes. Smaller beetles will be added at a later date, though they will not be included in the challenge.

Furthermore, as mentioned above, only a subset of beetle specimens that are collected during a sampling event are imaged, and included in this dataset. If common taxa have high abundances for a given plot-date (a pooled set of traps from the same plot-date), they are archived in bulk storage and not available to be imaged. Thus, very abundant taxa are not included in this dataset for plot-dates for which their counts were 10 or more. 
<!--  only taxa for which there are fewer than 10 individuals collected on a given plot-date are pinned.  Bulk specimens (those for which more than 10 individuals of the species were collected on a given plot-date) have not been imaged, and are unlikely to be in this context.
-->

### Recommendations

In its current form, this dataset is intended only for use as the training dataset in the [Beetles as Sentinel Taxa Scientific-Mood ML Challenge](https://www.codabench.org/competitions/9854). More detailed environmental data has been excluded and crucial identifiers have been anonymized for the challenge. After the challenge, this information will be added to the dataset so that it may be used for further scientific endeavors. We recommend waiting until this dataset has been updated with the full information to use it for anything beyond the [ML Challenge](https://www.nsfhdr.org/mlchallenge-y2).

## Licensing Information

[CC BY (Attribution)](https://creativecommons.org/licenses/by/4.0/)

**You are free to:**
- Share — copy and redistribute the material in any medium or format for any purpose, even commercially.
- Adapt — remix, transform, and build upon the material for any purpose, even commercially.
The licensor cannot revoke these freedoms as long as you follow the license terms.

**Under the following terms:**
- Attribution — You must give appropriate credit , provide a link to the license, and indicate if changes were made . You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

**Notices:**

You do not have to comply with the license for elements of the material in the public domain or where your use is permitted by an applicable exception or limitation.

No warranties are given. The license may not give you all of the permissions necessary for your intended use. For example, other rights such as publicity, privacy, or moral rights may limit how you use the material.

## Citation

**BibTeX:**

**Data**
```
@misc{East-beetles-2025,
  author = {Alyson East and Michael Belitz and Leah Cotton and Jacqueline Dominguez and Isabelle Betancourt and 
    S M Rayeed and Fangxun Liu and David Carlyn and Connor Kilrain and Jiaman Wu and Chandra Earl and Hilmar Lapp 
    and Kayla I. Perry and Charles Stewart and Matthew J. Thompson and Elizabeth G. Campolongo and Wei-Lun Chao and
    Eric R. Sokol and Sydne Record},
  title = {Beetles as Sentinel Taxa: Predicting drought conditions from {NEON} specimen imagery},
  year = {2025},
  url = {https://huggingface.co/datasets/imageomics/sentinel-beetles},
  doi = {<doi once generated>},
  publisher = {Hugging Face}
}
```

<!--
-for an associated paper:
**Paper**
```
@article{<ref_code>,
  title    = {<title>},
  author   = {<author1 and author2>},
  journal  = {<journal_name>},
  year     =  <year>,
  url      = {<DOI_URL>},
  doi      = {<DOI>}
}
```
-->


Please be sure to also cite the original data sources (specimen collection and metadata) and include the NEON acknowledgements (provided below).

```bibtex
@misc{NEON-pinned-beetles,
  doi = {10.48443/CD21-Q875},
  url = {https://data.neonscience.org/data-products/DP1.10022.001/RELEASE-2025},
  author = {{National Ecological Observatory Network (NEON)}},
  keywords = {diversity, taxonomy, community composition, species composition, population, invertebrates, abundance, beetles, Carabidae, insects, DNA sequences, COI, DNA barcoding, ground beetles, pitfall traps, material samples, archived samples, bet, introduced species, invasive species, native species, biodiversity},
  language = {en},
  title = {Ground beetles sampled from pitfall traps (DP1.10022.001)},
  publisher = {National Ecological Observatory Network (NEON)},
  year = {2025}
}
```

```bibtex
@misc{NEON-field-metadata,
  url = {https://www.neonscience.org/field-sites/exports/NEON_Field_Site_Metadata_20250625},
  author = {{National Ecological Observatory Network (NEON)}},
  language = {en},
  title = {{NEON} Field Site Metadata},
  publisher = {National Ecological Observatory Network (NEON)},
  year = {2025},
  note = {Dataset accessed from https://data.neonscience.org/api/v0/locations/sites on June 25, 2025}
}
```

## Acknowledgements

This work was supported by the [Imageomics Institute](https://imageomics.org), which is funded by the US National Science Foundation's Harnessing the Data Revolution (HDR) program under [Award #2118240](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2118240) (Imageomics: A New Frontier of Biological Information Powered by Knowledge-Guided Machine Learning). This material is based in part upon work supported by the National Ecological Observatory Network ([NEON](https://www.neonscience.org/)), a program sponsored by the U.S. National Science Foundation (NSF) and operated under cooperative agreement by Battelle.

S. Record and A. East were additionally supported by the US National Science Foundation's [Award No. 242918](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2429418&HistoricalAwards=false) and by Hatch project Award #MEO-022425 from the US Department of Agriculture’s National Institute of Food and Agriculture. M. Belitz was additionally supported by the US National Science Foundation's [Award #2410152](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2410152&HistoricalAwards=false).

Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation or US Department of Agriculture. 

<!-- 
## Glossary 

[optional] If relevant, include terms and calculations in this section that can help readers understand the dataset or dataset card. -->

## More Information 

The HDR ML Challenge program is hosting its second FAIR challenge, this year presenting three scientific benchmarks for modeling out of distribution in three critical areas: Neural Forecasting, Climate Prediction using Ecological Data, and Coastal Flooding Prediction over time. This dataset is one of those three challenges and has been created in a collaboration between the Imageomics Institute and NEON.

## Dataset Card Authors 

- Eric R. Sokol (esokol@battelleecology.org)
- Chandra Earl (chandra.earl@asu.edu)
- David Carlyn (carlyn.1@osu.edu)
- Elizabeth G. Campolongo

## Dataset Card Contact

We encourage those with questions regarding the dataset to open a discussion in the [Community tab](https://huggingface.co/datasets/imageomics/sentinel-beetles/discussions).