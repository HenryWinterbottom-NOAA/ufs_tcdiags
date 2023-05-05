# =========================================================================

# Module: ush/tcdiags/atmos/winds.py

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

    winds.py

Description
-----------

    This module contains functions to compute total wind field
    diagnostics.

Functions
---------

    _cleanup(xspharm)

        This function attempts to destroy the initialized spherical
        harmonic transform object and subsequently collect any
        remaining/residual object attributes.

    _get_lev_uv(varobj, lev)

        This function returns the total wind vector component
        quantities at the specified vertical level.

    _init_spharm(array_in)

        This method initializes the spherical harmonic transform
        object.

    _reset_nan(vararr, ref_vararr)

        This function sets all array `vararr` values where the
        reference variable `ref_vararr` is `numpy.nan` to `numpy.nan`.

    _reset_nan2zero(vararr)

        This function resets all `numpy.nan` values within the array
        `vararr` to `0.0`.

    global_divg(varobj)

        This function computes the global divergence field using
        spherical harmonic transforms.

    global_vort(varobj)

        This function computes the global vorticity field using
        spherical harmonic transforms.

    global_wind_part(varobj)

        This function computes the components of the total wind field
        using spherical harmonic transforms; the methodology follows
        from Lynch [1988].

    wndmag(varobj)

        This function computes the magnitude of the vector wind field.

Requirements
------------

- metpy; https://unidata.github.io/MetPy/latest/index.html

- pyspharm; https://github.com/jswhit/pyspharm

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 09 March 2023

History
-------

    2023-03-09: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=invalid-name
# pylint: disable=too-many-locals

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import gc
from typing import Tuple

import numpy
import spharm
from tcdiags.exceptions import DerivedAtmosWindsError
from tools import parser_interface
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["global_divg", "global_psichi", "global_vort", "global_wind_part", "wndmag"]

# ----

logger = Logger(caller_name=__name__)

# ----


def _cleanup(xspharm: spharm.Spharmt) -> None:
    """
    Description
    -----------

    This function attempts to destroy the initialized spherical
    harmonic transform object and subsequently collect any
    remaining/residual object attributes.

    Parameters
    ----------

    xspharm: spharm.Spharmt

        A Python object containing the initialized spherical harmonic
        transform object.

    """

    # Destroy the initialized spherical harmonic transform object.
    del xspharm
    gc.collect()


# ----


def _get_lev_uv(varobj: object, lev: int) -> Tuple[numpy.array, numpy.array]:
    """
    Description
    -----------

    This function returns the total wind vector component quantities
    at the specified vertical level.

    Parameters
    ----------

    varobj: object

        A Python object containing, at minimum, the zonal and
        meridional total wind components.

    lev: int

        A Python integer specifying the vertical level from which to
        collect the zonal and meridional total wind components.

    Returns
    -------

    xuwnd: numpy.array

        A Python array-type variable containing the zonal wind
        component collected for the specified vertical level.

    xvwnd: numpy.array

        A Python array-type variable containing the meridional wind
        component collected for the specified vertical level.

    """

    # Define the zonal and meridional total wind components.
    (uwnd, vwnd) = [
        parser_interface.object_getattr(object_in=varobj, key=wndvar)
        for wndvar in ["uwnd", "vwnd"]
    ]

    # Define the zonal and meridional total wind components for the
    # respective/specified vertical level; proceed accordingly.
    if uwnd.ndim == 3 and vwnd.ndim == 3:
        (xuwnd, xvwnd) = [uwnd.values[lev, :, :], vwnd.values[lev, :, :]]

    elif uwnd.ndim == 2 and vwnd.ndim == 2:
        (xuwnd, xvwnd) = [uwnd.values[:, :], vwnd.values[:, :]]

    else:
        msg = (
            "The wind vector components could not be parsed and/or "
            "the level attribute is invalid. Aborting!!!"
        )
        raise DerivedAtmosWindsError(msg=msg)

    return (xuwnd, xvwnd)


# ----


def _init_spharm(array_in: numpy.array) -> spharm.Spharmt:
    """
    Description
    -----------

    This method initializes the spherical harmonic transform object.

    Parameters
    ----------

    array_in: numpy.array

        A Python array-type variable; the shape of the respective
        array will be used to initialize the spherical harmonic
        transform object.

    Returns
    -------

    xspharm: spharm.Spharmt

        A Python object containing the initialized spherical harmonic
        transform object.

    """

    # Initialize the spherical harmonic transform object accordingly.
    if array_in.ndim == 3:
        (nx, ny) = (array_in.shape[2], array_in.shape[1])

    else:
        (nx, ny) = (array_in.shape[1], array_in.shape[2])

    xspharm = spharm.Spharmt(nx, ny)

    return xspharm


# ----


def _reset_nan(vararr: numpy.array, ref_vararr: numpy.array) -> numpy.array:
    """
    Description
    -----------

    This function sets all array `vararr` values where the reference
    variable `ref_vararr` is `numpy.nan` to `numpy.nan`.

    Parameters
    ----------

    vararr: numpy.array

        A Python array-type variable.

    ref_vararr: numpy.array

        A Python array-type variable (possibly) containing `numpy.nan`
        values.

    Returns
    -------

    vararr: numpy.array

        A Python array-type variable with values replaced with
        `numpy.nan` relative to the reference variable `ref_vararr`.

    """

    # Reset any array values relative to the reference array.
    vararr = numpy.where(numpy.isnan(ref_vararr), numpy.nan, vararr)

    return vararr


# ----


def _reset_nan2zero(vararr: numpy.array) -> numpy.array:
    """
    Description
    -----------

    This function resets all `numpy.nan` values within the array
    `vararr` to `0.0`.

    Parameters
    ----------

    vararr: numpy.array

        A Python array-type variable (possibly) containing `numpy.nan`
        values.

    Returns
    -------

    vararr: numpy.array

        A Python array-type variable where any `numpy.nan` values have
        been reset to `0.0`.

    """

    # Reset any numpy.nan values to 0.0 accordingly.
    vararr = numpy.where(numpy.isnan(vararr), 0.0, vararr)

    return vararr


# ----


def global_divg(varobj: object) -> numpy.array:
    """
    Description
    -----------

    This function computes the global divergence field using spherical
    harmonic transforms.

    Parameters
    ----------

    varobj: object

        A Python object containing, at minimum, the zonal and
        meridional wind components; units are meters per second.

    Returns
    -------

    divg: numpy.array

        A Python array-type variable containing the global divergence
        values.

    """

    # Initialize the local variable and objects.
    divg = numpy.zeros(varobj.uwnd.values.shape)
    xspharm = _init_spharm(array_in=divg)
    nlevs = divg.shape[0]

    # Compute the divergence field; proceed accordingly.
    msg = f"Computing global divergence array of dimension {divg.shape}."
    logger.info(msg=msg)

    for lev in range(nlevs):

        # Define the wind vector components.
        (uwnd, vwnd) = _get_lev_uv(varobj=varobj, lev=lev)
        xuwnd = _reset_nan2zero(vararr=uwnd)
        xvwnd = _reset_nan2zero(vararr=vwnd)

        # Compute the divergence and reset the output values
        # accordingly.
        (_, dataspec) = xspharm.getvrtdivspec(ugrid=xuwnd, vgrid=xvwnd)
        divg[lev, :, :] = xspharm.spectogrd(dataspec=dataspec)
        divg[lev, :, :] = _reset_nan(vararr=divg[lev, :, :], ref_vararr=uwnd)

    # Deallocate memory for the spherical harmonic transform object.
    _cleanup(xspharm=xspharm)

    return divg


# ----


def global_psichi(varobj: object) -> Tuple[numpy.array, numpy.array]:
    """
    Description
    -----------

    This function computes the global velocity potential (`chi`) and
    streamfunction (`psi`) fields using spherical harmonic transforms.

    Parameters
    ----------

    varobj: object

        A Python object containing, at minimum, the zonal and
        meridional wind components; units are meters per second.

    Returns
    -------

    chi: numpy.array

        A Python array-type variable containing the global velocity
        potential values.

    psi: numpy.array

        A Python array-type variable containing the global
        streamfunction values.

    """

    # Initialize the local variable and objects.
    chi = numpy.zeros(varobj.uwnd.shape)
    psi = numpy.zeros(varobj.uwnd.shape)
    xspharm = _init_spharm(array_in=chi)
    nlevs = chi.shape[0]

    # Compute the streamfunction and velocity potential fields;
    # proceed accordingly.
    msg = (
        f"Computing global streamfunction and velocity arrays of dimension {chi.shape}."
    )
    logger.info(msg=msg)

    for lev in range(nlevs):

        # Define the wind vector components.
        (uwnd, vwnd) = _get_lev_uv(varobj=varobj, lev=lev)
        xuwnd = _reset_nan2zero(vararr=uwnd)
        xvwnd = _reset_nan2zero(vararr=vwnd)

        # Compute the streamfunction and velocity potential and reset
        # the output values accordingly.
        (psi[lev, :, :], chi[lev, :, :]) = xspharm.getpsichi(ugrid=xuwnd, vgrid=xvwnd)
        chi[lev, :, :] = _reset_nan(vararr=chi[lev, :, :], ref_vararr=uwnd)
        psi[lev, :, :] = _reset_nan(vararr=psi[lev, :, :], ref_vararr=uwnd)

    # Deallocate memory for the spherical harmonic transform object.
    _cleanup(xspharm=xspharm)

    return (chi, psi)


# ----


def global_vort(varobj: object) -> numpy.array:
    """
    Description
    -----------

    This function computes the global vorticity field using spherical
    harmonic transforms.

    Parameters
    ----------

    varobj: object

        A Python object containing, at minimum, the zonal and
        meridional wind components; units are meters per second.

    Returns
    -------

    vort: numpy.array

        A Python array-type variable containing the global vorticity
        values.

    """

    # Initialize the local variable and objects.
    vort = numpy.zeros(varobj.uwnd.shape)
    xspharm = _init_spharm(array_in=vort)
    nlevs = vort.shape[0]

    msg = f"Computing global vorticity array of dimension {vort.shape}."
    logger.info(msg=msg)

    # Compute the vorticity field; proceed accordingly.
    for lev in range(nlevs):

        # Define the wind vector components.
        (uwnd, vwnd) = _get_lev_uv(varobj=varobj, lev=lev)
        xuwnd = _reset_nan2zero(vararr=uwnd)
        xvwnd = _reset_nan2zero(vararr=vwnd)

        # Compute the vorticity and reset the output values
        # accordingly.
        (dataspec, _) = xspharm.getvrtdivspec(ugrid=xuwnd, vgrid=xvwnd)
        vort[lev, :, :] = xspharm.spectogrd(dataspec=dataspec)
        vort[lev, :, :] = _reset_nan(vararr=vort[lev, :, :], ref_vararr=uwnd)

    # Deallocate memory for the spherical harmonic transform object.
    _cleanup(xspharm=xspharm)

    return vort


# ----


def global_wind_part(
    varobj: object,
) -> Tuple[
    numpy.array, numpy.array, numpy.array, numpy.array, numpy.array, numpy.array
]:
    """
    Description
    -----------

    This function computes the components of the total wind field
    using spherical harmonic transforms; the methodology follows from
    Lynch [1988].

    Parameters
    ----------

    varobj: object

        A Python object containing, at minimum, the zonal and
        meridional wind components; units are meters per second.

    Returns
    -------

    (udiv, vdiv): [numpy.array, numpy.array]

        The components of the divergent component of the global total
        wind field.

    (uhrm, vhrm): [numpy.array, numpy.array]

        The components of the harmonic (i.e., residual) component of
        the global total wind field.

    (uvor, vvort): [numpy.array, numpy.array]

        The components of the rotational component of the global total
        wind field.

    References
    ----------

    Lynch, P., 1994: Paritioning the Wind in a Limited
    Domain. Mon. Wea. Rev., 116, 86-93.

    https://doi.org/10.1175/1520-0493(1988)116<0086:DTWFVA>2.0.CO;2

    """

    # Initialize the local variable and objects.
    (udiv, uhrm, uvor, vdiv, vhrm, vvor) = [
        numpy.zeros(varobj.uwnd.shape) for idx in range(6)
    ]

    xspharm = _init_spharm(array_in=uvor)
    nlevs = uvor.shape[0]

    msg = f"Computing global partitioned total wind arrays of dimension {uvor.shape}."
    logger.info(msg=msg)

    # Compute the total wind components; proceed accordingly.
    for lev in range(nlevs):

        # Define the wind vector components.
        (uwnd, vwnd) = _get_lev_uv(varobj=varobj, lev=lev)
        xuwnd = _reset_nan2zero(vararr=uwnd)
        xvwnd = _reset_nan2zero(vararr=vwnd)

        (zspec_save, dspec_save) = xspharm.getvrtdivspec(ugrid=xuwnd, vgrid=xvwnd)

        # Compute the divergent component of the total wind field.
        (zspec, dspec) = [numpy.zeros(zspec_save.shape), dspec_save]
        (udiv[lev, :, :], vdiv[lev, :, :]) = xspharm.getuv(vrtspec=zspec, divspec=dspec)
        udiv[lev, :, :] = _reset_nan(vararr=udiv[lev, :, :], ref_vararr=uwnd)
        vdiv[lev, :, :] = _reset_nan(vararr=vdiv[lev, :, :], ref_vararr=vwnd)

        # Compute the rotational component of the total wind field.
        (zspec, dspec) = [zspec_save, numpy.zeros(dspec_save.shape)]
        (uvor[lev, :, :], vvor[lev, :, :]) = xspharm.getuv(vrtspec=zspec, divspec=dspec)
        uvor[lev, :, :] = _reset_nan(vararr=uvor[lev, :, :], ref_vararr=uwnd)
        vvor[lev, :, :] = _reset_nan(vararr=vvor[lev, :, :], ref_vararr=vwnd)

        # Compute the residual (i.e., harmonic) component of the total
        # wind field.
        uhrm[lev, :, :] = numpy.array(xuwnd[:, :]) - (uvor[lev, :, :] + udiv[lev, :, :])
        vhrm[lev, :, :] = numpy.array(xvwnd[:, :]) - (vvor[lev, :, :] + vdiv[lev, :, :])

    # Deallocate memory for the spherical harmonic transform object.
    _cleanup(xspharm=xspharm)

    return (udiv, vdiv, uhrm, vhrm, uvor, vvor)


# ----


def wndmag(varobj: object) -> numpy.array:
    """
    Description
    -----------

    This function computes the magnitude of the vector wind field.

    Parameters
    ----------

    varobj: object

        A Python object containing, at minimum, the zonal and
        meridional wind components; units are meters per second.

    Returns
    -------

    magwnd: numpy.array

        A Python array-type variable containing the magnitude of the
        total wind field.

    """

    # Initialize the local variable array.
    magwnd = numpy.zeros(varobj.uwnd.shape)

    # Compute the magnitude of the vector wind field.
    magwnd = numpy.sqrt(varobj.uwnd * varobj.uwnd + varobj.vwnd * varobj.vwnd)

    return magwnd
