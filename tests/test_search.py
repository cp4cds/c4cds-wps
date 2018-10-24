import pytest

from c4cds import search


@pytest.mark.data
def test_search_cmip5():
    assert 'tas_Amon_HadGEM2-ES_historical_r1i1p1_195912-198411.nc' in search.search_cmip5(
        model='HadGEM2-ES',
        experiment='historical',
        variable='tas',
        start_year=1971,
        end_year=1980
    )
