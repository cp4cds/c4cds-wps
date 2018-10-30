import pytest

from c4cds.subsetter import Subsetter

from .common import CORDEX_NC, resource_ok


@pytest.mark.skipif(not resource_ok(CORDEX_NC),
                    reason="Test data not available.")
def test_subset_by_country_egypt():
    subsetter = Subsetter()
    assert 'tasmin_AFR-44i_Egypt_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc' in \
        subsetter.subset_by_country(CORDEX_NC, country='Egypt')
