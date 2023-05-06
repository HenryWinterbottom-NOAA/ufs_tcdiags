# =========================================================================

# Module: ush/tcdiags/interp/vertical.py

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

    vertical.py

Description
-----------

    This module contains functions for vertical interpolation
    applications.

Functions
---------

    vertical(varin, zarr, levs)

        This method interpolates a 3-dimensional variable to specified
        vertical levels.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

- wrf-python; https://github.com/NCAR/wrf-python

Author(s)
---------

    Henry R. Winterbottom; 07 March 2023

History
-------

    2023-03-07: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from typing import List

import numpy
from tcdiags.exceptions import InterpVerticalError
from utils.logger_interface import Logger
from wrf import interplevel

# ----

# Define all available functions.
__all__ = ["interp"]

# ----

logger = Logger(caller_name=__name__)

# ----


def interp(varin: numpy.array, zarr: numpy.array, levs: List) -> numpy.array:
    """
    Description
    -----------

    This method interpolates a 3-dimensional variable to specified
    vertical levels.

    Parameters
    ----------

    varin: numpy.array

        A Python array for the 3-dimensional variable to be
        interpolated.

    zarr: numpy.array

        A Python array for the vertical level type; this array must be
        of the same dimension as varin.

    levs: List

        A Python list of levels to which to interpolate; the units of
        this list must be identical to the units of the zarr array.

    Returns
    -------

    varout: numpy.array

        A Python array containing the 3-dimensional variable
        interpolated to the specified vertical levels.

    Raises
    ------

    InterpError:

        - raised if an exception is encountered during the vertical
          interpolation.

    """

    # Interpolate the 3-dimensional variable specified upon input to
    # the specified vertical-type levels.
    try:
        varout = interplevel(varin.T, zarr.T, levs)

    except Exception as errmsg:
        msg = f"The vertical interpolation failed with error {errmsg}. Aborting!!!"
        raise InterpVerticalError(msg=msg) from errmsg

    return varout
