# =========================================================================
# File: scripts/compute_tcdiags.py
# Author: Henry R. Winterbottom
# Date: 03 March 2023
# Version: 0.0.1
# License: LGPL v2.1
# =========================================================================

"""
Module
------

    build_basemap.py

Description
-----------

    This module contains functions related to building application
    basemaps.

Functions
---------

    build_basemap(lat, lon, resolution = "c", projection = "cylc",
                  llcrnrlat = -90.0, llcrnrlon = 0.0, urcrnrlat = 90.0,
                  urcrnrlon = 360.0)

        This function builds a basemap object.

Requirements
------------

- mpl_toolkits.basemap; https://github.com/matplotlib/basemap

Author(s)
---------

    Henry R. Winterbottom; 26 August 2023

History
-------

    2023-08-26: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=invalid-name
# pylint: disable=too-many-arguments

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from typing import Tuple

import numpy
from mpl_toolkits.basemap import Basemap

# ----


def build_basemap(
    lat: numpy.array,
    lon: numpy.array,
    resolution: str = "c",
    projection: str = "cyl",
    llcrnrlat: float = -90.0,
    llcrnrlon: float = 0.0,
    urcrnrlat: float = 90.0,
    urcrnrlon: float = 360.0,
) -> Tuple[Basemap, numpy.array, numpy.array]:
    """
    Description
    -----------

    This function builds a basemap object.

    Parameters
    ----------

    lat: numpy.array

        A Python numpy.array containing a flattened (i.e.,
        1-dimensional) array of latitude coordinate values; units are
        degrees.

    lon: numpy.array

        A Python numpy.array containing a flattened (i.e.,
        1-dimensional) array of longitude coordinate values; units are
        degrees.

    Keywords
    --------

    resolution: str, optional

        The basemap resolution.

    projection: str, optional

        The basemap projection; see
        https://tinyurl.com/basemap-projection.

    llcrnrlat: float, optional

        The latitude coordinate for the lower-left corner of the
        basemap; units are degrees.

    llcrnrlon: float, optional

        The longitude coordinate for the lower-left corner of the
        basemap; units are degrees.

    urcrnrlat: float, optional

        The latitude coordinate for the upper-right corner of the
        basemap; units are degrees.

    urcrnrlon: float, optional

        The longitude coordinate for the upper-right corner of the
        basemap; units are degrees.

    Returns
    -------

    basemap: Basemap

        A Python Basemap object containing the basemap definition.

    x: numpy.array

        A Python numpy.array containing the x-coordinate values
        corresponding to the basemap meridionals.

    y: numpy.array

        A Python numpy.array containing the y-coordinate values
        corresponding to the basemap horizontals.

    """

    # Define the basemap attributes and return.
    basemap = Basemap(
        resolution=resolution,
        projection=projection,
        llcrnrlat=llcrnrlat,
        llcrnrlon=llcrnrlon,
        urcrnrlat=urcrnrlat,
        urcrnrlon=urcrnrlon,
    )
    (x, y) = numpy.meshgrid(lon, lat)

    return (basemap, x, y)
