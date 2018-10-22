from .wps_sleep import Sleep
from .wps_cmip5_regridder import CMIP5Regridder

processes = [
    Sleep(),
    CMIP5Regridder(),
]
