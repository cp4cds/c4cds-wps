import pytest

from pywps import Service
from pywps.tests import assert_response_success

from . common import client_for
from c4cds.processes.wps_cmip5_regridder import CMIP5Regridder


@pytest.mark.data
def test_wps_cmip5_regridder():
    client = client_for(Service(processes=[CMIP5Regridder()]))
    datainputs = "model=HadGEM2-ES"
    resp = client.get(
        service='WPS', request='Execute', version='1.0.0', identifier='cmip5_regridder',
        datainputs=datainputs)
    print(resp.data)
    assert_response_success(resp)
