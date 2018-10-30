import pytest

from c4cds.search import Search, C3S_CMIP5, CORDEX
from c4cds.search import filter_by_year

from .common import ARCHIVE_BASE, C3S_CMIP5_NC, CORDEX_NC, resource_ok


def test_filter_by_year():
    results = filter_by_year(
        ['/path/to/tas_Amon_HadGEM2-ES_historical_r1i1p1_196001-196912.nc',
         '/path/to/tas_Amon_HadGEM2-ES_historical_r1i1p1_197001-197912.nc'],
        1970, 1970)
    assert len(results) == 1


def test_c3s_cmip5_search_pattern():
    cmip5 = C3S_CMIP5(ARCHIVE_BASE)
    assert cmip5.search_pattern(
        model='HadGEM2-ES',
        experiment='historical',
        ensemble='r1i1p1',
        variable='tas',
    ) == ARCHIVE_BASE + '/c3s-cmip5/*/*/HadGEM2-ES/historical/mon/atmos/*/r1i1p1/tas/*/*'


@pytest.mark.skipif(not resource_ok(C3S_CMIP5_NC),
                    reason="Test data not available.")
def test_search_c3s_cmip5():
    search = Search(ARCHIVE_BASE)
    assert 'tas_Amon_HadGEM2-ES_historical_r1i1p1_186001-186012.nc' in search.search_cmip5(
        model='HadGEM2-ES',
        experiment='historical',
        variable='tas',
        start_year=1860,
        end_year=1861
    )


def test_cordex_search_pattern():
    cordex = CORDEX(ARCHIVE_BASE)
    assert cordex.search_pattern(
        domain='AFR-44i',
        experiment='evaluation',
        ensemble='r1i1p1',
        model='MOHC-HadRM3P',
        variable='tasmin'
    ) == ARCHIVE_BASE + '/cordex/*/AFR-44i/*/*/evaluation/r1i1p1/MOHC-HadRM3P/*/mon/tasmin/*/*'


@pytest.mark.skipif(not resource_ok(CORDEX_NC),
                    reason="Test data not available.")
def test_search_cordex():
    search = Search(ARCHIVE_BASE)
    assert 'tasmin_AFR-44i_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc' in search.search_cordex(
        model='MOHC-HadRM3P',
        domain='AFR-44i',
        experiment='evaluation',
        variable='tasmin'
    )
