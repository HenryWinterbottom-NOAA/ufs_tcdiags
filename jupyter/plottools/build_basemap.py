from mpl_toolkits.basemap import Basemap
import numpy


def build_basemap(lat: numpy.array, lon: numpy.array, resolution: str = "c",
                  projection: str = "cyl", llcrnrlat: float = -90.0,
                  llcrnrlon: float = 0.0, urcrnrlat: float = 90.0,
                  urcrnrlon: float = 360.0) -> Basemap:
    """
    Description
    -----------

    """

    # Define the basemap attributes and return.
    basemap = Basemap(resolution=resolution, projection=projection,
                      llcrnrlat=llcrnrlat, llcrnrlon=llcrnrlon,
                      urcrnrlat=urcrnrlat, urcrnrlon=urcrnrlon)
    (x, y) = numpy.meshgrid(lon, lat)

    return (basemap, x, y)

#
