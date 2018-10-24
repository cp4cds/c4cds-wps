import os

from pywps import Process
from pywps import LiteralInput
from pywps import ComplexOutput
from pywps import FORMATS
from pywps import configuration
from pywps.app.Common import Metadata

from c4cds.regridder import Regridder, GLOBAL
from c4cds.search import search_cmip5


class CMIP5Regridder(Process):
    def __init__(self):
        inputs = [
            LiteralInput('model', 'Model',
                         abstract='Choose a model like MPI-ESM-LR.',
                         data_type='string',
                         allowed_values=['HadGEM2-ES', 'MPI-ESM-LR', 'MPI-ESM-MR'],
                         default='HadGEM2-ES'),
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
            LiteralInput('variable', 'Variable',
                         abstract='Choose a variable like tas.',
                         data_type='string',
                         allowed_values=['tas', 'tasmax', 'tasmin'],
                         default='tas'),
            LiteralInput('start_year', 'Start year', data_type='integer',
                         abstract='Start year of model data.',
                         default="1980"),
            LiteralInput('end_year', 'End year', data_type='integer',
                         abstract='End year of model data.',
                         default="1981"),
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
        nc_file = search_cmip5(
            model=request.inputs['model'][0].data,
            experiment=request.inputs['experiment'][0].data,
            ensemble=request.inputs['ensemble'][0].data,
            variable=request.inputs['variable'][0].data,
            start_year=request.inputs['start_year'][0].data,
            end_year=request.inputs['end_year'][0].data,
        )
        regridder = Regridder(
            archive_base=configuration.get_config_value("data", "archive_root"),
            grid_files_dir=configuration.get_config_value("data", "grid_files_dir"),
            output_dir=os.path.join(self.workdir, 'outputs')
        )
        output_file = regridder.regrid(input_file=nc_file, domain_type=GLOBAL)
        response.outputs['output'].file = output_file
        response.update_status("done.", 100)
        return response
