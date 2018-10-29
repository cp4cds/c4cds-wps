from pywps.tests import WpsClient, WpsTestResponse

ARCHIVE_BASE = '/opt/data'

C3S_CMIP5_NC = '/opt/data/c3s-cmip5/output1/MOHC/HadGEM2-ES/historical/mon/atmos/Amon/r1i1p1/tas/v20120928/tas_Amon_HadGEM2-ES_historical_r1i1p1_185912-188411.nc'  # noqa
# CMIP5_NC = "/opt/data/cmip5/output1/MOHC/HadGEM2-ES/historical/day/atmos/day/r1i1p1/v20120716/tas/tas_day_HadGEM2-ES_historical_r1i1p1_19791201-19891130.nc"  # noqa
CORDEX_NC = "/opt/data/cordex/output/AFR-44i/MOHC/ECMWF-ERAINT/evaluation/r1i1p1/MOHC-HadRM3P/v1/mon/tasmin/v20131211/tasmin_AFR-44i_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc"  # noqa


class WpsTestClient(WpsClient):

    def get(self, *args, **kwargs):
        query = "?"
        for key, value in kwargs.items():
            query += "{0}={1}&".format(key, value)
        return super(WpsTestClient, self).get(query)


def client_for(service):
    return WpsTestClient(service, WpsTestResponse)
