import os

from pywps.tests import WpsClient, WpsTestResponse


def resource_file(filepath):
    return os.path.join(os.path.dirname(__file__), 'resources', filepath)


ARCHIVE_BASE = resource_file('data')
C3S_CMIP5_ARCHIVE_BASE = os.path.join(ARCHIVE_BASE, 'c3s-cmip5', 'output1')
CORDEX_ARCHIVE_BASE = os.path.join(ARCHIVE_BASE, 'cordex', 'output')

C3S_CMIP5_NC = C3S_CMIP5_ARCHIVE_BASE + '/MOHC/HadGEM2-ES/historical/mon/atmos/Amon/r1i1p1/tas/v20120928/tas_Amon_HadGEM2-ES_historical_r1i1p1_186001-186012.nc'  # noqa
CORDEX_NC = CORDEX_ARCHIVE_BASE + "/AFR-44i/MOHC/ECMWF-ERAINT/evaluation/r1i1p1/MOHC-HadRM3P/v1/mon/tasmin/v20131211/tasmin_AFR-44i_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc"  # noqa


def resource_ok(filename):
    return os.path.isfile(filename)


class WpsTestClient(WpsClient):

    def get(self, *args, **kwargs):
        query = "?"
        for key, value in kwargs.items():
            query += "{0}={1}&".format(key, value)
        return super(WpsTestClient, self).get(query)


def client_for(service):
    return WpsTestClient(service, WpsTestResponse)
