# =========================================================================

# Module: ush/tcdiags/interp/radial.py

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

from scipy.interpolate import griddata
import numpy

from utils.logger_interface import Logger

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

logger = Logger()

# ----


def interp(interp_obj: object, method: str = "linear") -> object:
    """ """

    # Initialize the grid attributes.
    x = numpy.arange(0, numpy.shape(interp_obj.vararray)[1], 1.0)
    y = numpy.arange(0, numpy.shape(interp_obj.vararray)[0], 1.0)

    (xx, yy) = numpy.meshgrid(x, y)
    outer_dist = interp_obj.distance
    inner_dist = outer_dist - interp_obj.ddist
    interp_var = interp_obj.vararray

    # Interpolate radially inward to recover the initial
    # missing-datum.
    while (inner_dist >= 0.0):

        msg = f"Interpolating within range {inner_dist} and {outer_dist}."
        logger.info(msg=msg)

        varin = numpy.where((interp_obj.raddist <= inner_dist), numpy.nan,
                            interp_var)

        mask = numpy.ma.masked_invalid(varin)

        xf = xx[~mask.mask]
        yf = yy[~mask.mask]
        invar = interp_var[~mask.mask]

        interp_var = griddata(
            (xf, yf), invar, (xx, yy), method=method)

        outer_dist = inner_dist
        inner_dist = outer_dist - interp_obj.ddist

    return interp_var
