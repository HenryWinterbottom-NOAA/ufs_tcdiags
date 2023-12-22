"""
Module
------

    lv1972_ohc.py

Description
-----------

    This module contains functions to plot variables relevant to the
    Leipper and Volgenau (1972) ocean heat content (OHC) and tropical
    cyclone heat potential (TCHP).

Functions
---------

    basemap_update(func)

        This function is a wrapper function for updating specified
        basemap attributes.

    lv1972_ohc_isodpth(ohc_obj, basemap_obj)

        This function plots the depth of the 26 Celcius isotherm.

    lv1972_ohc_ohc(ohc_obj, basemap_obj)

        This function plots the column-integrated ocean heat content
        (OHC).

    lv1972_ohc_sst(ohc_obj, basemap_obj)

         This function plots the sea-surface temperature (SST) and the
         26 Celcius isotherm.

    lv1972_ohc_tchp(ohc_obj, basemap_obj)

         This function plots the tropical cyclone heat potential
         (TCHP).

Requirements
------------

- cmocean; https://github.com/matplotlib/cmocean

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 22 December 2023

History
-------

    2023-12-22: Henry Winterbottom -- Initial implementation.


"""

# pylint: disable=anomalous-backslash-in-string
# pylint: disable=too-many-locals
# pylint: disable=unused-argument

# ----

import functools
from types import SimpleNamespace
from typing import Callable, Dict, Tuple

from cmocean.cm import deep, haline, thermal
import matplotlib.pyplot as plt
import numpy
from tcdiags.plot.plotter import plotter

# ----

# Define all available module properties
__all__ = ["lv1972_ohc_isodpth", "lv1972_ohc_ohc", "lv1972_ohc_sst", "lv1972_ohc_tchp"]

# ----


def basemap_update(func: Callable) -> Callable:
    """
    Description
    -----------

    This function is a wrapper function for updating specified basemap
    attributes.

    Parameters
    ----------

    func: ``Callable``

        A Python Callable object containing the function to be
        wrapped.

    Returns
    -------

    wrapped_function: ``Callable``

        A Python Callable object containing the wrapped function.

    """

    @functools.wraps(func)
    def wrapped_function(*args, **kwargs) -> Callable:
        """
        Description
        -----------

        This method modifies the specified basemap attributes.

        Other Parameters
        ----------------

        args: ``Tuple``

            A Python tuple containing additional arguments passed to
            the constructor.

        kwargs: ``Dict``

            A Python dictionary containing additional key and value
            pairs to be passed to the constructor.

        """

        # Modify the respective basemap attributes.
        basemap_obj = func(*args, **kwargs)
        for meridian in basemap_obj.drawmeridians.values():
            for text in meridian[1]:
                text.update({"fontsize": 8})
        for parallel in basemap_obj.drawparallels.values():
            for text in parallel[1]:
                text.update({"fontsize": 8})

        return basemap_obj

    return wrapped_function


# ----


@plotter(save_name="lv1972_ohc_isodpth.png", dpi=500)
@basemap_update
def lv1972_ohc_isodpth(
    ohc_obj: SimpleNamespace, basemap_obj: SimpleNamespace, *args: Tuple, **kwargs: Dict
) -> None:
    """
    Description
    -----------

    This function plots the depth of the 26 Celcius isotherm.

    Parameters
    ----------

    ohc_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the ocean heat
        content (OHC) attributes.

    basemap_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the basemap
        attributes.

    Other Parameters
    ----------------

    args: ``Tuple``

        A Python tuple containing additional arguments passed to the
        constructor.

    kwargs: ``Dict``

        A Python dictionary containing additional key and value pairs
        to be passed to the constructor.

    """

    # Define the plotting attributes.
    isotherm = ohc_obj.isotherm[...]
    mask = isotherm <= 0
    isotherm = numpy.ma.masked_array(isotherm, mask)
    (isodpth_min, isodpth_max) = (0.0, 750.01)
    levels = numpy.linspace(isodpth_min, isodpth_max, 255)
    ticks = numpy.arange(isodpth_min, isodpth_max, 75)
    cmap = deep
    lats = numpy.array(ohc_obj.lats)
    lons = numpy.array(ohc_obj.lons)

    # Plot the TCHP isotherm depth.
    basemap_kwargs = {"cmap": cmap, "levels": levels}
    basemap_obj.Basemap.contourf(lons, lats, isotherm, **basemap_kwargs)
    cbar = plt.colorbar(
        orientation="horizontal",
        ticks=ticks,
        pad=0.1,
        aspect=50,
    )
    cbar.set_label("Depth of the 26${\degree}$C Isotherm (m)", fontsize=10)
    cbar.ax.tick_params(labelsize=8)

    return basemap_obj


# ----


@plotter(save_name="lv1972_ohc_ohc.png", dpi=500)
@basemap_update
def lv1972_ohc_ohc(
    ohc_obj: SimpleNamespace, basemap_obj: SimpleNamespace, *args: Tuple, **kwargs: Dict
) -> None:
    """
    Description
    -----------

    This function plots the column-integrated ocean heat content
    (OHC).

    Parameters
    ----------

    ohc_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the ocean heat
        content (OHC) attributes.

    basemap_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the basemap
        attributes.

    Other Parameters
    ----------------

    args: ``Tuple``

        A Python tuple containing additional arguments passed to the
        constructor.

    kwargs: ``Dict``

        A Python dictionary containing additional key and value pairs
        to be passed to the constructor.

    """

    # Define the plotting attributes.
    ohc = numpy.trapz(numpy.array(ohc_obj.ohc), axis=0) / 1000.0
    (ohc_min, ohc_max) = (0.0, 200.01)
    levels = numpy.linspace(ohc_min, ohc_max, 255)
    ticks = numpy.arange(ohc_min, ohc_max, 20.0)
    cmap = thermal
    lats = numpy.array(ohc_obj.lats)
    lons = numpy.array(ohc_obj.lons)

    # Plot the column-integrated ocean heatcontent.
    basemap_obj.Basemap.bluemarble()
    basemap_kwargs = {"cmap": cmap, "levels": levels}
    basemap_obj.Basemap.contourf(lons, lats, ohc, **basemap_kwargs)
    cbar = plt.colorbar(
        orientation="horizontal",
        ticks=ticks,
        pad=0.1,
        aspect=50,
    )
    cbar.set_label("Column Integrated Ocean Heat Content (Joules)", fontsize=10)
    cbar.ax.tick_params(labelsize=8)

    return basemap_obj


# ----


@plotter(save_name="lv1972_ohc_sst.png", dpi=500)
@basemap_update
def lv1972_ohc_sst(
    ohc_obj: SimpleNamespace, basemap_obj: SimpleNamespace, *args: Tuple, **kwargs: Dict
) -> None:
    """
    Description
    -----------

    This function plots the sea-surface temperature (SST) and the 26
    Celcius isotherm.

    Parameters
    ----------

    ohc_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the ocean heat
        content (OHC) attributes.

    basemap_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the basemap
        attributes.

    Other Parameters
    ----------------

    args: ``Tuple``

        A Python tuple containing additional arguments passed to the
        constructor.

    kwargs: ``Dict``

        A Python dictionary containing additional key and value pairs
        to be passed to the constructor.

    """

    # Define the plotting attributes.
    ctemp = ohc_obj.ctemp[0, ...]
    (ctemp_min, ctemp_max) = (-5.0, 35.01)
    levels = numpy.linspace(ctemp_min, ctemp_max, 255)
    ticks = numpy.arange(ctemp_min, ctemp_max, 5.0)
    cmap = haline
    lats = numpy.array(ohc_obj.lats)
    lons = numpy.array(ohc_obj.lons)

    # Plot the sea-surface temperature.
    basemap_obj.Basemap.bluemarble()
    basemap_kwargs = {"levels": levels, "cmap": cmap}
    basemap_obj.Basemap.contourf(lons, lats, ctemp, **basemap_kwargs)
    cbar = plt.colorbar(
        orientation="horizontal",
        ticks=ticks,
        pad=0.1,
        aspect=50,
    )
    cbar.set_label("Sea-surface Temperature (${\degree}$C)", fontsize=10)
    cbar.ax.tick_params(labelsize=8)
    colors = "red"
    linewidths = 0.5
    levels = [26.0]
    basemap_kwargs = {"colors": colors, "linewidths": linewidths, "levels": levels}
    basemap_obj.Basemap.contour(lons, lats, ctemp, **basemap_kwargs)

    return basemap_obj


# ----


@plotter(save_name="lv1972_ohc_tchp.png", dpi=500)
@basemap_update
def lv1972_ohc_tchp(
    ohc_obj: SimpleNamespace, basemap_obj: SimpleNamespace, *args: Tuple, **kwargs: Dict
) -> None:
    """
    Description
    -----------

    This function plots the tropical cyclone heat potential (TCHP).

    Parameters
    ----------

    ohc_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the ocean heat
        content (OHC) attributes.

    basemap_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the basemap
        attributes.

    Other Parameters
    ----------------

    args: ``Tuple``

        A Python tuple containing additional arguments passed to the
        constructor.

    kwargs: ``Dict``

        A Python dictionary containing additional key and value pairs
        to be passed to the constructor.

    """

    # Define the plotting attributes.
    ohc = numpy.array(ohc_obj.tchp[...] / 1000.0)
    mask = ohc <= 0
    ohc = numpy.ma.masked_array(ohc, mask)
    (ohc_min, ohc_max) = (0.0, 200.01)
    levels = numpy.linspace(ohc_min, ohc_max, 255)
    ticks = numpy.arange(ohc_min, ohc_max, 20.0)
    cmap = thermal
    lats = numpy.array(ohc_obj.lats)
    lons = numpy.array(ohc_obj.lons)

    # Plot the column-integrated ocean heatcontent.
    basemap_kwargs = {"cmap": cmap, "levels": levels}
    basemap_obj.Basemap.contourf(lons, lats, ohc, **basemap_kwargs)
    cbar = plt.colorbar(
        orientation="horizontal",
        ticks=ticks,
        pad=0.1,
        aspect=50,
    )
    cbar.set_label("Tropical Cyclone Heat Potential (Joules m$^{-2}$)", fontsize=10)
    cbar.ax.tick_params(labelsize=8)

    return basemap_obj
