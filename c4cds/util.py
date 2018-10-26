import os
import shutil
import re
import glob

from netCDF4 import Dataset
from nco import Nco

from c4cds.mock_drs import MockDRS

import logging
LOGGER = logging.getLogger('PYWPS')


def parse_time_period(filepath):
    time_period = os.path.basename(filepath).split('_')[-1]
    time_period = time_period[:-3]  # skip extension .nc
    start, end = time_period.split('-')
    start_year = int(start[:4])
    end_year = int(end[:4])
    return start_year, end_year


def get_variable_name(input_file):
    return os.path.basename(input_file).split("_")[0]


def convert_to_netcdf3(input_file, output_file=None):
    nco = Nco()
    output_file = output_file or input_file
    tmp_file = input_file[:-3] + "-tmp.nc"
    nco.ncks(input=input_file, output=tmp_file, options=['-3'])
    shutil.move(tmp_file, output_file)
    LOGGER.info("Converted to NetCDF3 file: {}".format(output_file))
    return output_file


def map_to_drs(file_path, archive_base=None):
    """
    Maps a file to a MockDRS object - which is returned.
    """
    return MockDRS(file_path, archive_base=archive_base)


def get_grid_cell_area_variable(var_id, path, archive_base=None):
    """
    Looks in the file ``path`` to find the file that contains
    the grid cell areas.

    Returns None if cannot find file.
    """
    LOGGER.debug("Path: {}".format(path))
    ds = Dataset(path)
    if var_id not in ds.variables.keys():
        raise Exception("Cannot find variable '{}' in file '{}'.".format(var_id, path))
    v = ds.variables[var_id]

    try:
        acm = re.search(r'area:\s*(\w+)\s*', v.cell_measures).groups()[0]
        acm_file_name = re.search(r'{}:\s*({}_.+?\.nc)'.format(acm, acm), v.associated_files).groups()[0]
    except Exception:
        LOGGER.warning("Could not locate grid cell area file for '{}' in file '{}'.".format(var_id, path))
        return None

    d = map_to_drs(path, archive_base=archive_base)
    cell_areas_path = os.path.join(
        archive_base, d.activity, d.product, d.institute,
        d.model, d.experiment, "fx", d.modeling_realm, "fx", "r0i0p0",
        "*", acm, acm_file_name)

    files = glob.glob(cell_areas_path)
    if not files:
        LOGGER.warning("Cell areas file not found at: {}".format(cell_areas_path))
        return None
    elif len(files) == 1:
        cell_areas_file = files[0]
    else:
        # TODO: get latest version
        cell_areas_file = files[0]
    return cell_areas_file
