import os
import tempfile

from netCDF4 import Dataset
from cdo import Cdo

from c4cds import util

# domain types
GLOBAL = 'global'
REGIONAL = 'regional'

import logging
LOGGER = logging.getLogger('PYWPS')


class Regridder(object):
    def __init__(self, output_dir=None, archive_base=None, grid_files_dir=None):
        self.output_base_dir = output_dir or os.path.join(tempfile.gettempdir(), 'out_regrid')
        self.archive_base = archive_base or '/data'
        self.grid_files_dir = grid_files_dir or os.path.join(self.archive_base, 'grid_files')

    def regrid(self, input_file, domain_type):
        # Define some rules regarding the inputs and how they map to information needed by this process
        output_dir = self.create_output_dir(domain_type)
        grid_definition_file = self.get_grid_definition_file(input_file, domain_type)

        # Validate input grid first - check CDO can manage it
        self.validate_input_grid(input_file)

        # Determine output file name
        output_file = os.path.join(output_dir, os.path.basename(input_file))

        # We will need to select the main variable using the "select" operator piped into the CDO operator
        cdo = Cdo()
        var_id = util.get_variable_name(input_file)
        options = "-b F64"
        operation = '-select,name={}'.format(var_id)

        # Get the variable (in external file) that contains the grid cell area variable
        cell_areas_file = util.get_grid_cell_area_variable(var_id, input_file, archive_base=self.archive_base)
        if cell_areas_file:
            operation += " -setgridarea,{}".format(cell_areas_file)
        if domain_type == GLOBAL:
            operation = '-remapbil,{} {}'.format(grid_definition_file, operation)
            cdo.setgridtype('lonlat', input="{} {}".format(operation, input_file),
                            output=output_file, options=options)
        else:
            cdo.remapbil(grid_definition_file,
                         input="{} {}".format(operation, input_file),
                         output=output_file, options=options)

        self.validate_regridded_file(output_file, domain_type)

        if domain_type == REGIONAL:
            util.convert_to_netcdf3(output_file)

        return output_file

    def create_output_dir(self, domain_type=None):
        if domain_type == GLOBAL:
            grid_short_name = "1_deg"
        else:
            grid_short_name = "0.5_deg"
        output_dir = os.path.join(self.output_base_dir, grid_short_name)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        return output_dir

    def get_grid_definition_file(self, input_file, domain_type=None):
        if domain_type == GLOBAL:
            grid_definition_file = os.path.join(self.grid_files_dir, 'll1deg_grid.nc')
        else:
            regional_domain = os.path.basename(input_file).split("_")[1]
            grid_definition_file = os.path.join(self.grid_files_dir, 'll0.5deg_{}.nc'.format(regional_domain))
        return grid_definition_file

    def validate_input_grid(self, input_file):
        _, tmp_file = tempfile.mkstemp()
        cdo = Cdo()
        cdo.timmean(input="-seltimestep,1 {}".format(input_file), output=tmp_file)

        # Analyse the output for the error "generic" meaning that cdo does not recognise the grid which may mean
        # that the file contains no fields, just a time series
        # if outputs["stderr"].replace("\n", "").find("generic") > -1:
        #    raise Exception(
        #        "No spatial grid in this dataset or not recognised grid. Please check the grid in the dataset.")

    def validate_regridded_file(self, input_file, domain_type):
        ds = Dataset(input_file)
        if domain_type == GLOBAL:
            LOGGER.debug("lat={}, lon={}".format(ds.dimensions['lat'].size, ds.dimensions['lon'].size))
            if not(ds.dimensions['lat'].size == 180 and ds.dimensions['lon'].size == 360):
                msg = "Output grid not correct for: {}".format(input_file)
                raise Exception(msg)
        else:
            LOGGER.warning("NOT CHECKING OUTPUT GRID for REGIONAL DATA!")
