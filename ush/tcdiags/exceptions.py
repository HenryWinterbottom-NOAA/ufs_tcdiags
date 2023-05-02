# =========================================================================

# Module: ush/tcdiags/exceptions.py

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

    exceptions.py

Description
-----------

    This module loads the exceptions package.

Classes
-------

    AtmosMoistureError(msg)

        This is the base-class for exceptions encountered within the
        ush/tcdiags/atmos/moisture module; it is a sub-class of Error.

    AtmosWindsError(msg)

        This is the base-class for exceptions encountered within the
        ush/tcdiags/atmos/winds module; it is a sub-class of Error.

    DerivedError(msg)

        This is the base-class for exceptions encountered within the
        ush/tcdiags/io/derived module; it is a sub-class of Error.

    FFTError(msg)

        This is the base-class for exceptions encountered within the
        ush/tcdiags/analysis/fft module; it is a sub-class of Error.

    FilterVortexError(msg)

        This is the base-class for exceptions encountered within the
        ush/tcdiags/tc module FilterVortex class; it is a sub-class of
        Error.

    GeoMetsError(msg)

        This is the base-class for exceptions encountered within the
        ush/tcdiags/geomets module; it is a sub-class of Error.

    GFSError(msg)

        This is the base-class for exceptions encountered within the
        ush/tcdiags/io/gfs module; it is a sub-class of Error.

    InputFieldsError(msg)

        This is the base-class for exceptions encounterd within the
        ush/tcdiags/io/inputs module.

    InterpError(msg)

        This is the base-class for exceptions encountered within the
        ush/tcdiags/interp module; it is a sub-class of Error.

    TCDiagsError(msg)

        This is the base-class for exceptions encountered within the
        ush/tcdiags module; it is a sub-class of Error.

    TCDiagsIOError(msg)

        This is the base-class for exceptions encountered within the
        ush/tcdiags/io module; it is a sub-class of Error.

    TropCycMPIError(msg)

        This is the base-class for exceptions encountered within the
        ush/tcdiags/metrics/tropcycmpi module; it is a sub-class of
        Error.

    TropCycSteeringFlowsError(msg)

        This is the base-class for exceptions encountered within the
        ush/tcdiags/metrics/steeringflows module; it is a sub-class of
        Error.

    TropCycWNMSIError(msg)

        This is the base-class for exceptions encountered within the
        ush/tcdiags/metrics/tropcycwnmsi module; it is a sub-class of
        Error.

    VarIOError(msg)

        This is the base-class for exceptions encountered within the
        ush/tcdiags/io/vario module; it is a sub-class of
        Error.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 10 March 2023

History
-------

    2023-03-10: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from utils.error_interface import Error

# ----

# Define all available attributes.
__all__ = [
    "AtmosMoistureError",
    "AtmosWindsError",
    "DerivedError",
    "FFTError",
    "FilterVortexError",
    "GeoMetsError",
    "GFSError",
    "InputFieldsError",
    "InterpError",
    "TCDiagsError",
    "TCDiagsIOError",
    "TropCycMPIError",
    "TropCycSteeringFlowsError",
    "TropCycWNMSIError",
    "VarIOError",
]

# ----


class AtmosMoistureError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/tcdiags/atmos/moisture module; it is a sub-class of Error.

    """


# ----


class AtmosWindsError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/tcdiags/atmos/winds module; it is a sub-class of Error.

    """


# ----


class DerivedError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/tcdiags/io/derived module; it is a sub-class of Error.

    """


# ----


class FFTError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/tcdiags/analysis/fft module; it is a sub-class of Error.

    """


# ----


class FilterVortexError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/tcdiags/tc module FilterVortex class; it is a sub-class of
    Error.

    """


# ----


class GeoMetsError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/tcdiags/geomets module; it is a sub-class of Error.

    """


# ----


class GFSError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/tcdiags/io/gfs module; it is a sub-class of Error.

    """


# ----


class InputFieldsError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/tcdiags/io/inputs module; it is a sub-class of Error.

    """


# ----


class InterpError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/tcdiags/interp module; it is a sub-class of Error.

    """


# ----


class TCDiagsError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/tcdiags module; it is a sub-class of Error.

    """


# ----


class TCDiagsIOError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/tcdiags/io module; it is a sub-class of Error.

    """


# ----


class TropCycMPIError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/tcdiags/metrics/tropcycmpi module; it is a sub-class of Error.

    """


# ----


class TropCycSteeringFlowsError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/tcdiags/metrics/steeringflows module; it is a sub-class of
    Error.

    """


# ----


class TropCycWNMSIError(Error):

    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/tcdiags/metrics/tropcycwnmsi module; it is a sub-class of
    Error.

    """


# ----


class VarIOError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/tcdiags/io/vario module; it is a sub-class of Error.


    """
