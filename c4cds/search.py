import os
import tempfile
import glob
from pywps import configuration

import logging
LOGGER = logging.getLogger('PYWPS')

# init climaf
os.environ['CLIMAF_CACHE'] = os.path.join(tempfile.gettempdir(), 'climaf_cache')
os.environ['CLIMAF_LOG_DIR'] = tempfile.gettempdir()

from climaf.api import ds
from climaf.dataloc import dataloc


def search_cmip5(model=None, experiment=None, ensemble=None, variable=None, start_year=1980, end_year=1981):
    # defaults
    model = model or 'HadGEM2-ES'
    experiment = experiment or 'historical'
    ensemble = ensemble or 'r1i1p1'
    variable = variable or 'tas'
    # Set data location to CMIP5 archive on local file system
    cmip5_path = configuration.get_config_value("data", "archive_root")
    LOGGER.info("CMIP5 data path: %s", cmip5_path)
    dataloc(project="CMIP5", organization="CMIP5_DRS", url=[cmip5_path])
    # Define a dataset selection from the CMIP5 project, using user inputs
    dset = ds(project='CMIP5', model=model, experiment=experiment, frequency='monthly',
              variable=variable, period='{}-{}'.format(start_year, end_year))
    files = dset.baseFiles()
    if files:
        result = files.split()[0]
    else:
        result = None
    return result


# "/opt/data/cordex/output/AFR-44i/MOHC/ECMWF-ERAINT/evaluation/r1i1p1/MOHC-HadRM3P/v1/mon/tasmin/v20131211/
#     tasmin_AFR-44i_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc"
def search_cordex(model=None, experiment=None, ensemble=None, variable=None, domain=None,
                  start_year=1980, end_year=1981):
    # defaults
    model = model or 'MOHC-HadRM3P'
    experiment = experiment or 'evaluation'
    ensemble = ensemble or 'r1i1p1'
    variable = variable or 'tasmin'
    domain = domain or 'AFR-44i'
    # remap domain
    if domain == 'Africa':
        domain = 'AFR-44i'
    # Set data location to CMIP5 archive on local file system
    root_path = configuration.get_config_value("data", "archive_root")
    # cordex search pattern
    pattern = cordex_search_pattern(
        root_path,
        domain,
        experiment,
        ensemble,
        model,
        variable)
    # run pattern search
    LOGGER.info("search cordex: {}".format(pattern))
    files = glob.glob(pattern)
    if files:
        LOGGER.info('found cordex files: {}', len(files))
        result = files[0]
    else:
        LOGGER.warn("no cordex files found.")
        result = None
    return result


def cordex_search_pattern(root_path, domain, experiment, ensemble, model, variable):
    # file_pattern = '{}_{}_*_{}_{}_{}_*_mon_{}_*-*.nc'.format(variable, domain, experiment, ensemble, model, variable)
    pattern = os.path.join(
        root_path,
        'cordex',
        '*',
        domain,
        '*',
        '*',
        experiment,
        ensemble,
        model,
        '*',
        'mon',
        variable,
        '*',
        '*',
    )
    return pattern
