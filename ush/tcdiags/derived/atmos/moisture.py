# =========================================================================

# Module: ush/tcdiags/derived/atmos/moisture.py

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

    moisture.py

Description
-----------

    This module contains various moisture variable computation
    methods.

Functions
---------

    spfh_to_mxrt(inputs_obj)

        This function computes the mixing ratio from the specific
        humidity.

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
from metpy.calc import mixing_ratio_from_specific_humidity as mxrt_from_spfh
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["spfh_to_mxrt"]

# ----

logger = Logger(caller_name=__name__)

# ----


def spfh_to_mxrt(varobj: object) -> numpy.array:
    """
    Description
    -----------

    This function computes the mixing ratio from the specific
    humidity.

    Parameters
    ----------

    inputs_obj: object

        A Python object containing, at minimum, the specific humidity
        profile (`specific_humidity`) from which the mixing ratio will
        be computed.

    Returns
    -------

    mxrt: numpy.array

        A Python array-type variable containing the mixing-ratio
        profile.

    """

    # Compute the mixing ratio profile from the specific humidity
    # profile.
    msg = (
        "Computing the mixing ratio array of dimension "
        f"{varobj.specific_humidity.shape}."
    )
    logger.info(msg=msg)

    mxrt = mxrt_from_spfh(specific_humidity=varobj.specific_humidity)

    return mxrt
