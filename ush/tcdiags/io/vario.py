# =========================================================================

# Module: ush/tcdiags/io/vario.py

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

    vario.py

Description
-----------

    This module contains functions to configure, read, and update
    variable arrays.

Functions
---------

    define_units(varin, varunits)

        This function defines the units for the respective variable
        array.

    read_ncvar(varname, varobj)

        This function reads a netCDF-formatted variable from a
        netCDF-formatted file path; the netCDF-variable object
        `varobj` attribute `values` contains the respective variable
        array.

    update_grid(xlat_in, xlon_in)

        This function checks that the input latitude and longitude
        (`xlat_in` and `xlon_in`, respectively) arrays are of
        2-dimensions; if not, a 2-dimensionl grid is defined and
        returned; if so, nothing is done.

    update_varattrs(varin, flip_lat=False, flip_z=False, scale_mult=1.0,
                    scale_add=0.0)

        This function updates the attributes for the respective
        variable array; this includes manipulations along specified
        axes and values scaling.

Requirements
------------

- metpy; https://unidata.github.io/MetPy/latest/index.html

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 01 May 2023

History
-------

    2023-05-01: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from types import SimpleNamespace
from typing import Tuple, Union

import numpy
from ioapps import netcdf4_interface
from metpy.units import units
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = [
    "define_units",
    "read_ncvar",
    "update_grid",
    "update_varattrs",
]

# ----

logger = Logger(caller_name=__name__)

# ----


def define_units(varin: numpy.ndarray, varunits: Union[str, None]) -> units.Quantity:
    """
    Description
    -----------

    This function defines the units for the respective variable array.

    Parameters
    ----------

    varin: numpy.ndarray

        A Python numpy.ndarray variable containing the array for the
        respective variable.

    varunits: str

        A Python string specifying the units to be assigned to the
        respective variable.

    Returns
    -------

    varout: units.Quantity

        A Python units.Quantity variable now containing the specified
        units quantity for the respective variable.

    """

    # Assign a unit quantity to the respective variable array; proceed
    # accordingly.
    varout = varin
    if units is not None:
        varout = units.Quantity(varout, varunits)

    return varout


# ----


def read_ncvar(varname: str, varobj: SimpleNamespace) -> numpy.ndarray:
    """
    Description
    -----------

    This function reads a netCDF-formatted variable from a
    netCDF-formatted file path; the netCDF-variable object `varobj`
    attribute `values` contains the respective variable array.

    Parameters
    ----------

    varname: str

        A Python string specifying the variable name.

    varobj: SimpleNamespace

        A Python SimpleNamespace object containing the initialized
        netCDF-formatted variable container.

    Returns
    -------

    varobj: SimpleNamespace

        A Python SimpleNamespace object updated and now containing the
        netCDF-formatted variable array.

    """

    # Collect the respective variable and update as necessary.
    msg = f"Reading variable {varname} from netCDF-formatted file path {varobj.ncfile}."
    logger.info(msg=msg)
    varobj.values = netcdf4_interface.ncreadvar(
        ncfile=varobj.ncfile,
        ncvarname=varobj.ncvarname,
        squeeze=varobj.squeeze,
        axis=varobj.squeeze_axis,
    )

    return varobj


# ----


def update_grid(
    xlat_in: units.Quantity, xlon_in: units.Quantity
) -> Tuple[units.Quantity, units.Quantity]:
    """
    Description
    -----------

    This function checks that the input latitude and longitude
    (`xlat_in` and `xlon_in`, respectively) arrays are of
    2-dimensions; if not, a 2-dimensionl grid is defined and returned;
    if so, nothing is done.

    Parameters
    ----------

    xlat_in: units.Quantity

        A Python units.Quantity variable containing the latitude
        geographical coordinate.

    xlon_in: units.Quantity

        A Python units.Quantity variable containing the longitude
        geographical coordinate.

    Returns
    -------

    xlat_out: units.Quantity

        A Python units.Quantity variable containing a 2-dimensional
        projection of the latitude geographical coordinate.

    xlon_out: units.Quantity

        A Python units.Quantity variable containing a 2-dimensional
        projection of the longitude geographical coordinate.

    """

    # Check whether the geographical coordinate arrays are
    # 2-dimensional grid projections; proceed accordingly.
    if (xlat_in.ndim != 2) and (xlon_in.ndim != 2):
        msg = (
            "The geographical coordinate arrays for latitude and longitude "
            "are 1-dimensional; converting to gridded values."
        )
        logger.warn(msg=msg)

        (xlon_out, xlat_out) = numpy.meshgrid(xlon_in, xlat_in)
    else:
        msg = (
            "The geographical coordinate arrays are projected to "
            "2-dimensions; doing nothing."
        )
        logger.info(msg=msg)
        xlat_out = xlat_in
        xlon_out = xlon_in

    return (xlat_out, xlon_out)


# ----


def update_varattrs(
    varin: units.Quantity,
    flip_lat: bool = False,
    flip_z: bool = False,
    scale_mult: float = 1.0,
    scale_add: float = 0.0,
) -> units.Quantity:
    """
    Description
    -----------

    This function updates the attributes for the respective variable
    array; this includes manipulations along specified axes and values
    scaling.

    Parameters
    ----------

    varin: units.Quantity

         A Python units.Quantity variable containing an array for
         which the respective attributes will be evaluated.

    Keywords
    --------

    flip_lat: bool, optional

        A Python boolean valued variable specifying whether the input
        variable array `varin` is to be flipped along the latitudinal
        (e.g., `y`) axis.

    flip_z: bool, optional

        A Python boolean valued variable specifying whether the input
        variable array `varin` is to be flipped along the vertical
        (e.g., `z`) axis.

    scale_mult: float, optional

        A Python float value defining the multiplicative scaling
        value.

    scale_add: float, optional

        A Python float value defining the additive scaling value.

    Returns
    -------

    varout: units.Quantity

         A Python units.Quantity variable containing the array about
         which the attributes have been assessed/changed.

    """

    # Check whether the respective variable is to be flipped along the
    # z-axis; proceed accordingly.
    varout = varin
    if flip_z:
        if varin.ndim == 3:
            msg = "Flipping array along the vertical axis."
            logger.warn(msg=msg)
            varout = numpy.flip(varout[:, :, :], axis=0)

            # Check whether the respective variable is to be flipped along the
            # y-axis; proceed accordingly.
            if flip_lat:
                msg = "Flipping array along the latitudinal axis."
                logger.warn(msg=msg)
                varout = numpy.flip(varout[:, :, :], axis=1)
    else:
        # Check whether the respective variable is to be flipped along the
        # y-axis; proceed accordingly.
        if flip_lat:
            try:
                msg = "Flipping array along the latitudinal axis."
                logger.warn(msg=msg)
                varout = numpy.flip(varout[:, :], axis=0)
            except IndexError:
                pass

    # Scale the variable accordingly.
    varout = scale_mult * (varout) + scale_add

    return varout
