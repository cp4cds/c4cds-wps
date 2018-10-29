import pytest

from .common import CORDEX_NC

from c4cds.plotter import Plotter


@pytest.mark.data
def test_plot_preview():
    plotter = Plotter()
    plotter.plot_preview(CORDEX_NC)
