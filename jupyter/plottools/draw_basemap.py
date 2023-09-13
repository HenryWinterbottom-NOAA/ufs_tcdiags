"""
Module
------

    draw_basemap.py

Description
-----------

    This module contains function to draw basemaps.

Functions
---------

    draw_basemap(basemap)

        This function draws the basemap attributes.

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

import numpy
from mpl_toolkits.basemap import Basemap

# ----

# Define all available module properties.
__all__ = ["draw_basemap"]

# ----


def draw_basemap(basemap: Basemap) -> None:
    """
    Description
    -----------

    This function draws the basemap attributes.

    Parameters
    ----------

    basemap: Basemap

        A Python Basemap object containing the basemap definition.

    """

    # Draw the basemap attributes.
    basemap.drawcoastlines(color="lightgray", linewidth=0.25)
    basemap.drawmeridians(
        color="black",
        meridians=numpy.arange(0.0, 360.01, 30.0),
        labels=[False, False, True, True],
        linewidth=0.1,
        dashes=[10, 10],
        fontsize=8,
    )
    basemap.drawparallels(
        color="black",
        circles=numpy.arange(-80.0, 80.01, 40.0),
        labels=[True, True, False, False],
        linewidth=0.1,
        dashes=[10, 10],
        fontsize=8,
    )
    basemap.fillcontinents(color="lightgray")
