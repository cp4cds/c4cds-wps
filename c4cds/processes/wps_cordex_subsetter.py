import os

from pywps import Process
from pywps import LiteralInput
from pywps import ComplexOutput
from pywps import FORMATS, Format
from pywps import configuration
from pywps.app.Common import Metadata

from c4cds.regridder import Regridder, REGIONAL
from c4cds.subsetter import Subsetter
from c4cds.plotter import Plotter
from c4cds.search import Search
from c4cds.ncdump import ncdump
from c4cds import util

CORDEX_DOMAIN_MAP = {
    'Egypt': 'AFR-44i',
    'UK': 'EUR-44i',
    'France': 'EUR-44i',
    'Germany': 'EUR-44i',
}


class CordexSubsetter(Process):
    def __init__(self):
        inputs = [
            LiteralInput('country', 'Country',
                         abstract='Choose a Country like UK.',
                         data_type='string',
                         allowed_values=['Egypt', 'UK', 'France', 'Germany'],
                         default='Egypt'),
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
            ComplexOutput('output', 'Subsetted Dataset',
                          abstract='Subsetted Dataset.',
                          as_reference=True,
                          supported_formats=[FORMATS.NETCDF]),
            ComplexOutput('ncdump', 'Metadata',
                          abstract='ncdump of subsetted Dataset.',
                          as_reference=True,
                          supported_formats=[FORMATS.TEXT]),
            ComplexOutput('preview', 'Preview',
                          abstract='Preview of subsetted Dataset.',
                          as_reference=True,
                          supported_formats=[Format('image/png')]),
        ]

        super(CordexSubsetter, self).__init__(
            self._handler,
            identifier='cordex_subsetter',
            version='1.0',
            title='CORDEX Subsetter',
            abstract='CORDEX Subsetter using CDO.',
            metadata=[
                Metadata('CP4CDS Portal', 'https://cp4cds.github.io/'),
                Metadata('Documentation',
                         'https://c4cds-wps.readthedocs.io/en/latest/processes.html#cordex_subsetter',
                         role=util.WPS_ROLE_DOC),
                Metadata('Media',
                         'https://c4cds-wps.readthedocs.io/en/latest/_static/media/cordex_subsetter_thumbnail.png',
                         role=util.WPS_ROLE_MEDIA),
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
            domain=CORDEX_DOMAIN_MAP[request.inputs['country'][0].data],
            start_year=request.inputs['year'][0].data,
            end_year=request.inputs['year'][0].data,
        )
        if not nc_file:
            raise Exception("Could not find CORDEX file.")
        response.update_status('search done.', 10)
        # regridding
        regridder = Regridder(
            archive_base=configuration.get_config_value("data", "cordex_archive_root"),
            grid_files_dir=configuration.get_config_value("data", "grid_files_dir"),
            output_dir=os.path.join(self.workdir, 'out_regrid')
        )
        regridded_file = regridder.regrid(input_file=nc_file, domain_type=REGIONAL)
        response.update_status('regridding done.', 60)
        # subset by country
        subsetter = Subsetter(
            output_dir=os.path.join(self.workdir, 'out_subset')
        )
        subsetted_file = subsetter.subset_by_country(
            regridded_file,
            country=request.inputs['country'][0].data)
        response.outputs['output'].file = subsetted_file
        response.update_status('subsetting done.', 70)
        # plot preview
        title = "{} {} {} {} {}".format(
            request.inputs['country'][0].data,
            request.inputs['model'][0].data,
            request.inputs['experiment'][0].data,
            request.inputs['variable'][0].data,
            request.inputs['year'][0].data,
        )
        plotter = Plotter(
            output_dir=os.path.join(self.workdir, 'out_plot')
        )
        preview_file = plotter.plot_preview(subsetted_file, title)
        response.outputs['preview'].file = preview_file
        response.update_status('plot done.', 80)
        # run ncdump
        with open(os.path.join(self.workdir, "nc_dump.txt"), 'w') as fp:
            response.outputs['ncdump'].file = fp.name
            fp.writelines(ncdump(subsetted_file))
            response.update_status('ncdump done.', 90)
        # done
        response.update_status("done.", 100)
        return response
