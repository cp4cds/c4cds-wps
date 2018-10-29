import os

from pywps import Process
from pywps import LiteralInput
from pywps import ComplexOutput
from pywps import FORMATS, Format
from pywps import configuration
from pywps.app.Common import Metadata

from c4cds.regridder import Regridder, GLOBAL
from c4cds.plotter import Plotter
from c4cds.search import Search
from c4cds.ncdump import ncdump


class CMIP5Regridder(Process):
    def __init__(self):
        inputs = [
            LiteralInput('model', 'Model',
                         abstract='Choose a model like HadGEM2-ES.',
                         data_type='string',
                         allowed_values=['HadGEM2-ES',
                                         'IPSL-CM5A-MR',
                                         'MPI-ESM-MR'],
                         default='HadGEM2-ES'),
            LiteralInput('experiment', 'Experiment',
                         abstract='Choose an experiment like historical.',
                         data_type='string',
                         allowed_values=['historical', 'rcp26'],
                         default='historical'),
            LiteralInput('variable', 'Variable',
                         abstract='Choose a variable like tas.',
                         data_type='string',
                         allowed_values=['pr', 'tas', 'tasmax', 'tasmin'],
                         default='tas'),
            # LiteralInput('year', 'Match year', data_type='integer',
            #              abstract='File should match this year.',
            #              default="1980"),
        ]
        outputs = [
            ComplexOutput('output', 'Regridded Dataset',
                          abstract='Regridded Dataset.',
                          as_reference=True,
                          supported_formats=[FORMATS.NETCDF]),
            ComplexOutput('ncdump', 'Metadata',
                          abstract='ncdump of regridded Dataset.',
                          as_reference=True,
                          supported_formats=[FORMATS.TEXT]),
            ComplexOutput('preview', 'Preview',
                          abstract='Preview of subsetted Dataset.',
                          as_reference=True,
                          supported_formats=[Format('image/png')]),
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
        search = Search(configuration.get_config_value("data", "c3s_cmip5_archive_root"))
        nc_file = search.search_cmip5(
            model=request.inputs['model'][0].data,
            experiment=request.inputs['experiment'][0].data,
            variable=request.inputs['variable'][0].data,
            # start_year=request.inputs['year'][0].data,
            # end_year=request.inputs['year'][0].data,
        )
        if not nc_file:
            raise Exception("Could not find CMIP5 file.")
        response.update_status('search done.', 10)
        # regridding
        regridder = Regridder(
            archive_base=configuration.get_config_value("data", "c3s_cmip5_archive_root"),
            grid_files_dir=configuration.get_config_value("data", "grid_files_dir"),
            output_dir=os.path.join(self.workdir, 'outputs')
        )
        regridded_file = regridder.regrid(input_file=nc_file, domain_type=GLOBAL)
        response.outputs['output'].file = regridded_file
        response.update_status('regridding done.', 60)
        # plot preview
        title = "{} {} {}".format(
            request.inputs['model'][0].data,
            request.inputs['experiment'][0].data,
            request.inputs['variable'][0].data,
            # request.inputs['year'][0].data,
        )
        plotter = Plotter(
            output_dir=os.path.join(self.workdir, 'out_plot')
        )
        preview_file = plotter.plot_preview(regridded_file, title)
        response.outputs['preview'].file = preview_file
        response.update_status('plot done.', 80)
        # run ncdump
        with open(os.path.join(self.workdir, "nc_dump.txt"), 'w') as fp:
            response.outputs['ncdump'].file = fp.name
            fp.writelines(ncdump(regridded_file))
            response.update_status('ncdump done.', 90)
        # done
        response.update_status("done.", 100)
        return response
