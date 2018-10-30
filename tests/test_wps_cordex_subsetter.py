import pytest

from pywps import Service
from pywps.tests import assert_response_success

from . common import client_for, resource_file
from c4cds.processes.wps_cordex_subsetter import CordexSubsetter


cfgfiles = [resource_file('test.cfg'), ]


def test_wps_cordex_subsetter_egypt():
    client = client_for(Service(processes=[CordexSubsetter()], cfgfiles=cfgfiles))
    datainputs = "country=Egypt,variable=tasmin"
    resp = client.get(
        service='WPS', request='Execute', version='1.0.0', identifier='cordex_subsetter',
        datainputs=datainputs)
    print(resp.data)
    assert_response_success(resp)


def test_wps_cordex_subsetter_uk():
    client = client_for(Service(processes=[CordexSubsetter()], cfgfiles=cfgfiles))
    datainputs = "country=UK"
    resp = client.get(
        service='WPS', request='Execute', version='1.0.0', identifier='cordex_subsetter',
        datainputs=datainputs)
    print(resp.data)
    assert_response_success(resp)
