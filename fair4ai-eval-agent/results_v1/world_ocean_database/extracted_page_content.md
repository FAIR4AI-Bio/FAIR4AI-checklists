The World Ocean Database (WOD) is world's largest collection of uniformly formatted, quality controlled, publicly available ocean profile data. It is a powerful tool for oceanographic, climatic, and environmental research, and the end result of more than 20 years of coordinated efforts to incorporate data from institutions, agencies, individual researchers, and data recovery initiatives into a single database. WOD data spans from Captain Cook's 1772 voyage to the contemporary Argo period, making it a valuable resource for long term and historical ocean climate analysis. Original versions of the 20,000+ datasets in the WOD are available through the NCEI archives.

Data Access

Documentation

Quality Control

Help

Access Methods

Use the WODselect retrieval system to search the WOD by specific parameters (date, geographic area, probe type, etc.) and measured variables. View a dataset distribution map and cast count of your search criteria, and download a custom dataset in WOD native, csv, or netCDF.

Launch WODSelect

WOD Updates

WOD data is also accessible through interfaces that sort data geographically and by date in native ASCII format.

Data by Location

Data by Year

For additional documentation and access methods, visit the

dataset landing page

.

Auxiliary Datasets

Secchi Disk Dataset Format Description

Download Observations

Observation File Columns

Accession number (corresponds to original data in archive)

WOD cruise designator

WOD unique cast number

Latitude

Longitude

Year

Month

Day

Time (GMT, 24 hr format)

Secchi disk depth (meters)

Water color (

extended Forel/Ule scale)

Major Releases

The WOD consists of periodic major releases and quarterly updates to those releases. Each major release is associated with a concurrent release of the World Ocean Atlas (WOA), and contains final quality control flags used in the WOA, which includes manual as well as automated steps.

Each quarterly update release includes additional historical and recent data and preliminary quality control. The latest major release is World Ocean Database 2023 (WOD23), which includes more than 18.6 million oceanographic casts made up of 3.13 billion individual profile measurements.

Current Version: WOD23

Mishonov A.V., T. P. Boyer, O. K. Baranova, C. N. Bouchard, S. Cross, H. E. Garcia, R.  A. Locarnini, C. R. Paver, J. R. Reagan, Z. Wang, D. Seidov, A. I. Grodsky, J. G. Beauchamp, (2024): World Ocean Database 2023. C. Bouchard, Technical Ed., NOAA Atlas NESDIS 97, 206 pp.,

doi.org/10.25923/z885-h264

,

World Ocean Database 2023

WOD18

Boyer, T.P., O.K. Baranova, C. Coleman, H.E. Garcia, A. Grodsky, R.A. Locarnini, A.V. Mishonov, C.R. Paver, J.R. Reagan, D. Seidov, I.V. Smolyar, K. Weathers, M.M. Zweng,(2018): World Ocean Database 2018. A.V. Mishonov, Technical Ed., NOAA Atlas NESDIS 87.

World Ocean Database 2018

WOD13

Boyer, T.P., J.I. Antonov, O.K. Baranova, C. Coleman, H.E. Garcia, A. Grodsky, D.R. Johnson, R.A. Locarnini, A.V. Mishonov, T.D. O'Brien, C.R. Paver, J.R. Reagan, D. Seidov, I.V. Smolyar, and M.M. Zweng, 2013: World Ocean Database 2013., S. Levitus, Ed., A. Mishonov, Technical Ed.; NOAA Atlas NESDIS 72, 209 pp.,

doi:10.7289/V5NZ85MT

.

WOD09

Boyer, T.P., J.I. Antonov , O.K. Baranova, H.E. Garcia, D.R. Johnson, R.A. Locarnini, A.V. Mishonov, T. D. O’Brien, D. Seidov, I.V. Smolyar, M.M. Zweng, 2009. World Ocean Database 2009 S. Levitus, Ed., NOAA Atlas NESDIS 66, 216 pp.,

https://repository.library.noaa.gov/view/noaa/1195

WOD05

Boyer, T.P., J.I. Antonov, H.E. Garcia, D.R. Johnson, R.A. Locarnini, A.V. Mishonov, M T. Pitcher, O.K. Baranova, I.V. Smolyar, 2006. World Ocean Database 2005. S. Levitus, Ed., NOAA Atlas NESDIS 60, 190 pp.,

https://repository.library.noaa.gov/view/noaa/1131

Current Citations

WOD Introduction

Mishonov A.V., T. P. Boyer, O. K. Baranova, C. N. Bouchard, S. Cross, H. E. Garcia, R.  A. Locarnini, C. R. Paver, J. R. Reagan, Z. Wang, D. Seidov, A. I. Grodsky, J. G. Beauchamp, (2024): World Ocean Database 2023. C. Bouchard, Technical Ed., NOAA Atlas NESDIS 97, 206 pp.,

doi.org/10.25923/z885-h264

WOD Introduction

WOD User Manual

Garcia, H.E., T. P. Boyer, R. A. Locarnini, J. R. Reagan, A. V. Mishonov, O. K. Baranova, C. R. Paver, Z. Wang, C. Bouchard, S. Cross, D. Seidov, D. Dukhovskoy (2024). World Ocean Database 2023: User’s Manual. A.V. Mishonov, Technical Ed., NOAA Atlas NESDIS 98, pp 129.,

doi.org/10.25923/j8gq-ee82

WOD User Manual

Data Sources

The oceanographic data that comprise the WOD have been acquired through many sources and projects as well as from individual scientists. In addition, many international organizations such as the IODE/GODAR and WDS have facilitated data exchanges, which have provided much data to the WOD. The World Ocean Database (WOD) is an NCEI product and an

IODE

(International Oceanographic Data and Information Exchange) project. This work is funded in partnership with the NOAA OAR

Global Ocean Monitoring (GOMO)

.

Ocean Profiles

The WOD is made up of ocean profiles, which contain measurements for a single variable (temperature, salinity, etc.) taken from one location at different depths, or a horizontal string of readings taken from the surface. WOD profiles must contain more than a single depth/variable pair. Multiple profiles taken at the same location with the same set of instruments form an oceanographic cast.

Variables

Temperature

Salinity

Oxygen

Nutrients

Tracers

Biological variables (plankton, chlorophyll, etc.)

Consult the

WOD Introduction

for a full set of definitions, and the

WOD User’s Manual

for a description of fields and codes.

Code Tables

Code tables necessary to use the World Ocean Database data.

Code Table Library

WOD Masks

Data masks delineating ocean areas, range basins, and 5-degree standard deviation.

range_area.msk

Ocean areas for each set of variable min/max ranges

range_basin_list.msk

Range basins list

sd_multiplier.msk

5-degree standard deviation multiplier

WOD Programs

Programs List

Use these programs to read WOD data, or convert it from WOD format to tabular column or comma separated columns (.csv)

wod_nc.f

Sample FORTRAN program for reading WOD ragged array netCDF files

readFOR.txt

Readme file describes the wodFOR programs

wodFOR.f

Sample FORTRAN program for reading the data

sampFOR.txt

Sample of output from wodFOR.f

readASC.txt

Describes the use of wodASC.f

wodASC.f

Outputs a user selected variable in either tabular or comma separated columns

wodASC.exe

Executable for wodASC.f program

sampASC.txt

Sample output data from wodASC.f

wodSUR.f

Writes surface-only data out in a comma-separated-value (CSV) format

wodSUR.exe

Microsoft compatible executable for wodSUR.f

sampSUR.txt

Sample of output from wodSUR.exe

readC.txt

Readme file describing the wodC program

wodC.c

Sample C program for reading the data

wodC.exe

Executable for C program

wodtodepthmatrix_info.txt

Info file describing the wodtodepthmatrix.c program

wodtodepthmatrix.c

Sample C program for reading the data

Wodtodepthmatrix.exe

Executable for wodtodepthmatrix.exe program (for Windows 64bit system)

About Quality Control

Quality control procedures are documented and performed on each cast and the results are included as flags on each measurement. The WOD contains the data on the originally measured depth levels (observed) and also interpolated to standard depth levels to present a more uniform set of iso-surfaces for oceanographic and climate work.

The WOD is made up of more than 20,000 separate archived datasets from the United States and around the world, each of which is available in its original form in the NCEI archives. All datasets are converted to the same standard format, checked for duplication within the WOD, and assigned quality flags based on objective tests. Additional subjective flags are set upon calculation of ocean climatological mean fields which make up the World Ocean Atlas (WOA) series.

Corrections

Expendable Bathythermograph (XBT) Corrections

XBT References Table

Mechanical Bathythermograph (MBT) Corrections

Frequently Asked Questions

Please find guidance below on the following topics:

Access

Data Specifics

Global Ocean Heat and Salt Content

For additional help, please contact

OCL.help@noaa.gov

.

Access

Am I allowed to use and reproduce WOD/WOA data/figures in my publications?

The World Ocean Database and World Ocean Atlas are available for public use without restriction. Please let us know about WOD and WOA based publications by sending citations to

ncei.info@noaa.gov.

How do you extract header information from historical temperature profiles without processing the data?

With some programming skills, you can adapt WOD data reading programs to retrieve only header information from WOD native ASCII files, or create a subset in WODselect to isolate a geographic distribution graphic.

How do I access Sea Surface Temperature (SST) data?

The

Global Ocean Heat and Salt Content

product has historical sea surface temperature anomaly data from in situ measurements dating back to 1955. Download the temperature anomaly data, then add the temperature anomalies back to the climatological means (available on the same page) to calculate SSTs (as well as water temperature in the depth) for each year (or season) 1955 to present.

How do I download WOD data in NetCDF?

You can download data in netCDF, as well as CSV and WOD Native through WODselect.

How do I convert WOD ASCII data to a readable format?

Ocean Data View (ODV), a freeware oceanographic profile data display. Detailed instructions are available in the

WOD Tutorial

beginning on page 7. Note that ODV cannot read surface only data, originator's quality flags, or plankton biomass and taxonomic data in the OSD file.

Use WODselect to download data as CSV or netCDF

How do I download WOD18 data for a specific region?

Use WODselect to search data by geographic coordinates

Can I download the entire WOD database?

To download WOD in native ASCII, use the following command:

wget -N -nH -nd -r -e robots=off --no-parent --force-html https://data.nodc.noaa.gov/woa/WOD/YEARLY/.

For netCDF format, mark all years in WODselect (1773-2018), and request the data in netCDF. You will receive an email with files attached once your request is processed.

How long are my requested files available on the FTP site?

Files are removed from the FTP site 3 days after they are created.

Can I use the cruise ID number to find cruise attributes?

In WODselect:

Check the CRUISE option, select Build a Query.

Enter a cruise number in the search box (example format: US029567) and select Get an Inventory. To search multiple cruises, separate the number with a comma.

Select CRUISE LIST for a list of cruises with links to cruise and accession metadata.

Select a cruise to open a file with data distribution map at the top. Scroll down to access metadata.

Example:

US029567. Click the accession# for the link to the Archive System.

WOD CRUISE REFERENCE US029567

COUNTRY UNITED STATES (US)

NCEI ACCESSION NUMBER (CTD) 59005

SHIP NAME ALPHA HELIX

INSTITUTE ALFRED-WEGENER-INSTITUTE (BREMERHAVEN)

PROJECT SHELF BASIN INTERACTION PROJECT (SBI)

DATE OF FIRST CAST 9/8/2001

DATE OF LAST CAST 9/12/2001

TOTAL NUMBER OF CASTS 54

Where can I look for references for XBT Bias Depth and Temperature Corrections?

The

XBT References Table

contains the list of relevant references.

How do I make XBT corrections in a profile?

The XBT correction is in the second header code 54. See the list of the codes and the correction they represent.

Data Specifics

Why does WOD18 have fewer profiling float casts than WOD09?

A number of floats in the North Atlantic had a pressure offset problem which was not correctable. The Argo program removed these floats from their dataset, and we followed their example.

Read Argo's explanation

How can I calculate the apparent oxygen utilization (AOU) in the deep ocean?

Use the saturation oxygen content calculated using potential temperature with respect to the surface, minus the dissolved oxygen measured at depth.

How is the Surface Only Dataset (SUR) organized?

The

WOD Surface-Only Dataset

is a set of single profile casts that contains all the surface-only data from an entire cruise. The individual levels of the surface-only form are distinct surface measurement sets from a given date/position. The cruise will span a time period from days to months rather than the single date/time of a profile cast. For this reason, surface-only data are in a single file rather than split out by year in the YEARLY directory, or by position in the GEOGRAPHIC directory.

Is there a time variable in WOD?

WOD time variables are listed in UTC format, and unspecified times are assumed to be UTC until otherwise proven.

As with all data, time zone information is not always correctly reported. We use quality control measure to correct common errors, including UTC designations that should be labeled as local time.

Does the WOD netCDF file contain information about the chlorophyll measuring method used?

Second Header variables in the netCDF file identify collection and processing methods used for the various parameters. For chlorophyll, we identify a whole suite of methods that range from in situ fluorometer to HPLC. The codes are listed below:

600 Fluorescence

601 Fluorescence in-situ Turner fluorometer (Strickland and Parsons 1972)

602 Fluorescence in-vivo underway (Lorenzen 1966)

603 Fluorometer in-situ CTD

604 Fluorometer (Aiken 1981)

605 Fluorometric chl-a assay acetone extraction

606 Fluorometric chl-a assay methanol extraction

607 Fluorometric chl-a assay acetone extraction; Turner fluorometer (Yentsch and Menzel, 1963, Holm-Hansen et al. 1965)

700 HPLC (High Performance Liquid Chromatography)

701 HPLC (normal phase High Performance Liquid Chromatography)

702 HPLC (reverse phase High Performance Liquid Chromatography)

About chlorophyll CTD profiles

Many of the chlorophyll measurements in CTD datasets are uncalibrated fluorometer readings that are often still in engineering units. These data have to be read very carefully, and can only be evaluated on a cruise by cruise basis. There is a calibration indicator (variable specific second header 14), but this information is rarely included with the data.

More information is available on page 19 of the World Ocean Database 2018

Introduction

.

What do large negative values at the particular depths mean? Why do these data have !C code ‘0’, for good data?

-999.99 represents missing data in the WOD. We use zero as the flag for missing data in conjunction with the -999.99 value.

How are WOD depth values calculated?

Data are submitted with depth values

We use UNESCO algorithm for standard ocean to calculate depth for data that includes pressure measurements

Data collected from an expendable bathythermograph (XBT) has depths which are calculated from a drop-rate equation and time since drop

Pre 1976 depth calculations were derived from wire length and angle

Regardless of the depth calculation method, all profiles are interpolated to the standard World Ocean Atlas standard depths.

Explain the output format for WOD-reading programs

Output generally includes ocean parameters, number of significant digits stored, and QC flags. The parenthetical value states the number of significant digits in the measurement directly to its left. The same is true for second headers. The two bracketed numbers are single digit quality flags; one set by the WOD, and the other by the originator.

Note:

The program only prints the first 3 decimal places, but the full value to the given significant figures is stored in the file’s array read.

Learn more about output format in the

WOD User Manual

, and consult

WOD codes

for specific flag values.

Which methods are used to measure nutrient data?

There isn’t a definitive set of methods for measuring or calculating nutrient data. From page 45 of the

WOD Introduction

:

It is difficult to estimate the precision and reproducibility of the historical chemical data in part because (1) there has not been a generally accepted set of standard international analytical oceanographic methods; (2) there has been a continuous availability over time of new or improved analytical techniques for the sampling and determination of the concentration of dissolved and particulate constituents in seawater; (3) there is the practical difficulty of periodic comparison of the precision and accuracy of oceanographic data collected by oceanographic institutions worldwide.

At present, we are not aware of a suitable monitoring program for the systematic comparison of analytical instruments, measurements, and certified reference standards used by international research Institutions or Universities to collect oceanographic observations.

We do include information on the method used for nutrient (and other) data when it is available. Variable description for the second header 6 may be found on

WOD codes

page, or accessed directly through the

methods list

.

Global Ocean Heat and Salt Content

What is the file format for Global Ocean Heat and Salt Content?

Officially archived versions of the fields are stored in Climate-Forecast (CF) compliant netCDF. See section 5, page 8 of

World Ocean Atlas 2018 documentation

for more details, other available formats.

Why is there an inconsistency between the 5-year and shorter average ocean heat anomalies?

The 5 year period is actually a composite calculated from the mean anomaly in each 1 degree grid square over a 5-year period using all measurements from that 5 year stretch. There’s a discrepancy between the 5 year composite and shorter periods, because the shorter means are based on conservative estimates due to limited data coverage. The 5-year composite mean typically has better data coverage, which allows for a less cautious, more precise estimate.

How is heat content calculated?

Temperature anomalies are calculated at 16 standard depths from 0-700m (or 26 standard depths 0-2000m) by subtracting observed (interpolated) temperatures from the long-term (1955-2018) climatological monthly mean. The mean of all temperature anomalies is calculated at each standard depth for every box on the grid. The temperature anomaly represents the volume of water that makes up the vertical distance from halfway between the next shallower depth and the given standard depth to halfway between the next deeper depth and the given standard depth.

The temperature anomaly is multiplied by the climatological mean density of the one-degree square and the heat capacity of water and the area and volume of the one-degree square for the given standard depth. The heat contents for each volume surrounding a standard depth are summed to calculate full ocean heat content anomaly for each one degree gridbox. The values for each gridbox are summed to calculate global value. [Note this is a global integral, not an average.] The area of each one-degree gridbox is calculated similar to the attached FORTRAN subroutine (easily adaptable to any software language).

The

land/sea mask

used to decide whether a one-degree gridbox is land or ocean (the one-degree, not quarter-degree) is derived from the ETOPO2 altitude/bathymetry data set. This same land/sea mask is used to determine whether the volume of a given one-degree square extends to the bottom of the integration level (700 m or 2000 m) or to a shallower depth. Because ocean temperature measurements are relatively sparse at the subsurface level, we use an objective analysis technique to calculate a complete set of one-degree temperature anomaly data at each standard depth after the anomalies from existing data are calculated. From there the heat content is calculated. The objective analysis technique is described in a number of publications, including

WOA18 Temperature

.

Does the dataset include yearly salt content data?

We have pentadal salinity anomalies back to 1955. See

Global Heat and Salt Content

, but yearly data only spans the Argo time period (i.e., 2005 onward) and is available on the salinity anomaly page.

What are the units for 0-700 m heat content?

The value of J/m**2 is multiplied by the grid area over which the heat content is calculated, resulting in final units of joules [J].

What is the halosteric component of sea level rise?

Halosteric change is the change in sea level due to the effects of salinity change on seawater density.