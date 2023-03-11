# =========================================================================

# Module: ush/tcdiags/atmos/pressures.py

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

    pressures.py

Description
-----------

    This module contains various pressure profile computational
    methods.

Functions
---------

    pressure_from_thickness(inputs_obj)

        This function computes the pressure profile using the isobaric
        thickness for the corresponding variable level interfaces; the
        profile is computed by integrating isobaric interface
        thickness from the top of the atmosphere, downward, to the
        surface.

    pressure_to_sealevel(inputs_obj)

        This function reduces the surface pressure array to sea-level
        following Wallace and Hobbs [1977].

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

import numpy
from metpy.calc import altimeter_to_sea_level_pressure as a2slp
from metpy.units import units
from tools import parser_interface
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["pressure_from_thickness"]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


def pressure_from_thickness(inputs_obj: object) -> object:
    """
    Description
    -----------

    This function computes the pressure profile using the isobaric
    thickness for the corresponding variable level interfaces; the
    profile is computed by integrating isobaric interface thickness
    from the top of the atmosphere, downward, to the surface.

    Parameters
    ----------

    inputs_obj: object

        A Python object containing, at minimum, the isobaric level
        interface thicknesses and the surface pressure from which
        pressure profile will be computed.

    Returns
    -------

    inputs_obj: object

        A Python object updated to contain the pressure profile.

    """

    # Initialize the pressure profile.
    dpres = numpy.array(inputs_obj.pres)
    pres = numpy.array(inputs_obj.pres)
    pres[0, :, :] = numpy.array(inputs_obj.psfc)[:, :]

    # Compute the pressure profile using the surface pressure and
    # layer thickness; proceed accordingly.
    msg = f"Computing pressure profile array of dimension {pres.shape}."
    logger.info(msg=msg)

    for zlev in range(pres.shape[0] - 2, 0, -1):

        # Compute the pressure profile.
        pres[zlev, :, :] = pres[zlev + 1, :, :] + dpres[zlev, :, :]

    # Correct units and update the input variable object.
    pres = units.Quantity(pres, "Pa")

    inputs_obj = parser_interface.object_setattr(
        object_in=inputs_obj, key="pres", value=pres
    )

    return inputs_obj

# ----


def pressure_to_sealevel(inputs_obj: object) -> object:
    """
    Description
    -----------

    This function reduces the surface pressure array to sea-level
    following Wallace and Hobbs [1977].

    Parameters
    ----------

    inputs_obj: object

        A Python object containing, at minimum, the surface prssure,
        the surface elevation, and the temperature profile from which
        the sea-level pressure will be computed.

    Returns
    -------

    inputs_obj: object

        A Python object updated to contain the surface pressure
        reduced to sea-level.

    """

    # Reduce the surface pressure value to the sea-surface.
    pslp = a2slp(altimeter_value=inputs_obj.psfc[:, :],
                 height=inputs_obj.zsfc[:, :],
                 temperature=inputs_obj.temp[0, :, :])

    # Correct units and update the input variable object.
    pslp = units.Quantity(pslp, "Pa")

    inputs_obj = parser_interface.object_setattr(
        object_in=inputs_obj, key="pslp", value=pslp
    )

    return inputs_obj
