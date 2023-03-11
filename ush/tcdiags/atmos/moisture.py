# =========================================================================

# Module: ush/tcdiags/atmos/moisture.py

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


"""

# ----


# ----

from exceptions import AtmosMoistureError
from metpy.calc import mixing_ratio_from_specific_humidity as mxrt_from_spfh
from metpy.units import units
from pint import Quantity
from tools import parser_interface
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["sphmd_to_mxrt"]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


def spfh_to_mxrt(inputs_obj: object) -> object:
    """

    """

    # Compute the mixing ratio profile from the specific humidity
    # profile.
    mxrt = mxrt_from_spfh(specific_humidity=inputs_obj.spfh)

    # Correct units and update the input variable object.
    mxrt = units.Quantity(mxrt, "kilogram / kilogram")

    inputs_obj = parser_interface.object_setattr(
        object_in=inputs_obj, key="mxrt", value=mxrt
    )

    return inputs_obj
