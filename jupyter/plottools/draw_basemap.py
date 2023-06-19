from mpl_toolkits.basemap import Basemap
import numpy


def draw_basemap(basemap: Basemap) -> None:
    """
    Description
    -----------

    """

    basemap.drawcoastlines(color="lightgray", linewidth=0.25)
    basemap.drawmeridians(color="black", meridians=numpy.arange(0.0, 360.01, 30.0),
                          labels=[False, False, True, True], linewidth=0.1, dashes=[10, 10],
                          fontsize=8)
    basemap.drawparallels(color="black", circles=numpy.arange(-80.0, 80.01, 40.0),
                          labels=[True, True, False, False], linewidth=0.1, dashes=[10, 10],
                          fontsize=8)
    basemap.fillcontinents(color="lightgray")
