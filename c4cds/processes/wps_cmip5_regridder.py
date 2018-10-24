import os

from pywps import Process
from pywps import LiteralInput
from pywps import ComplexOutput
from pywps import FORMATS
from pywps import configuration
from pywps.app.Common import Metadata

from c4cds.regridder import Regridder, GLOBAL


TEST_NC = "/opt/data/cmip5/output1/MOHC/HadGEM2-ES/historical/day/atmos/day/r1i1p1/v20120716/tas/tas_day_HadGEM2-ES_historical_r1i1p1_19791201-19891130.nc"  # noqa


class CMIP5Regridder(Process):
    def __init__(self):
        inputs = [
            LiteralInput('grid_type', 'Grid Type',
                         abstract='Choose a Grid Type.',
                         data_type='string',
                         allowed_values=['earth'],
                         default='earth'),
            LiteralInput('model', 'Model',
                         abstract='Choose a model like MPI-ESM-LR.',
                         data_type='string',
                         allowed_values=['MPI-ESM-LR', 'MPI-ESM-MR'],
                         default='MPI-ESM-LR'),
            LiteralInput('experiment', 'Experiment',
                         abstract='Choose an experiment like historical.',
                         data_type='string',
                         allowed_values=['historical', 'rcp26', 'rcp45', 'rcp85'],
                         default='historical'),
            LiteralInput('ensemble', 'Ensemble',
                         abstract='Choose an ensemble like r1i1p1.',
                         data_type='string',
                         allowed_values=['r1i1p1', 'r2i1p1', 'r3i1p1'],
                         default='r1i1p1'),
            LiteralInput('start_year', 'Start year', data_type='integer',
                         abstract='Start year of model data.',
                         default="2000"),
            LiteralInput('end_year', 'End year', data_type='integer',
                         abstract='End year of model data.',
                         default="2001"),
        ]
        outputs = [
            ComplexOutput('output', 'Output',
                          abstract='Regridded NetCDF file.',
                          as_reference=True,
                          supported_formats=[FORMATS.NETCDF]),
        ]

        super(CMIP5Regridder, self).__init__(
            self._handler,
            identifier='cmip5_regridder',
            version='1.0',
            title='CMIP5 Regridder',
            abstract='CMIP5 Regridder using CDO.',
            profile='',
            metadata=[
                Metadata('CP4CDS Portal', 'https://cp4cds.github.io/'),
            ],
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        regridder = Regridder(
            archive_base=configuration.get_config_value("data", "archive_root"),
            grid_files_dir=configuration.get_config_value("data", "grid_files_dir"),
            output_dir=os.path.join(self.workdir, 'outputs')
        )
        output_file = regridder.regrid(input_file=TEST_NC, domain_type=GLOBAL)
        response.outputs['output'].file = output_file
        response.update_status("done.", 100)
        return response