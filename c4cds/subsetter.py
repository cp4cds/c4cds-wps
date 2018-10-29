import os
import tempfile

from cdo import Cdo

from c4cds.util import cordex_country_drs_filename

COUNTRY_BBOX = {
    # bbox: min_lon, max_lon, min_lat, max_lat
    'Egypt': '13,37,5,50.861',
}


class Subsetter(object):
    def __init__(self, output_dir=None):
        self.output_dir = output_dir or '/tmp/out'
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)

    def subset_by_country(self, dataset, country):
        if country not in COUNTRY_BBOX:
            raise Exception("Unknown country: {}".format(country))
        bbox = COUNTRY_BBOX[country]
        outfile = os.path.join(
            self.output_dir,
            cordex_country_drs_filename(dataset, country))
        cdo = Cdo()
        cdo.sellonlatbox(bbox, input=dataset, output=outfile)
        return outfile
