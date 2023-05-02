# =========================================================================

# Module: ush/tcdiags/derived/atmos/heights.py

# Author: Henry R. Winterbottom

# Email: henry.winterbottom@noaa.gov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the respective public license published by the
# Free Software Foundation and included with the repository within
# which this application is contained.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# =========================================================================

"""
Module
------

    heights.py

Description
-----------

    This module contains various height profile computational methods.

Functions
---------

    height_from_pressure(pressure)

        This function computes the geometric height profile from the
        pressure profile array.

Requirements
------------

- metpy; https://unidata.github.io/MetPy/latest/index.html

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 09 March 2023

History
-------

    2023-03-09: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import numpy
from metpy.calc import pressure_to_height_std
from metpy.units import units
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["height_from_pressure"]

# ----

logger = Logger()

# ----


def height_from_pressure(varobj: object) -> numpy.array:
    """
    Description
    -----------

    This function computes the geometric height profile from the
    pressure profile array.

    Parameters
    ----------

    varobj: object

        A Python object containing, at minimum, the pressure levels
        from which the height profile will be computed.

    Returns
    -------

    height: numpy.array

        A Python array-type variable containing the geometric height
        profile.

    """

    # Compute the geometric height profile using the pressure profile.
    msg = (
        "Computing the geometric height profile array of dimension "
        f"{varobj.pressure.values.shape}."
    )
    logger.info(msg=msg)

    pressure = units.Quantity(varobj.pressure.values, "Pa")
    height = pressure_to_height_std(pressure=pressure)

    return height
