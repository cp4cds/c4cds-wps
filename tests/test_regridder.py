import pytest

import os

from c4cds.regridder import Regridder, GLOBAL, REGIONAL

from .common import C3S_CMIP5_NC, CORDEX_NC, ARCHIVE_BASE, resource_ok


def test_create_output_dir():
    regridder = Regridder()
    assert 'out_regrid/1_deg' in regridder.create_output_dir(domain_type=GLOBAL)
    assert 'out_regrid/0.5_deg' in regridder.create_output_dir(domain_type=REGIONAL)


def test_get_grid_definition_file():
    regridder = Regridder(archive_base=ARCHIVE_BASE)
    assert 'grid_files/ll1deg_grid.nc' in regridder.get_grid_definition_file(
        C3S_CMIP5_NC, domain_type=GLOBAL)
    assert 'grid_files/ll0.5deg_AFR-44i.nc' in regridder.get_grid_definition_file(
        CORDEX_NC, domain_type=REGIONAL)


@pytest.mark.skipif(not resource_ok(CORDEX_NC),
                    reason="Test data not available.")
def test_validate_input_grid():
    regridder = Regridder(archive_base=ARCHIVE_BASE)
    regridder.validate_input_grid(CORDEX_NC)


@pytest.mark.skipif(not resource_ok(CORDEX_NC),
                    reason="Test data not available.")
def test_validate_regridded_file_cordex():
    regridder = Regridder(archive_base=ARCHIVE_BASE)
    regridder.validate_regridded_file(CORDEX_NC, REGIONAL)


@pytest.mark.skip(reason='no regridded file')
def test_validate_regridded_file_cmip5():
    regridder = Regridder(archive_base=ARCHIVE_BASE)
    regridder.validate_regridded_file(C3S_CMIP5_NC, GLOBAL)


@pytest.mark.skip(reason="no grid file for CORDEX.")
def test_regrid_cordex():
    regridder = Regridder(archive_base=ARCHIVE_BASE)
    assert '0.5_deg/tasmin_AFR-44i_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc' \
        in regridder.regrid(CORDEX_NC, REGIONAL)


@pytest.mark.skipif(not resource_ok(C3S_CMIP5_NC),
                    reason="Test data not available.")
def test_regrid_cmip5():
    regridder = Regridder(archive_base=ARCHIVE_BASE)
    assert '1_deg/tas_Amon_HadGEM2-ES_historical_r1i1p1_186001-186012.nc' \
        in regridder.regrid(C3S_CMIP5_NC, GLOBAL)
