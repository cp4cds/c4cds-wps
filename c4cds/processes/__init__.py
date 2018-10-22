from .wps_sleep import Sleep
from .wps_cmip5_regridder import CMIP5Regridder
from .wps_cordex_regridder import CordexRegridder

processes = [
    Sleep(),
    CMIP5Regridder(),
    CordexRegridder(),
]
