import pytest

from c4cds import util

from .common import CORDEX_NC, C3S_CMIP5_NC, C3S_CMIP5_ARCHIVE_BASE, CORDEX_ARCHIVE_BASE, resource_ok


def test_guess_variable_name():
    assert util.guess_variable_name(CORDEX_NC) == 'tasmin'
    assert util.guess_variable_name(C3S_CMIP5_NC) == 'tas'


def test_cordex_country_drs_filename():
    assert util.cordex_country_drs_filename(CORDEX_NC, country='Egypt') == \
        'tasmin_AFR-44i_Egypt_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc'


def test_parse_time_period():
    assert util.parse_time_period(
        '/path/to/tas_Amon_HadGEM2-ES_historical_r1i1p1_195912-198411.nc'
    ) == (1959, 1984)
    assert util.parse_time_period(
        '/path/to/tasmin_AFR-44i_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc'
    ) == (1990, 1990)
    assert util.parse_time_period(
        '/path/to/tasmin_AFR-44i_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_day_19900101-19901231.nc'
    ) == (1990, 1990)


def test_get_variable_name():
    assert util.get_variable_name(CORDEX_NC) == 'tasmin'
    assert util.get_variable_name(C3S_CMIP5_NC) == 'tas'


@pytest.mark.skipif(not resource_ok(CORDEX_NC),
                    reason="Test data not available.")
def test_convert_to_netcdf3():
    assert util.convert_to_netcdf3(CORDEX_NC, output_file='/tmp/test.nc') == '/tmp/test.nc'


def test_map_to_drs_cmip5():
    assert util.map_to_drs(C3S_CMIP5_NC, archive_base=C3S_CMIP5_ARCHIVE_BASE) is not None


@pytest.mark.skip(reason='not working')
def test_get_grid_cell_area_variable_cordex():
    assert util.get_grid_cell_area_variable(
        var_id='tasmin',
        path=CORDEX_NC,
        archive_base=CORDEX_ARCHIVE_BASE) is not None


@pytest.mark.skip(reason='no fx in c3s-cmip5')
def test_get_grid_cell_area_variable_cmip5():
    assert util.get_grid_cell_area_variable(
        var_id='tas',
        path=C3S_CMIP5_NC,
        archive_base=C3S_CMIP5_ARCHIVE_BASE) == \
        '/opt/data/c3s-cmip5/output1/MOHC/HadGEM2-ES/historical/fx/atmos/fx/r0i0p0/latest/areacella/areacella_fx_HadGEM2-ES_historical_r0i0p0.nc'  # noqa
