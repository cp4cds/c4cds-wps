import pytest

from c4cds import search

from .common import ARCHIVE_BASE


@pytest.mark.data
def test_search_cmip5():
    assert 'tas_Amon_HadGEM2-ES_historical_r1i1p1_195912-198411.nc' in search.search_cmip5(
        model='HadGEM2-ES',
        experiment='historical',
        variable='tas',
        start_year=1971,
        end_year=1980
    )


@pytest.mark.data
def test_search_cordex():
    assert 'tasmin_AFR-44i_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc' in search.search_cordex(
        model='MOHC-HadRM3P',
        domain='AFR-44i',
        experiment='evaluation',
        variable='tasmin'
    )


def test_cordex_search_pattern():
    assert search.cordex_search_pattern(
        root_path=ARCHIVE_BASE,
        domain='AFR-44i',
        experiment='evaluation',
        ensemble='r1i1p1',
        model='MOHC-HadRM3P',
        variable='tasmin'
    ) == '/opt/data/cordex/*/AFR-44i/*/*/evaluation/r1i1p1/MOHC-HadRM3P/*/mon/tasmin/*/*'
