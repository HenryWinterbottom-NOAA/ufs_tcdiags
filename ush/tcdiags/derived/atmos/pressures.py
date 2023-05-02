# =========================================================================

# Module: ush/tcdiags/derived/atmos/pressures.py

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

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import numpy
from metpy.calc import altimeter_to_sea_level_pressure as a2slp
from metpy.units import units
from tools import parser_interface
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["pressure_from_thickness", "pressure_to_sealevel"]

# ----

logger = Logger()

# ----


def pressure_from_thickness(varobj: object) -> numpy.array:
    """
    Description
    -----------

    This function computes the pressure profile using the isobaric
    thickness for the corresponding variable level interfaces; the
    profile is computed by integrating isobaric interface thickness
    from the top of the atmosphere, downward, to the surface.

    Parameters
    ----------

    varobj: object

        A Python object containing, at minimum, the isobaric level
        interface thicknesses and the surface pressure from which
        pressure profile will be computed.

    Returns
    -------

    pres: numpy.array

        A Python array-type variable containing the pressure profile;
        units are Pascals.

    """

    # Initialize the pressure profile.
    dpres = numpy.array(varobj.pressure.values)
    pres = dpres
    pres[0, :, :] = numpy.array(varobj.surface_pressure.values)

    # Compute the pressure profile using the surface pressure and
    # layer thickness; proceed accordingly.
    msg = f"Computing pressure profile array of dimension {pres.shape}."
    logger.info(msg=msg)

    for zlev in range(pres.shape[0] - 2, 0, -1):

        # Compute the pressure profile.
        pres[zlev, :, :] = pres[zlev + 1, :, :] + dpres[zlev, :, :]

    return pres


# ----


def pressure_to_sealevel(varobj: object) -> object:
    """
    Description
    -----------

    This function reduces the surface pressure array to sea-level
    following Wallace and Hobbs [1977].

    Parameters
    ----------

    varobj: object

        A Python object containing, at minimum, the surface prssure,
        the surface elevation, and the temperature profile from which
        the sea-level pressure will be computed.

    Returns
    -------

    varobj: object

        A Python object updated to contain the surface pressure
        reduced to sea-level.

    """

    # Reduce the surface pressure value to the sea-surface.
    pslp = a2slp(
        altimeter_value=varobj.psfc[:, :],
        height=varobj.zsfc[:, :],
        temperature=varobj.temp[0, :, :],
    )

    varobj = parser_interface.object_setattr(
        object_in=varobj, key="pslp", value=units.Quantity(pslp, "Pa")
    )

    return varobj
