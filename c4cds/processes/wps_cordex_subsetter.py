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
    'Cairo': 'AFR-44i',
    'UK': 'EUR-44i',
    'France': 'EUR-44i',
    'Germany': 'EUR-44i',
}


class CordexSubsetter(Process):
    def __init__(self):
        inputs = [
            LiteralInput('region', 'Region',
                         abstract='Choose a Country like UK.',
                         data_type='string',
                         allowed_values=['Cairo', 'UK', 'France', 'Germany'],
                         default='Cairo'),
            LiteralInput('model', 'Model',
                         abstract='Choose a model like MOHC-HadRM3P.',
                         data_type='string',
                         allowed_values=['MOHC-HadRM3P'],
                         default='MOHC-HadRM3P'),
            LiteralInput('experiment', 'Experiment',
                         abstract='Choose an experiment like evaluation.',
                         data_type='string',
                         allowed_values=['evaluation'],
                         default='evaluation'),
            LiteralInput('variable', 'Variable',
                         abstract='Choose a variable like tas.',
                         data_type='string',
                         allowed_values=['tas', 'tasmax', 'tasmin'],
                         default='tasmin'),
            LiteralInput('year', 'Match year', data_type='integer',
                         abstract='File should match this year.',
                         allowed_values=[1990, 2000, 2010],
                         default="1990"),
        ]
        outputs = [
            ComplexOutput('output', 'Output',
                          abstract='Regridded NetCDF file.',
                          as_reference=True,
                          supported_formats=[FORMATS.NETCDF]),
        ]

        super(CordexSubsetter, self).__init__(
            self._handler,
            identifier='cordex_subsetter',
            version='1.0',
            title='CORDEX Subsetter',
            abstract='CORDEX Subsetter using CDO.',
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
            variable=request.inputs['variable'][0].data,
            domain=CORDEX_DOMAIN_MAP[request.inputs['region'][0].data],
            start_year=request.inputs['year'][0].data,
            end_year=request.inputs['year'][0].data,
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