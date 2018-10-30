import six
import os
from subprocess import check_output, CalledProcessError

import logging
LOGGER = logging.getLogger('PYWPS')


def ncdump(dataset):
    '''
    Returns the metadata of the dataset

    Code taken from https://github.com/ioos/compliance-checker-web
    '''

    try:
        output = check_output(['ncdump', '-h', dataset])
        if not isinstance(output, six.string_types):
            output = output.decode('utf-8')
        lines = output.split('\n')
        # replace the filename for safety
        dataset_id = os.path.basename(dataset)  # 'uploaded-file'
        lines[0] = 'netcdf {} {{'.format(dataset_id)
        # decode to ascii
        filtered_lines = ['{}\n'.format(line) for line in lines]
    except Exception as err:
        LOGGER.error("Could not generate ncdump: {}".format(err))
        return "Error: generating ncdump failed"
    return filtered_lines
