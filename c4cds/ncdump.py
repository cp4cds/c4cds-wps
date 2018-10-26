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
        if not isinstance(output, str):
            output = output.decode('utf-8')
        lines = output.split('\n')
        # replace the filename for safety
        dataset_id = os.path.basename(dataset)  # 'uploaded-file'
        lines[0] = 'netcdf %s {' % dataset_id
        # decode to ascii
        filtered_lines = [str(line) + '\n' for line in lines]
    except CalledProcessError as err:
        LOGGER.exception("could not generate ncdump")
        return "Error: generating ncdump failed. Output: {0.output}".format(err)
    return filtered_lines
