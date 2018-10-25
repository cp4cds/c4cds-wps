import os

from pywps import Process
from pywps import LiteralInput
from pywps import ComplexOutput
from pywps import FORMATS
from pywps import configuration
from pywps.app.Common import Metadata

from c4cds.regridder import Regridder, REGIONAL
from c4cds.search import Search

CORDEX_DOMAIN_MAP = {
    'Africa': 'AFR-44i',
    'Europe': 'EUR-44i',
    'UK': 'EUR-44i',
    'France': 'EUR-44i',
    'Germany': 'EUR-44i',
}


class CordexRegridder(Process):
    def __init__(self):
        inputs = [
            LiteralInput('domain', 'Domain',
                         abstract='Choose a regional Domain.',
                         data_type='string',
                         allowed_values=['Africa', 'Europe', 'UK', 'France', 'Germany'],
                         default='Africa'),
            LiteralInput('model', 'Model',
                         abstract='Choose a model like MPI-ESM-LR.',
                         data_type='string',
                         allowed_values=['MOHC-HadRM3P', 'MPI-ESM-LR', 'MPI-ESM-MR'],
                         default='MOHC-HadRM3P'),
            LiteralInput('experiment', 'Experiment',
                         abstract='Choose an experiment like historical.',
                         data_type='string',
                         allowed_values=['evaluation', 'historical', 'rcp26', 'rcp45', 'rcp85'],
                         default='evaluation'),
            LiteralInput('ensemble', 'Ensemble',
                         abstract='Choose an ensemble like r1i1p1.',
                         data_type='string',
                         allowed_values=['r1i1p1', 'r2i1p1', 'r3i1p1'],
                         default='r1i1p1'),
            LiteralInput('variable', 'Variable',
                         abstract='Choose a variable like tas.',
                         data_type='string',
                         allowed_values=['tas', 'tasmax', 'tasmin'],
                         default='tasmin'),
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

        super(CordexRegridder, self).__init__(
            self._handler,
            identifier='cordex_regridder',
            version='1.0',
            title='CORDEX Regridder',
            abstract='CORDEX Regridder using CDO.',
            metadata=[
                Metadata('CP4CDS Portal', 'https://cp4cds.github.io/'),
            ],
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        search = Search(configuration.get_config_value("data", "cordex_archive_root"))
        nc_file = search.search_cordex(
            model=request.inputs['model'][0].data,
            experiment=request.inputs['experiment'][0].data,
            ensemble=request.inputs['ensemble'][0].data,
            variable=request.inputs['variable'][0].data,
            domain=CORDEX_DOMAIN_MAP[request.inputs['domain'][0].data],
            start_year=request.inputs['start_year'][0].data,
            end_year=request.inputs['end_year'][0].data,
        )
        if not nc_file:
            raise Exception("Could not find CORDEX file.")
        regridder = Regridder(
            archive_base=configuration.get_config_value("data", "cordex_archive_root"),
            grid_files_dir=configuration.get_config_value("data", "grid_files_dir"),
            output_dir=os.path.join(self.workdir, 'outputs')
        )
        output_file = regridder.regrid(input_file=nc_file, domain_type=REGIONAL)
        response.outputs['output'].file = output_file
        response.update_status("done.", 100)
        return response
