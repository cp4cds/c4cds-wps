import os
import tempfile
from pywps import configuration

import logging
LOGGER = logging.getLogger('PYWPS')

# init climaf
os.environ['CLIMAF_CACHE'] = os.path.join(tempfile.gettempdir(), 'climaf_cache')
# os.environ['CLIMAF_LOG_DIR'] = tempfile.gettempdir()

from climaf.api import ds
from climaf.dataloc import dataloc


def search_cmip5(model=None, experiment=None, ensemble=None, variable=None, start_year=1980, end_year=1981):
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
