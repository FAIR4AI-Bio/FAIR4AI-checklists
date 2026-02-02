---
license: cc0-1.0
language:
- en
pretty_name: KABR Behavior Telemetry - FAIR² Drone Wildlife Monitoring Dataset

task_categories:
  - object-detection
  - video-classification

tags:
  - biology
  - ecology
  - wildlife-monitoring
  - drone
  - uav
  - aerial-imagery
  - animal-behavior
  - zebra
  - giraffe
  - kenya
  - savanna

size_categories:
  - 100K<n<1M

description: Frame-level behavior telemetry dataset combining drone GPS tracks, camera metadata, animal detections, and behavior annotations from wildlife monitoring in Kenya. Supports detection, tracking, and behavioral analysis research.

# FAIR² COMPLIANCE METADATA
fair2_compliance:
  findable:
    doi: ""  # To be assigned
    metadata_registry: ["DataCite", "GBIF"]
  accessible:
    open_access: true
    authentication_required: false
  interoperable:
    standards: ["Darwin Core", "TDWG", "Humboldt Eco", "FAIR2"]
  reusable:
    license_clear: true
    provenance_documented: true
  ai_ready:
    machine_readable: true
    structured_annotations: true

# DARWIN CORE COMPLIANCE
darwin_core:
  event_coverage:
    start_date: "2023-01-11"
    end_date: "2023-01-17"
    decimal_latitude: 0.36
    decimal_longitude: 36.88
    coordinate_uncertainty_meters: 10
    locality: "Mpala Research Centre, Laikipia County, Kenya"
    habitat: "Open savanna and bushy woodland"

  occurrence_info:
    kingdom: "Animalia"
    taxa_included: ["Equus grevyi", "Equus quagga", "Giraffa reticulata"]
    sampling_protocol: "Aerial drone video survey at 20-50m altitude with continuous recording and frame-by-frame behavior annotation"

# PLATFORM SPECIFICATIONS
platform:
  type: "UAV"
  manufacturer: "DJI"
  model: "Mavic Air 2, DJI Mini"
  autonomy_mode: "manual"

# SENSOR SPECIFICATIONS
sensors:
  - type: "RGB"
    manufacturer: "DJI"
    model: "Integrated camera"
    resolution: [5472, 3078]

# MISSION PARAMETERS
mission:
  altitude_m: 35
  speed_ms: 3
  telemetry_available: true
---

# Dataset Card for KABR Behavior Telemetry

**Synchronized frame-level telemetry, detections, and behavior annotations from drone wildlife monitoring in Kenya, enabling research on animal behavior analysis and optimal drone survey protocols.**

## Dataset Details

### Dataset Description

- **Curated by:** Jenna M. Kline, Elizabeth Campolongo
- **Language(s):** English (metadata and documentation)
- **Homepage:** [KABR Project](https://imageomics.github.io/KABR/)
- **Repository:** [kabr-behavior-telemetry](https://github.com/Imageomics/fair_drones/tree/main/examples/kabr)
- **Paper:** In preparation 

This dataset provides frame-level integration of drone telemetry (GPS position, altitude, camera settings), animal detection bounding boxes, and expert-annotated behaviors from aerial wildlife monitoring in Kenyan savannas. Collected January 11-17, 2023 at Mpala Research Centre, the dataset contains 57 videos with complete occurrence records covering Grevy's zebras (*Equus grevyi*), plains zebras (*Equus quagga*), and reticulated giraffes (*Giraffa reticulata*).

The dataset was developed to analyze optimal drone flight parameters for wildlife behavior research—correlating altitude, speed, and camera settings with data quality and animal disturbance levels. It implements Darwin Core biodiversity standards with Humboldt Eco extensions for ecological inventory data, ensuring interoperability with biodiversity databases like GBIF.

Key features:
- **57 complete video occurrence files** with ~10,000-66,000 frames each
- **68 video-level Darwin Core events** with GPS bounds and temporal coverage
- **18 session-level events** aggregating mission-level metadata
- **Frame-synchronized data**: GPS coordinates, camera EXIF, detection boxes, behavior labels
- **Behavior ethogram**: Walking, running, grazing, vigilance, social interactions, and more
- **Multi-species coverage**: Three focal species across diverse habitats

### Supported Tasks and Applications

This dataset supports computer vision, ecological analysis, and autonomous systems research:

**🤖 Computer Vision Tasks:**
- Object Detection (bounding boxes around animals)
- Multi-Object Tracking (ID consistency across frames in mini-scenes)
- Behavior Recognition (activity classification)
- Scale-Invariant Detection (animals at varying altitudes/distances)

**🌿 Ecological Applications:**
- Behavioral time budgets and activity patterns
- Habitat use analysis
- Group size and composition estimation
- Flight parameter impact on data quality
- Animal response to drone presence

**🚁 Drone Systems Research:**
- Optimal altitude/speed/distance determination
- Camera parameter optimization for wildlife
- Detection performance vs. flight parameters
- Disturbance minimization protocols

## Dataset Structure

### Directory Organization

```
kabr-behavior-telemetry/
├── data/
│   ├── occurrences/           # Frame-level occurrence records (57 videos)
│   │   ├── 11_01_23-DJI_0977.csv
│   │   ├── 11_01_23-DJI_0978.csv
│   │   └── ...
│   ├── video_events.csv       # Darwin Core Event records (68 videos)
│   └── session_events.csv     # Darwin Core Event records (18 sessions)
├── scripts/
│   ├── merge_behavior_telemetry.py    # Generate occurrence files
│   ├── update_video_events.py         # Add annotation file paths
│   ├── add_event_times.py             # Extract temporal bounds
│   └── add_gps_data.py                # Extract GPS statistics
├── metadata/
│   ├── DATA_DICTIONARY.md             # Complete field descriptions
│   └── event_session_fields.csv       # Field metadata
└── README.md
```

### Data Instances

**Occurrence Files** (`data/occurrences/*.csv`):

Each CSV contains frame-by-frame records for one video. Example from `11_01_23-DJI_0977.csv`:

| Field | Example Value | Description |
|-------|---------------|-------------|
| `date` | 11_01_23 | Recording date |
| `video_id` | DJI_0977 | Video identifier |
| `frame` | 0 | Frame number |
| `date_time` | 2023-01-11 16:04:03,114,286 | Timestamp with μs precision |
| `latitude` | 0.399770 | GPS latitude (WGS84) |
| `longitude` | 36.891217 | GPS longitude (WGS84) |
| `altitude` | 20.2 | Altitude (m above sea level) |
| `iso` | 100 | Camera ISO |
| `xtl`, `ytl`, `xbr`, `ybr` | 1245, 678, 1389, 842 | Bounding box coordinates |
| `id` | 12 | Mini-scene/track ID |
| `behaviour` | walking | Behavior class |

**Naming Convention:**
```
{date}_{video_id}.csv
Example: 11_01_23-DJI_0977.csv
         └─date─┘ └video_id┘
```

**Temporal Information:**
- Date range: 2023-01-11 to 2023-01-17
- Time coverage: Morning (09:38) to afternoon (16:28)
- Dry season in Laikipia, Kenya

### Data Fields

**See [metadata/DATA_DICTIONARY.md](metadata/DATA_DICTIONARY.md) for complete field descriptions.**

Key field groups:

**🌿 Darwin Core Event Fields** (`video_events.csv`, `session_events.csv`):
- Event identifiers and temporal coverage
- Geographic coordinates and bounds
- Sampling protocol descriptions
- Taxonomic scope and abundance
- Humboldt Eco extensions for inventory data

**📍 Geolocation** (occurrence files):
- GPS latitude/longitude (WGS84)
- Altitude above sea level
- Launch point and bounding box (event files)

**📷 Camera Metadata** (occurrence files):
- ISO, shutter speed, aperture
- Focal length and zoom ratio
- Color temperature and mode

**🦓 Detection Annotations** (occurrence files):
- Bounding box coordinates (CVAT format)
- Track ID for multi-frame sequences
- Occlusion and truncation flags

**🏃 Behavior Labels** (occurrence files):
- Activity classification (ethogram-based)
- Behavioral state at frame capture
- Mini-scene grouping

### Data Splits

This dataset does not include pre-defined train/val/test splits. Recommended splitting strategies:

**Temporal Split:**
- Train: Jan 11-13 (sessions 1-8)
- Val: Jan 16 (session 9)
- Test: Jan 17 (sessions 10-11)

**Spatial Split:**
- Split by location clusters based on GPS coordinates

**Species-Stratified:**
- Ensure all three species in each split

**Mission-Based:**
- Keep complete sessions together (do not split individual videos)

## Platform and Mission Specifications

### 🚁 Platform Details

**Type:** UAV (Unmanned Aerial Vehicle)

**Hardware:**
- **Primary Platform:** DJI Mavic Air 2
- **Secondary Platform:** DJI Mini
- Max flight time: ~25-30 minutes
- Wind resistance: Moderate (class 5 winds, ~8-10 m/s)

**Autonomy:**
- Mode: Manual flight with GPS stabilization
- Navigation: Operator-controlled following focal groups
- Collision avoidance: Obstacle detection enabled
- Return-to-home: Automatic on signal loss

### 📷 Sensor Specifications

**Primary Sensor: DJI Integrated Camera**
- Type: RGB
- Resolution: 5472 × 3078 pixels (5.4K)
- Frame rate: 24-30 fps
- Bit depth: 8-bit
- Format: MP4 video

**Telemetry Included:**
- GPS coordinates (SRT files embedded in video)
- IMU data (altitude, orientation)
- Camera settings (ISO, shutter, aperture, focal length)
- Timestamp synchronization

### 🗺️ Mission Parameters

**Flight Specifications:**
- Altitude: 20-50 m AGL (above ground level)
- Typical altitude: 30-40 m
- Speed: 0-5 m/s (adaptive to animal movement)
- Flight pattern: Focal animal follows (manual tracking)
- Duration per mission: 5-50 minutes

**Environmental Conditions:**
- Season: Dry season (January)
- Weather: Clear to partly cloudy
- Wind: Light to moderate
- Time of day: Morning (09:00-12:00) and afternoon (14:00-16:30)

### 🔍 Sampling Protocol

**Survey Design:**
- Focal group follows: Single herd tracked continuously per session
- Opportunistic sampling of observed groups
- Continuous video recording during follows

**Flight Operations:**
- Licensed drone operators with Kenya Civil Aviation Authority approval
- Maintained minimum altitude of 20m to minimize disturbance
- Animals monitored for behavioral response; flight aborted if disturbance detected

**Data Collection:**
- Continuous video recording at 5.4K resolution
- GPS telemetry embedded in SRT sidecar files
- Frame extraction in CVAT for annotation

**Quality Control:**
- Field notes recorded for each session
- Video quality assessed before annotation
- Behavior annotations reviewed by expert ecologists

## Dataset Creation

### Curation Rationale

This dataset was created to address two key research questions:

1. **What drone flight parameters optimize behavioral data quality?** By correlating altitude, speed, distance, and camera settings with annotation completeness and animal visibility, researchers can develop evidence-based protocols for wildlife monitoring.

2. **Can we quantify animal disturbance from drone presence?** Frame-level behavior annotations allow detection of alert, fleeing, or disrupted behaviors that indicate drone impact.

The dataset fills a critical gap: while many drone wildlife datasets provide detection boxes, few include detailed behavior labels synchronized with flight telemetry. This enables research on the trade-offs between data quality and animal welfare.

### Source Data

#### Data Collection and Processing

**Field Collection:**

1. **Planning:**
   - Sites selected based on known zebra and giraffe populations at Mpala Research Centre
   - Flights conducted during peak activity hours (morning/afternoon)
   - Safety briefings and airspace clearance for each flight

2. **Collection:**
   - Operators located focal groups via binoculars or vehicle sighting
   - Drones launched 50-100m from animals
   - Continuous video recording while following group movements
   - Flight logs automatically recorded in SRT files
   - Field notes on weather, behavior, and technical issues

3. **Post-Processing:**
   - Videos transferred from SD cards with immediate backup
   - SRT files extracted for telemetry data
   - Frame extraction at 1 fps in CVAT annotation platform
   - Detection bounding boxes drawn for all visible animals
   - Mini-scenes identified (continuous behavioral sequences)
   - Behavior labels applied by trained ecologists
   - Quality review of all annotations

**Software and Tools Used:**
- Flight planning: DJI Fly app
- Video capture: DJI Mavic Air 2 / DJI Mini onboard recording
- Frame extraction: CVAT (Computer Vision Annotation Tool)
- Annotation: CVAT with custom behavior taxonomy
- Telemetry parsing: Custom Python scripts
- Data merging: `merge_behavior_telemetry.py` (this repository)

### Annotations

#### Annotation Process

**🤖 Annotation Method:**
- [x] Semi-automated (CVAT tracking tools + manual review and behavior labeling)

**Tools Used:**
- Software: CVAT (Computer Vision Annotation Tool)
- Version: Web-based platform (2023)

**Annotation Guidelines:**
- All visible animals annotated with bounding boxes
- Bounding boxes drawn tightly around animal body
- Partial occlusions included if >30% of animal visible
- Track IDs maintained across frames within mini-scenes
- Behavior labels applied based on dominant activity in frame
- Uncertain behaviors marked for expert review

**Quality Control:**
- Training included intensive review of species-specific behavioral definitions with video examples, technical instruction on the CVAT interface, and practice annotation sessions until achieving greater than 90\% agreement with expert annotations
- Weekly calibration sessions throughout the annotation period to address interpretation drift and maintain consistency across all annotators. These included random double-annotation of 10\% of mini-scenes to monitor inter-annotator reliability (achieving $\kappa=0.88$ for primary behavioral categories), weekly calibration sessions to address any annotation drift, and final expert review by field-experienced team members for all completed annotations. 

**Annotation Coverage:**
- Fully annotated: No (not all frames have animals)
- Frames with visible animals: ~90% annotated
- Behavior labels: Applied to mini-scenes (continuous sequences)
- Missing annotations: Frames without animals or poor quality (blur, occlusion)

#### Who are the annotators?

**Annotator Team:**
- Number of annotators: 10, including expert reviewers
- Expertise: Research staff, professors, and students in ecology/computer science with wildlife identification training
- Training provided: 2 hours initial training + ongoing feedback
- Compensation: Academic credit and authorship

**Subject Matter Experts:**
- Daniel Rubenstein - Guidance on zebra and giraffe behavior
- Charles Stewart - Computer vision and annotation protocols
- Tanya Berger-Wolf - Funding, project oversight
- Elizabeth Campolongo - Data science and annotation review
- Matt Thompson - Software development and data processing
- Jenna Kline - Drone operations, project lead, annotation review

### Personal and Sensitive Information

**⚠️ Privacy and Security Considerations:**

**Human Subjects:**
- [x] No humans visible in imagery
- Note: Flights conducted in remote areas away from settlements

**Endangered Species:**
- [x] Contains endangered/threatened species: *Equus grevyi* (Grevy's zebra, Endangered)
- Location precision: Full GPS coordinates included (site is within protected research center)
- Consultation: Mpala Research Centre and Kenya Wildlife Service approved data sharing

**Cultural Sensitivity:**
- [x] Traditional lands: Mpala Research Centre operates with community consent

**Security:**
- [x] No security concerns
- Data collected in collaboration with local authorities
- Full coordinates shared to support scientific use

## Considerations for Using the Data

### Dataset Statistics

**Species Distribution:**

| Species (Scientific Name) | Common Name | Videos | Sessions | Individuals (range) |
|---------------------------|-------------|--------|----------|---------------------|
| *Equus grevyi* | Grevy's zebra | 5 | 3 | 3-7 |
| *Equus quagga* | Plains zebra | 30 | 11 | 2-12 |
| *Giraffa reticulata* | Reticulated giraffe | 6 | 2 | 4-8 |
| Mixed | Multiple species | 6 | 1 | 2-4 |

**Class Balance:**
- Plains zebra over-represented (opportunistic sampling)
- Grevy's zebra limited by lower population density
- Giraffes limited to specific habitat types

**Video Characteristics:**
- Frame count range: 10,000-66,000 frames per video
- Duration range: 3-50 minutes per video
- Altitude range: 8-72 m above sea level
- Typical animal size in frame: 50-200 pixels (height)

**Behavior Distribution:**
- Walking: ~40%
- Grazing: ~25%
- Standing/vigilance: ~20%
- Running: ~10%
- Other (social, nursing, etc.): ~5%

### Bias, Risks, and Limitations

**⚠️ Known Biases:**

1. **Geographic Bias:**
   - Data from single site (Mpala Research Centre, Laikipia)
   - May not generalize to other savanna ecosystems
   - Represents dry season only, captured during drought conditions

2. **Temporal Bias:**
   - Morning and afternoon flights only (battery/weather constraints)
   - Nocturnal or dawn/dusk behavior not captured
   - Single month snapshot (seasonal variation not represented)

3. **Species Bias:**
   - Plains zebra over-represented (most abundant species)
   - Grevy's zebra limited by population size
   - No data on smaller species (<50 cm body size)

4. **Environmental Bias:**
   - Dry season habitat conditions
   - Drought-affected vegetation
   - Clear to partly cloudy weather only
   - No wet season or dense vegetation scenarios

5. **Detection Bias:**
   - Animals in open areas more likely to be followed
   - Dense vegetation reduces detection probability
   - Cryptic species under-represented

**Technical Limitations:**

- **Image Quality:** Variable due to altitude, lighting, and atmospheric conditions
- **Coverage Gaps:** 11 videos lack occurrence data due to missing/corrupted SRT files or failed processing
- **Annotation Limitations:** Behavior labels are subjective; inter-observer agreement not quantified
- **GPS Accuracy:** ±5-10m typical; may drift during long flights

**Ethical Limitations:**

- **Animal Welfare:** Potential for disturbance despite mitigation efforts
- **Data Usage:** GPS coordinates could theoretically enable harmful uses (though species are common and well-protected at Mpala)

### Recommendations

**Best Practices for Using This Dataset:**

1. **For Detection/Tracking Models:**
   - Account for altitude-dependent scale variation (20-50m range)
   - Consider species-specific detection difficulty (giraffes easier than zebras)
   - Test generalization to new sites (single-location training data)

2. **For Behavior Recognition:**
   - Class imbalance exists; consider weighted loss or resampling
   - Behavior labels are coarse; fine-grained states may be ambiguous
   - Temporal context improves accuracy (behaviors occur in sequences)

3. **For Ecological Analysis:**
   - Do not extrapolate to wet season without additional data
   - Account for detection probability varying by habitat/altitude
   - Animal counts are minimum estimates (some individuals may be hidden)

4. **For Drone Protocol Development:**
   - Correlate altitude/speed with detection rate and annotation completeness
   - Monitor for behavioral responses in data (alert, flee behaviors)
   - Consider trade-offs between data quality and disturbance risk

**Ethical Use:**

- Do not use for unethical wildlife targeting or harassment
- Respect that full GPS coordinates enable site replication for conservation research
- Cite dataset appropriately and acknowledge indigenous land stewardship

**What This Dataset Should NOT Be Used For:**

- Estimating absolute population sizes (sampling is not systematic)
- Generalizing to wet season, nighttime, or other habitats/regions

## Licensing Information

**Dataset License:** [CC0 1.0 Universal (CC0 1.0) Public Domain Dedication](https://creativecommons.org/publicdomain/zero/1.0/)

**Citation Requirement:** While CC0 does not legally require citation, we strongly request that you cite the dataset and associated paper if you use this data (see [Citation section](#citation)).

**Code License:** MIT License for scripts in this repository

## Citation

**If you use this dataset, please cite:**

**Dataset:**
```bibtex
@misc{kline2024kabr_behavior_telemetry,
  author = {Jenna Kline and Maksim Kholiavchenko and Michelle Ramirez and Sam Stevens and Alec Sheets and Reshma Ramesh Babu and
    Namrata Banerji and Elizabeth Campolongo and Matthew Thompson Nina Van Tiel and Jackson Miliko and Isla Duporge and Neil Rosser and Eduardo Bessa and Charles Stewart and Tanya Berger-Wolf and Daniel Rubenstein},
  title = {KABR Behavior Telemetry: Frame-Level Drone Wildlife Monitoring Dataset},
  year = {2024},
  publisher = {Hugging Face},
  url = {https://huggingface.co/datasets/imageomics/kabr-behavior-telemetry}
}
```

**Associated Paper:**
```bibtex
@article{kline2024integrating,
  title = {Integrating Biological Data into Autonomous Remote Sensing Systems for
           In Situ Imageomics: A Case Study for Kenyan Animal Behavior Sensing with
           Unmanned Aerial Vehicles (UAVs)},
  author = {Kline, Jenna M. and Campolongo, Elizabeth and Thompson, Matt and others},
  journal = {arXiv preprint arXiv:2407.16864},
  year = {2024},
  url = {https://arxiv.org/abs/2407.16864}
}
```

**FAIR² Drone Data Standard:**
```bibtex
@article{kline2025fair2,
  title = {Toward a FAIR² Standard for Drone-Based Wildlife Monitoring Datasets},
  author = {Kline, Jenna and others},
  year = {2025},
  note = {In preparation}
}
```

## Acknowledgements

This work was supported by the [Imageomics Institute](https://imageomics.org), which is funded by the US National Science Foundation's Harnessing the Data Revolution (HDR) program under [Award #2118240](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2118240) (Imageomics: A New Frontier of Biological Information Powered by Knowledge-Guided Machine Learning). Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.

We thank:
- **Mpala Research Centre** and **Jackson Miliko** for logistical support and site access
- **Kenya Wildlife Service** for research permits
- **Kenya Civil Aviation Authority** for drone operation clearances
- **Local field assistants** from Mpala Research Centre
- **Annotation team**: 
Maksim Kholiavchenko (Rensselaer Polytechnic Institute) - ORCID: 0000-0001-6757-1957
Jenna Kline (The Ohio State University) - ORCID: 0009-0006-7301-5774
Michelle Ramirez (The Ohio State University)
Sam Stevens (The Ohio State University)
Alec Sheets (The Ohio State University) - ORCID: 0000-0002-3737-1484
Reshma Ramesh Babu (The Ohio State University) - ORCID: 0000-0002-2517-5347
Namrata Banerji (The Ohio State University) - ORCID: 0000-0001-6813-0010
Elizabeth Campolongo (Imageomics Institute, The Ohio State University) - ORCID: 0000-0003-0846-2413
Matthew Thompson (Imageomics Institute, The Ohio State University) - ORCID: 0000-0003-0583-8585
Nina Van Tiel (Eidgenössische Technische Hochschule Zürich) - ORCID: 0000-0001-6393-5629
Daniel Rubenstein (Princeton University) - ORCID: 0000-0002-8285-1233
- **Data Collection Team:**
Jenna M. Kline (The Ohio State University)
Michelle Ramirez (The Ohio State University)
Sam Stevens (The Ohio State University)
Reshma Ramesh Babu (The Ohio State University) - ORCID: 0000-0002-2517-5347
Isla Duporge (The Ohio State University) - ORCID: 0000-0002-9873-1233
Neil Rosser (The Ohio State University) - ORCID: 0000-0002
- **Project Oversight and Guidance:**
Elizabeth Campolongo (Imageomics Institute, The Ohio State University) - ORCID: 0000-0003-0846-2413
Matthew Thompson (Imageomics Institute, The Ohio State University) - ORCID: 0000-0003-0583-858
Tanya Berger-Wolf (Imageomics Institute, The Ohio State University) - ORCID: 0000-0002-1236-4153
Charles Stewart (Rensselaer Polytechnic Institute) - ORCID: 0000-0002-5204-1862
Daniel Rubenstein (Princeton University) - ORCID: 0000-0002-8285-1233


**Conservation Partners:**
- Mpala Research Centre, Laikipia County, Kenya
- Grevy's Zebra Trust

**Data Collection Permits:**
The data was gathered at the Mpala Research Centre in Kenya, in accordance with Research License No. NACOSTI/P/22/18214. 
The data collection protocol adhered strictly to the guidelines set forth by the Institutional Animal Care and Use Committee under permission No. IACUC 1835F.

## Validation and Quality Metrics

**🤖 AI-Readiness Validation:**

- [x] Machine-readable metadata (YAML front matter complete)
- [x] Structured annotations in Darwin Core format
- [ ] Train/val/test splits pre-defined (users should create)
- [x] Class distribution documented
- [x] Data loading code provided (Python scripts)
- [ ] Example notebooks (planned)

**🌿 Darwin Core Validation:**

- [x] Event records complete and valid
- [x] Occurrence records complete and valid (57/68 videos)
- [x] Scientific names validated against GBIF backbone
- [x] Coordinates in WGS84
- [x] Sampling protocol documented
- [ ] GBIF dataset registration (planned)

**⚠️ FAIR² Compliance Checklist:**

- [ ] **Findable:** DOI to be assigned
- [x] **Accessible:** Open access via GitHub/Hugging Face
- [x] **Interoperable:** Darwin Core, Humboldt Eco, CSV/JSON formats
- [x] **Reusable:** CC0 license, full provenance documented
- [x] **AI-Ready:** Machine-readable, structured, versioned

## Code and Tools

**Data Loading (Python):**

```python
import pandas as pd

# Load session-level events
sessions = pd.read_csv('data/session_events.csv')

# Load video-level events
videos = pd.read_csv('data/video_events.csv')

# Load occurrence records for a specific video
occurrences = pd.read_csv('data/occurrences/11_01_23-DJI_0977.csv')

# Filter to frames with detections
detections = occurrences.dropna(subset=['xtl', 'ytl', 'xbr', 'ybr'])

# Group by behavior
behavior_counts = detections.groupby('behaviour').size()
```

**Processing Scripts:**

See `scripts/` directory for:
- `merge_behavior_telemetry.py` - Generate occurrence files from source data
- `update_video_events.py` - Add annotation file references
- `add_event_times.py` - Extract temporal bounds
- `add_gps_data.py` - Calculate GPS statistics

## Glossary

- **AGL:** Above Ground Level - altitude measured from terrain surface
- **Darwin Core:** Biodiversity data standard maintained by TDWG
- **Ethogram:** Catalog of behaviors exhibited by a species
- **FAIR²:** FAIR principles extended for AI-ready datasets
- **Humboldt Eco:** Extension of Darwin Core for ecological inventory data
- **Mini-scene:** Continuous behavioral sequence tracked across frames
- **Occurrence:** Darwin Core term for species observation record
- **SRT:** SubRip subtitle format; used for drone telemetry embedding
- **TDWG:** Biodiversity Information Standards (Taxonomic Databases Working Group)
- **UAV:** Unmanned Aerial Vehicle (drone)
- **WKT:** Well-Known Text format for geographic geometries

## Dataset Card Authors

Jenna M. Kline

## Dataset Card Contact

For questions about this dataset:
- **Primary Contact:** Jenna M. Kline (kline.377@osu.edu)
- **Issues:** [GitHub repository issues](https://github.com/Imageomics/kabr-behavior-telemetry/issues)
- **KABR Project:** https://imageomics.github.io/KABR/

---

**Version History:**

- v1.1.0 (2026-01-02): Added occurrence files, GPS data, temporal bounds, updated Darwin Core events
- v1.0.0 (2024-12-31): Initial release with session and video event metadata

---

*This dataset card follows the FAIR² Drone Data Standard and extends the [Imageomics dataset card template](https://imageomics.github.io/Imageomics-guide/wiki-guide/HF_DatasetCard_Template_mkdocs/).*
