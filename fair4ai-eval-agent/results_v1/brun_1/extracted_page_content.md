Despite plasticity, heatwaves are costly for a coral reef fish

Van Wert, Jacey

1

;

Birnie-Gauvin, Kim

2

;

Gallagher, Jordan

1

;

Hardison, Emily

1

;

Landfield, Kaitlyn

1

;

Burkepile, Deron

1

;

Eliason, Erika

1

Author affiliations

University of California, Santa Barbara

Technical University of Denmark

Published Jul 15, 2024

on

Dryad

.

https://doi.org/10.5061/dryad.wdbrv15vm

Data files

Jul 15, 2024 version files

11.17 KB

README.md

3.98 KB

VanWert_etal_2023_hawkfish.csv

7.19 KB

Click names to download individual files

Download full dataset

Abstract

Climate change is intensifying extreme weather events, including marine heatwaves, which are prolonged periods of anomalously high sea surface temperature that pose a novel threat to aquatic animals. Tropical animals may be especially vulnerable to marine heatwaves because they are adapted to a narrow temperature range. If these animals cannot acclimate to marine heat waves, the extreme heat could impair their behavior and fitness. Here, we investigated how marine heatwave conditions affected the performance and thermal tolerance of a tropical predatory fish, arceye hawkfish (

Paracirrhites arcatu

s), across two seasons in Mo'orea, French Polynesia. We found that the fish’s daily activities, including recovery from burst swimming and digestion, were more energetically costly in fish exposed to marine heatwave conditions across both seasons, while their aerobic capacity remained the same. Given their constrained energy budget, these rising costs associated with warming may impact how hawkfish prioritize activities. Additionally, hawkfish that were exposed to hotter temperatures exhibited cardiac plasticity by increasing their maximum heart rate but were still operating within a few degrees of their thermal limits. With more frequent and intense heatwaves, hawkfish, and other tropical fishes must rapidly acclimate, or they may suffer physiological consequences that alter their role in the ecosystem.

README:

Despite plasticity, heatwaves are costly for a coral reef fish

Description of the Data and file structure

Author Information

A. Principal Investigator Contact Information

Name: Dr. Erika Eliason or Dr. Deron Burkepile

Institution: University of California, Santa Barbara

Email:

eliason@ucsb.edu

,

dburkepile@ucsb.edu

B. Corresponding Author Contact Information

Name: Jacey Van Wert

Institution: University of California, Santa Barbara

Email:

jcvanwert@gmail.com

Date range of data collection (single date, range, approximate date): 2019-2022

Geographic location of data collection: Mo'orea, French Polynesia

File List:

VanWert_etal_2023_hawkfish.csv - contains hawkfish collection and morphology data, SMR, MMR, AAS, SDA metrics, and cardiac thermal tolerance test metrics

METHODOLOGICAL INFORMATION

Description of methods used for collection/generation/processing of data:

Hawkfish (

Paracirrhites arcatus

) were collected in Mo'orea, French Polynesia during Austral winter (2019) and Austral summer (2022). They were acclimated to one of five treatments (27, 28, 29, 31, or 33°C) for one week and tested for metabolic performance metrics, including maximum metabolic rate (MMR), standard metabolic rate (SMR), and costs of digestion (specific dynamic action, SDA) using custom-made respirometry chambers. A subset of fish was also tested for thermal tolerance using an acute cardiac thermal tolerance test. In addition, wild fish were also caught and tested for acute cardiac thermal tolerance. Metabolic data were processed in R and heart rate data were processed in LabChart. Please refer to the main manuscript for details regarding the methods used to collect and analyze this data.

People involved with sample collection, processing, analysis, and/or submission: Jacey C. Van Wert, Kim Birnie-Gauvin, Jordan Gallagher, Emily A. Hardison, Kaitlyn Landfield, Deron E. Burkepile, and Erika J. Eliason

DATA-SPECIFIC INFORMATION FOR: VanWert_etal_2023_hawkfish.csv

Number of variables: 22

Number of cases/rows: 76

Variable List:

hawkfish_no = unique fish ID

year = year of fish collection and measurements

season = Austral summer (summer) or Austral winter (winter)

treatment_new = acclimation temperature; 'wild' indicates fish were not acclimated and were collected from the wild and immediately tested

bw_g = wet mass of fish (units g)

tank = fish tank ID during acclimation

tl_cm = total length of fish (units cm)

sl_cm = standard length of fish (units cm)

chase_pre_v_post = whether exhaustive exercise chase occurred before (pre) or after (post) SMR measurements

mmr_corrected = body mass corrected maximum metabolic rate by universal metabolic scaling coefficient of 0.89 (units mg O2 kg-1 min-1)

smr_low10_all = standard metabolic rate (units mg O2 kg-1 min-1)

aas_corrected = absolute aerobic scope (units mg O2 kg-1 min-1)

fas = factorial aerobic scope calculated as mmr/smr (unitless)

percent_bw_scallop_fed = percent of body weight scallop fed for SDA trial

SDA_integrated = integral of specific dynamic action (SDA) (units mg O2 kg-1)

SDA_duration = duration of specific dynamic action (SDA) (units hours)

peak_SDA_max = maximum metabolic oxygen consumption (MO2) reached during specific dynamic action (SDA) (units mg O2 kg-1 min-1)

time_peak_SDA_max = time at which peak_SDA_max occurred (units hours)

sda_coeff = specific dynamic action (SDA) coefficient (units %)

tarr = temperature of arrhythmia (units degC), only measured during winter tests

fhmax_peak = peak maximum heart rate (units beats per min), only measured during winter tests

tpeak = temperature at which fhmax_peak occurred (units degC), only measured during winter tests

Sharing/Access Information

Licenses/restrictions placed on the data: N/A

Links to other publicly accessible locations of the data: N/A

Was data derived from another source? No

Methods

Hawkfish (

Paracirrhites arcatus

) were collected in Mo'orea, French Polynesia during the Austral winter (2019) and Austral summer (2022). They were acclimated to one of five treatments (27, 28, 29, 31, or 33°C) for one week and tested for metabolic performance metrics, including maximum metabolic rate (MMR), standard metabolic rate (SMR), and costs of digestion (specific dynamic action, SDA) using custom-made respirometry chambers. A subset of fish was also tested for thermal tolerance using an acute cardiac thermal tolerance test. In addition, wild fish were also caught and tested for acute cardiac thermal tolerance. Metabolic data were processed in R and heart rate data were processed in LabChart. Please see the published manuscript for detailed methods.

Works referencing this dataset

Van Wert, Jacey C.; Birnie-Gauvin, Kim; Gallagher, Jordan et al. (2024). Despite plasticity, heatwaves are costly for a coral reef fish. Scientific Reports.

https://doi.org/10.1038/s41598-024-63273-8