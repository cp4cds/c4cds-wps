import pytest

from .common import CORDEX_NC, resource_ok

from c4cds.plotter import Plotter


@pytest.mark.skipif(not resource_ok(CORDEX_NC),
                    reason="Test data not available.")
def test_plot_preview():
    plotter = Plotter()
    plotter.plot_preview(CORDEX_NC)
