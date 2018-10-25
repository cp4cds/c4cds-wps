import os
import tempfile
import glob

import logging
LOGGER = logging.getLogger('PYWPS')


class Project():
    def __init__(self, archive_base):
        self.archive_base = archive_base or '/opt/data'

    def search_pattern():
        raise NotImplementedError


class CMIP5(Project):
    def search_pattern(self, experiment=None, ensemble=None, model=None, variable=None):
        # defaults
        model = model or 'HadGEM2-ES'
        experiment = experiment or 'historical'
        ensemble = ensemble or 'r1i1p1'
        variable = variable or 'tas'
        # "/opt/data/cmip5/output1/MOHC/HadGEM2-ES/historical/day/atmos/day/r1i1p1/v20120716/tas/
        pattern = os.path.join(
            self.archive_base,
            'cmip5',
            '*',
            '*',
            model,
            experiment,
            'mon',
            'atmos',
            '*',
            ensemble,
            '*',
            variable,
            '*',
        )
        return pattern


class CORDEX(Project):
    def search_pattern(self, domain, experiment, ensemble, model, variable):
        # defaults
        model = model or 'MOHC-HadRM3P'
        experiment = experiment or 'evaluation'
        ensemble = ensemble or 'r1i1p1'
        variable = variable or 'tasmin'
        domain = domain or 'AFR-44i'
        # /opt/data/cordex/output/AFR-44i/MOHC/ECMWF-ERAINT/evaluation/r1i1p1/MOHC-HadRM3P/v1/mon/tasmin/v20131211/
        pattern = os.path.join(
            self.archive_base,
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


class Search():
    def __init__(self, archive_base):
        self.archive_base = archive_base or '/opt/data'

    def _search(self, pattern):
        # run pattern search
        LOGGER.info("search pattern: {}".format(pattern))
        files = glob.glob(pattern)
        if files:
            LOGGER.info('found cmip5 files: {}', len(files))
            result = files[0]
        else:
            LOGGER.warn("no cmip5 files found.")
            result = None
        return result

    def search_cmip5(self, model=None, experiment=None, ensemble=None, variable=None,
                     start_year=1980, end_year=1981):
        cmip5 = CMIP5(self.archive_base)
        pattern = cmip5.search_pattern(
            experiment=experiment,
            ensemble=ensemble,
            model=model,
            variable=variable)
        return self._search(pattern)

    def search_cordex(self, model=None, experiment=None, ensemble=None, variable=None, domain=None,
                      start_year=1980, end_year=1981):
        cordex = CORDEX(self.archive_base)
        # cordex search pattern
        pattern = cordex.search_pattern(
            domain,
            experiment,
            ensemble,
            model,
            variable)
        return self._search(pattern)
