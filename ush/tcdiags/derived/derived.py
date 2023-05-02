# =========================================================================

# Module: ush/tcdiags/derived/derived.py

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

    derived.py

Description
-----------

    This module contains interfaces to derive various quantities using
    the respective methodologies.

Functions
---------

    _get_module(module, method)

        This method returns the function corresponding to the
        specified method (`method`) within the respective specified
        class (`module`).

    compute_height(varobj, method)

        This function computes a height diagnostic type using the
        specified method.

    compute_pressure(varobj, method)

        This function computes a pressure type using the specified
        method.

Author(s)
---------

    Henry R. Winterbottom; 02 May 2023

History
-------

    2023-05-02: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from importlib import import_module
from typing import Callable

import numpy
from tcdiags.exceptions import DerivedError
from tools import parser_interface
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["compute_height", "compute_pressure"]

# ----

logger = Logger()

# ----


def _get_module(module: str, method: str) -> Callable:
    """
    Description
    -----------

    This method returns the function corresponding to the specified
    method (`method`) within the respective specified class
    (`module`).

    Parameters
    ----------

    module: str

        A Python string specifying the name of the module or package
        from which to collect the respective method.

    method: str

        The method or function within the module or package (`module`)
        to be returned.

    Returns
    -------

    compute_method: Callable

        A Python function within the specified module.

    """

    try:
        compute_method = parser_interface.object_getattr(
            object_in=import_module(module), key=f"{method}", force=True
        )

    except Exception as errmsg:
        msg = (
            f"Collecting method {method} from module {module} failed with "
            f"error {errmsg}. Aborting!!!"
        )
        raise DerivedError(msg=msg) from errmsg

    return compute_method


# ----


def compute_height(varobj: object, method: str) -> numpy.array:
    """
    Description
    -----------

    This function computes a height diagnostic type using the
    specified method.

    Parameters
    ----------

    varobj: object

        A Python object containing, at minimum, the variables required
        for the respective height diagnostic computation.

    method: str

        A Python string specifying the method beneath
        `tcdiags.derived.atmos.heights`; currently supported methods
        are the following.

        - height_from_pressure

    Returns
    -------

    height: numpy.array

        A Python array-type variable containing the computed height
        values.

    """

    # Compute the respective height type from the specified method.
    compute_module = "tcdiags.derived.atmos.heights"

    compute_method = _get_module(module=compute_module, method=method)
    height = compute_method(varobj=varobj)

    return height


# ----


def compute_pressure(varobj: object, method: str) -> numpy.array:
    """
    Description
    -----------

    This function computes a pressure type using the specified method.

    Parameters
    ----------

    varobj: object

        A Python object containing, at minimum, the variables required
        for the respective pressure computation.

    method: str

        A Python string specifying the method beneath
        `tcdiags.derived.atmos.pressures`; currently supported methods
        are the following.

        - pressure_from_thickness

        - pressure_to_sealevel

    Returns
    -------

    pressure: numpy.array

        A Python array-type variable containing the computed pressure
        values.

    """

    # Compute the respective pressure type from the specified method.
    compute_module = "tcdiags.derived.atmos.pressures"

    compute_method = _get_module(module=compute_module, method=method)
    pressure = compute_method(varobj=varobj)

    return pressure
