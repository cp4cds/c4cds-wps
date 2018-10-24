$ /usr/bin/cdo  remapbil,./grid_files/ll0.5deg_AFR-44i.nc -select,name=tasmin /badc/cordex/data/cordex/output/AFR-44/MOHC/ECMWF-ERAINT/evaluation/r1i1p1/MOHC-HadRM3P/v1/mon/tasmin/v20131211/tasmin_AFR-44_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc OUT/0.5_deg/tasmin_AFR-44_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc

cdo(2) select: Process started
cdo remapbil: Bilinear weights from lonlat (194x201) to lonlat (173x179) grid
cdo(2) select: Processed 467928 values from 1 variable over 12 timesteps
cdo remapbil: Processed 467928 values from 1 variable over 12 timesteps [0.20s 20MB]

$ ncdump -h /badc/cordex/data/cordex/output/AFR-44/MOHC/ECMWF-ERAINT/evaluation/r1i1p1/MOHC-HadRM3P/v1/mon/tasmin/v20131211/tasmin_AFR-44_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc | head -6

netcdf tasmin_AFR-44_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012 {
dimensions:
        time = UNLIMITED ; // (12 currently)
        lat = 201 ;
        lon = 194 ;
        bnds = 2 ;

$ ncdump -h OUT/0.5_deg/tasmin_AFR-44_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc | head -6

netcdf tasmin_AFR-44_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012 {
dimensions:
        time = UNLIMITED ; // (12 currently)
        bnds = 2 ;
        lon = 173 ;
