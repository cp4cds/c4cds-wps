import os
import tempfile
import glob

from c4cds import util

import logging
LOGGER = logging.getLogger('PYWPS')


class Project():
    def __init__(self, archive_base):
        self.archive_base = archive_base or '/data'

    def search_pattern():
        raise NotImplementedError


class C3S_CMIP5(Project):
    def search_pattern(self, experiment=None, ensemble=None, model=None, variable=None):
        # defaults
        model = model or 'HadGEM2-ES'
        experiment = experiment or 'historical'
        ensemble = ensemble or 'r1i1p1'
        variable = variable or 'tas'
        version = '*'
        # "/opt/data/c3s-cmip5/output1/
        #        MOHC/HadGEM2-ES/historical/day/atmos/day/r1i1p1/v20120716/tas/
        pattern = os.path.join(
            self.archive_base,
            '*',
            model,
            experiment,
            'mon',
            'atmos',
            '*',
            ensemble,
            variable,
            version,
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
        # /opt/data/cordex/output/
        #      AFR-44i/MOHC/ECMWF-ERAINT/evaluation/r1i1p1/MOHC-HadRM3P/v1/mon/tasmin/v20131211/
        pattern = os.path.join(
            self.archive_base,
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


def filter_by_year(files, start_year=None, end_year=None):
    result = []
    for filepath in files:
        try:
            f_start_year, f_end_year = util.parse_time_period(filepath)
        except Exception:
            LOGGER.warn("could not parse time period: {}".format(filepath))
            continue
        if end_year is not None and end_year < f_start_year:
            continue
        elif start_year is not None and start_year > f_end_year:
            continue
        else:
            result.append(filepath)
    return result


class Search():
    def __init__(self, archive_base):
        self.archive_base = archive_base or '/data'

    def _search(self, pattern, start_year=None, end_year=None):
        # run pattern search
        LOGGER.info("search pattern: {}".format(pattern))
        files = glob.glob(pattern)
        if files:
            files = filter_by_year(files, start_year, end_year)
            LOGGER.info('found files: {}', len(files))
        if files:
            result = files[0]
        if not files:
            LOGGER.warning("no files found.")
            result = None
        return result

    def search_cmip5(self, model=None, experiment=None, ensemble=None, variable=None,
                     start_year=None, end_year=None):
        cmip5 = C3S_CMIP5(self.archive_base)
        pattern = cmip5.search_pattern(
            experiment=experiment,
            ensemble=ensemble,
            model=model,
            variable=variable)
        return self._search(pattern, start_year, end_year)

    def search_cordex(self, model=None, experiment=None, ensemble=None, variable=None, domain=None,
                      start_year=None, end_year=None):
        cordex = CORDEX(self.archive_base)
        # cordex search pattern
        pattern = cordex.search_pattern(
            domain,
            experiment,
            ensemble,
            model,
            variable)
        return self._search(pattern, start_year, end_year)
