"""
mock_drs.py
===========

Holds the MockDRS class for handling DRS interactions.

"""

# Standard library imports
import os

import logging
LOGGER = logging.getLogger('PYWPS')


class MockDRS(object):
    "A simple object to hold a DRS structure mapping."

    __slots__ = ["activity", "product", "institute", "model", "experiment", "frequency",
                 "modeling_realm", "MIP_table", "ensemble_member", "variable_name", "version_number",
                 "time_range", "extension", "_archive_base"]

    def __init__(self, fpath, archive_base=None):
        self._archive_base = archive_base or '/tmp/data'
        LOGGER.info("Analysing DRS from: {}".format(fpath))
        self._interpret(fpath)

    def _interpret(self, fpath):
        (dr, fn) = os.path.split(fpath)
        allowed = self.__slots__[:-2]

        # Get from archive DRS strcture and filename if found
        if fpath.find(self._archive_base) == 0:
            items = dr.replace(self._archive_base, "").strip("/").split("/")

            if len(items) != len(allowed) - 1:
                raise Exception("Incorrect number of items in analysed DRS: required are: {}; Found are: {}".format(
                    allowed[:-1], items))

            # Now populate this object with keys from DRS
            for (i, key) in enumerate(allowed[:-1]):
                try:
                    setattr(self, key, items[i])
                except Exception:
                    raise KeyError("Cannot identify section '%s' in file path." % key)

            # Now validate file name and directory use the same DRS values
            fname_dict = self._split_filename(fn)

            for key in ("variable_name", "MIP_table", "model", "experiment", "ensemble_member"):
                if fname_dict[key] != getattr(self, key):
                    raise ValueError("DRS component in path does not match DRS component in file name: '{}' != '{}'.".format(  # noqa
                        fname_dict[key], getattr(self, key)))

            # Add some properties from file name
            for key in ("time_range", "extension"):
                try:
                    setattr(self, key, fname_dict[key])
                except Exception:
                    raise KeyError("Cannot identify section '%s' in file path." % key)

        # Or get from file only named after DRS structure
        else:
            items = fn.split(".")[:-1]

            for (i, key) in enumerate(allowed):
                setattr(self, key, items[i])

            setattr(self, "extension", ".".join(items[(i + 1):]).strip("."))

    def _split_filename(self, fname):
        """
        Splits the NetCDF file and returns sections as dictionary with keys:
           (variable_name, MIP_table, model, experiment, ensemble_member, extension, time_range).
        """
        keys = ("variable_name", "MIP_table", "model", "experiment", "ensemble_member", "time_range")
        d = {"extension": ""}

        if fname[-3:] != ".nc":
            raise Exception("Incorrect file extension. Expected NetCDEF '.nc' extension but found: '%s'." % fname[-3:])

        for (i, found) in enumerate(fname[:-3].split("_")):
            if i < len(keys):
                d[keys[i]] = found
            else:
                d["extension"] += "_" + found

        d["extension"] = d["extension"].strip("_")
        return d

    def as_string(self, sep="."):
        return sep.join([getattr(self, key) for key in self.__slots__]).strip(sep)

    def as_dict(self):
        return dict([(key, getattr(self, key)) for key in self.__slots__])

    def as_iter(self):
        for key in self.__slots__:
            yield (key, getattr(self, key))

    def __repr__(self):
        resp = {}
        for key in self.__slots__:
            resp[key] = getattr(self, key, None)

        return str(resp)
