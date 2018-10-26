from .wps_sleep import Sleep
from .wps_cmip5_regridder import CMIP5Regridder
from .wps_cordex_subsetter import CordexSubsetter

processes = [
    Sleep(),
    CMIP5Regridder(),
    CordexSubsetter(),
]
