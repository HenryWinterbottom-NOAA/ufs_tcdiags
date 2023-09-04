# =========================================================================

# Module: ush/tcdiags/analysis/svd.py

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

    svd.py

Description
-----------

    This module contains functions related to singular value
    decompositions of provided variable arrays.

Functions
---------

    desconstruct(varin, compute_uv=True, full_matrices=True,
                 overwrite_at=True, check_finite=True, lapack_driver="gesdd")

        This function factorizes (e.g., deconstructs) the
        2-dimensional input variable `varin` using Singular Value
        Decomposition (SVD) into unitary matrices (Umat and Vmat) and
        a 1-dimensional array of singular values.

    reconstruct(Umat, Sarr, Vmat)

        This function reconstructs a variable field provided the
        unitary matrices `Umat` and `Vmat` and the singular values
        `Sarr` computed from the singular value decomposition of the
        respective variable field.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 09 June 2023

History
-------

    2023-06-09: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=invalid-name
# pylint: disable=too-many-arguments

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from typing import Tuple

import numpy
from scipy.linalg import svd
from utils.logger_interface import Logger

from tcdiags.exceptions import SVDError

# ----

logger = Logger(caller_name=__name__)

# ----


def deconstruct(
    varin: numpy.array,
    compute_uv: bool = True,
    full_matrices: bool = True,
    overwrite_a: bool = False,
    check_finite: bool = True,
    lapack_driver: str = "gesdd",
) -> Tuple[numpy.array, numpy.array, numpy.array]:
    """
    Description
    -----------

    This function factorizes (e.g., deconstructs) the 2-dimensional
    input variable `varin` using Singular Value Decomposition (SVD)
    into unitary matrices (Umat and Vmat) and a 1-dimensional array of
    singular values.

    Parameters
    ----------

    varin: numpy.array

        A Python numpy.array variable containing the input variable
        for the SVD (i.e., `A`).

    Keywords
    --------

    compute_uv: bool, optional

        A Python boolean valued variable specifying whether to compute
        the unitary matrices `Umat` and `Vmat` in addition to the
        singular value array `Sarr`.

    full_matrices: bool, optional

        A Python boolean valued variable specifying whether to compute
        the SVD using full (`True`) or reduced dimension (`False`)
        matrices.

    overwrite_a: bool, optional

        A Python boolean valued variable specifying whether to
        overwrite the input matrix `A` when computing the SVD.

    check_finite: bool, optional

        A Python boolean valued variable specifying whether to check
        if the input matrix `A` contains only finite values.

    lapack_driver: str, optional

        A Python string variable specyfing the LAPACK SVD driver.

    Returns
    -------

    Umat: numpy.array

        A Python numpy.array variable containing the unitary matrix
        `U` computed from the SVD of the input variable `varin`.

    Sarr: numpy.array

        A Python numpy.array variable containing the singular values
        array compute from the SVD of the input variable `varin`.

    Vmat: numpy.array

        A Python numpy.array variable containing the unitary matrix
        `V` computed from the SVD of the input variable `varin`.

    Raises
    ------

    SVDError:

        - raised if the input variable is not 2-dimensions.

        - raised if an exception is encountered while computing the
          SVD.

    """

    # Compute the singular value decomposition of the input variable.
    if varin.ndim != 2:
        msg = ("The input variable must be 2-dimensions; received a variable "
               f"of shape {numpy.shape(varin)} upon entry. Aborting!!!"
               )
        raise SVDError(msg=msg)
    try:
        (Umat, Sarr, Vmat) = svd(
            numpy.array(varin),
            full_matrices=full_matrices,
            compute_uv=compute_uv,
            overwrite_a=overwrite_a,
            check_finite=check_finite,
            lapack_driver=lapack_driver,
        )
    except Exception as errmsg:
        msg = f"The SVD computation failed with error {errmsg}. Aborting!!!"
        raise SVDError(msg=msg)

    return (Umat, Sarr, Vmat)

# ----


def rebuild(varin: numpy.array, ncoeffs: int, compute_uv: bool = True,
            full_matrices: bool = True, overwrite_a: bool = False,
            check_finite: bool = True, lapack_driver: str = "gesdd",) -> numpy.array:
    """
    Description
    -----------

    This function deconstructs a 2-dimensional input variable `varin`
    using SVD and subsequently reconstructs the variable field using
    the specified singular values.

    Parameters
    ----------

    varin: numpy.array

        A Python numpy.array variable containing the input variable
        for the SVD (i.e., `A`).

    ncoeffs: int

        A Python integer specifying the number of singular values,
        relative to 0, to be set to 0.0 prior to rebuilding the
        variable field.

    Keywords
    --------

    compute_uv: bool, optional

        A Python boolean valued variable specifying whether to compute
        the unitary matrices `Umat` and `Vmat` in addition to the
        singular value array `Sarr`.

    full_matrices: bool, optional

        A Python boolean valued variable specifying whether to compute
        the SVD using full (`True`) or reduced dimension (`False`)
        matrices.

    overwrite_a: bool, optional

        A Python boolean valued variable specifying whether to
        overwrite the input matrix `A` when computing the SVD.

    check_finite: bool, optional

        A Python boolean valued variable specifying whether to check
        if the input matrix `A` contains only finite values.

    lapack_driver: str, optional

        A Python string variable specyfing the LAPACK SVD driver.

    Returns
    -------

    varout: numpy.array

        A Python numpy.array variable containing the output variable
        reconstructed from the input variable array.

    """

    # Deconstruct the input variable `varin` and subsequently
    # reconstruct the variable using the specified singular values.
    (Umat, Sarr, Vmat) = deconstruct(varin=varin, compute_uv=compute_uv,
                                     full_matrices=full_matrices,
                                     overwrite_a=overwrite_a,
                                     check_finite=check_finite,
                                     lapack_driver=lapack_driver)
    Sarr[0:ncoeffs] = 0.0
    varout = reconstruct(Umat=Umat, Sarr=Sarr, Vmat=Vmat)

    return varout


# ----


def reconstruct(Umat: numpy.array, Sarr: numpy.array, Vmat: numpy.array) -> numpy.array:
    """
    Description
    -----------

    This function reconstructs a variable field provided the unitary
    matrices `Umat` and `Vmat` and the singular values `Sarr` computed
    from the singular value decomposition of the respective variable
    field.

    Parameters
    ----------

    Umat: numpy.array

        A Python numpy.array variable containing the unitary matrix
        `U` computed from from the SVD.

    Sarr: numpy.array

        A Python numpy.array variable containing the singular values
        array compute from the SVD.

    Vmat: numpy.array

        A Python numpy.array variable containing the unitary matrix
        `V` computed from the SVD.

    Returns
    -------

    varout: numpy.array

        A Python numpy.array variable containing the reconstructed
        variable field.

    Raises
    ------

    SVDError:

        - raised if an exception is encountered while reconstructing
          the variable field.

    """

    # Reconstruct the variable field.
    try:
        sigma = numpy.zeros((numpy.shape(Umat)[0], numpy.shape(Vmat)[0]))
        for idx in range(numpy.shape(Sarr)[0]):
            sigma[idx, idx] = Sarr[idx]
        varout = numpy.dot(Umat, numpy.dot(sigma, Vmat))
    except Exception as errmsg:
        msg = f"The vector reconstruction failed with error {errmsg}. Aborting!!!"
        raise SVDError(msg=msg)

    return varout
