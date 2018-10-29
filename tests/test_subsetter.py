import pytest

from c4cds.subsetter import Subsetter

from .common import CORDEX_NC


@pytest.mark.data
def test_subset_by_country():
    subsetter = Subsetter()
    assert 'tasmin_AFR-44i_Egypt_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc' in \
        subsetter.subset_by_country(CORDEX_NC, country='Egypt')
