import pytest

from c4cds.mock_drs import MockDRS

from .common import C3S_CMIP5_NC, ARCHIVE_BASE

FX_NC = "/cmip5/output1/MPI-M/MPI-ESM-P/piControl/fx/atmos/fx/r0i0p0/latest/orog/orog_fx_MPI-ESM-P_piControl_r0i0p0.nc"


def test_mock_drs_cmip5_as_iter():
    m = MockDRS(C3S_CMIP5_NC, archive_base=ARCHIVE_BASE)
    for i in m.as_iter():
        print(i)
    assert m.experiment == 'historical'
    assert m.model == 'HadGEM2-ES'
    assert m.variable_name == 'tas'


def test_mock_drs_cmip5_as_dict():
    m = MockDRS(C3S_CMIP5_NC, archive_base=ARCHIVE_BASE)
    print(m.as_dict())


@pytest.mark.skip(reason='can not handle fx')
def test_mock_drs_fx():
    MockDRS(FX_NC)
