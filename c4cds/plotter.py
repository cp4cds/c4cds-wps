import os

import cartopy.crs as ccrs
from cartopy import config

from netCDF4 import Dataset

from c4cds.util import guess_variable_name

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt  # noqa: E402


class Plotter(object):
    def __init__(self, output_dir=None):
        self.output_dir = output_dir or '/tmp/out'
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)
        config['data_dir'] = self.output_dir

    def plot_preview(self, filename, title=None):
        ds = Dataset(filename)
        timestep = 0
        variable = guess_variable_name(filename)
        # values
        values = ds.variables[variable][timestep, :, :]
        lats = ds.variables['lat'][:]
        lons = ds.variables['lon'][:]
        # axxis
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.coastlines()
        ax.set_global()
        # plot
        plt.contourf(lons, lats, values, 60, transform=ccrs.PlateCarree())
        # Save the plot by calling plt.savefig() BEFORE plt.show()
        plot_name = os.path.basename(filename)
        title = title or plot_name
        output = os.path.join(self.output_dir, plot_name[:-3] + ".png")
        plt.title(title)
        plt.savefig(output)
        plt.show()
        plt.close()
        return output
