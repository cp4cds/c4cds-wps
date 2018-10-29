import pytest

from pywps import Service
from pywps.tests import assert_response_success

from . common import client_for
from c4cds.processes.wps_cordex_subsetter import CordexSubsetter


@pytest.mark.data
def test_wps_cordex_subsetter():
    client = client_for(Service(processes=[CordexSubsetter()]))
    datainputs = "domain=Egypt"
    resp = client.get(
        service='WPS', request='Execute', version='1.0.0', identifier='cordex_subsetter',
        datainputs=datainputs)
    print(resp.data)
    assert_response_success(resp)
