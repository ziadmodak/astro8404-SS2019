# astro8404_SS2019
Calibration and Imaging scripts for astro8404 (SS2019)

The ALMA Project used here is 2015.1.00497.S (PI: T. Davis) and its raw data can be downloaded from the [ALMA Science Archive](http://almascience.eso.org/aq/). The scripts focus on the data reduction and imaging of a single scientific target (NGC 1386).

Data from the tarball can be extracted using the ALMA downloader script or manually by running:
```
tar -xvf 2015.1.00497.S_uid___A002_Xaeaf96_X515.asdm.sdm.tar
```
All the data reduction, calibration and imaging is done in [CASA](https://casa.nrao.edu/) 5.1.1-5.

my_calibration.py is a Python script for calibrating the raw data.

my_imaging.py is a Python script for imaging NGC1386, one of the nearby galaxies observed in the project.
