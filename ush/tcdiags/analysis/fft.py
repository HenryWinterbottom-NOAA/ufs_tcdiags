# =========================================================================

# Module: ush/tcdiags/analysis/fft.py

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

    fft.py

Description
-----------
   
    This module contains functional wrappers for the available numpy
    fast-Fourier transform applications.

Functions
---------

    forward_fft2d(varin)

        This function computes the forward fast Fourier transform
        (FFT) of a 2-dimensional real-value input array `varin`.

    inverse_fft2d(varin)

        This function computes the forward fast Fourier transform
        (FFT) of a 2-dimensional complex-value input array `varin`.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 16 March 2023

History
-------

    2023-03-16: Henry Winterbottom -- Initial implementation.

"""

# ----

import numpy
from exceptions import FFTError
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["forward_fft2d", "inverse_fft2d"]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


def forward_fft2d(varin: numpy.array) -> numpy.complex_:
    """
    Description
    -----------

    This function computes the forward fast Fourier transform (FFT) of
    a 2-dimensional real-value input array `varin`.

    Parameters
    ----------

    varin: array-type

        A Python array-type variable containing the 2-dimensional
        real-values input array.

    Returns
    -------

    varout: array-type

        A Python array-type variable containing the 2-dimensional
        complex-values computed from the forward FFT.

    Raises
    ------

    FFTError:

        * raised if the input array is not of 2-dimensions.

    """

    # Compute the forward fast Fourier transform in the input variable
    # array.
    if len(varin.shape) != 2:
        msg = (
            "The input array is not 2-dimensions; received an array of "
            f"{len(varin.shape)} dimensions. Aborting!!!"
        )
        raise FFTError(msg=msg)

    msg = (
        "Computing the forward Fourier transform of input array dimension "
        f"({varin.shape[0]}, {varin.shape[1]})."
    )
    logger.info(msg=msg)

    varout = numpy.fft.fft2(varin)

    return varout


# ----


def inverse_fft2d(varin: numpy.complex_) -> numpy.complex_:
    """
    Description
    -----------

    This function computes the inverse fast Fourier transform (FFT) of
    a 2-dimensional complex-value input array `varin`.

    Parameters
    ----------

    varin: array-type

        A Python array-type variable containing the 2-dimensional
        complex-values computed from the FFT.

    Returns
    -------

    varout: array-type

        A Python array-type variable containing the 2-dimensional
        complex-values computed from the inverse FFT.

    Raises
    ------

    FFTError:

        * raised if the input array is not of 2-dimensions.

    """

    # Compute the inverse fast Fourier transform in the input variable
    # array.
    if len(varin.shape) != 2:
        msg = (
            "The input array is not 2-dimensions; received an array of "
            f"{len(varin.shape)} dimensions. Aborting!!!"
        )
        raise FFTError(msg=msg)

    msg = (
        "Computing the inverse Fourier transform of input array dimension "
        f"({varin.shape[0]}, {varin.shape[1]})."
    )
    logger.info(msg=msg)

    varout = numpy.fft.ifft2(varin)

    return varout
