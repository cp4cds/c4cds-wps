# Test data

## CORDEX

We are using the following file:

* http://esgf-data1.ceda.ac.uk/thredds/fileServer/esg_cordex/cordex/output/AFR-44i/MOHC/ECMWF-ERAINT/evaluation/r1i1p1/MOHC-HadRM3P/v1/mon/tasmin/v20131211/tasmin_AFR-44i_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc
* http://esgf-data1.ceda.ac.uk/thredds/fileServer/esg_cordex/cordex/output/EUR-44i/MOHC/ECMWF-ERAINT/evaluation/r1i1p1/MOHC-HadRM3P/v1/mon/tas/v20131212/tas_EUR-44i_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc

## C3S_CMIP5

We are using the following file:

http://cp4cds-data1.ceda.ac.uk/thredds/fileServer/esg_c3s-cmip5/output1/MOHC/HadGEM2-ES/historical/mon/atmos/Amon/r1i1p1/tas/v20120928/tas_Amon_HadGEM2-ES_historical_r1i1p1_185912-188411.nc

This file is subsetted by the time-range 1860/01-1860/12 using cdo:

     $ cdo seltimestep,2,3,4,5,6,7,8,9,10,11,12,13 infile outfile
