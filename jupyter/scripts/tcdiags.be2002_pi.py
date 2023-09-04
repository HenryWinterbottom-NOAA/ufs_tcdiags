#!/usr/bin/env python3

# =========================================================================
# File: scripts/compute_tcdiags.py
# Author: Henry R. Winterbottom
# Date: 03 March 2023
# Version: 0.0.1
# License: LGPL v2.1
# =========================================================================

"""
Script
------

    tcdiags.be2002_pi.py

Description
-----------

    This script computes and plots the tropical cyclone (TC) potential
    intensity (PI) metrics described by Bister and Emanuel [2002].

Classes
-------

    BE2002(options_obj)

        This is the base-class object for all tropical cyclone
        potential intensity metric computations and plottings.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

References
----------

    Bister, M., and K. A. Emanuel. "Low frequency variability of
    tropical cyclone potential intensity, 1, Interannual to
    interdecadal variability". Journal of Geophysical Research 107
    (2002): 4801.

    Gifford, D. M., "pyPI (v1.3): Tropical cyclone potential intensity
    calculations in Python". Geoscientific Model Development 14
    (2020): 2351-2369.

Author(s)
---------

    Henry R. Winterbottom; 26 August 2023

History
-------

    2023-08-26: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=too-many-locals

# ----

import os
import time
from types import SimpleNamespace
from typing import Generic

import matplotlib.pyplot as plt
import numpy
from cmocean.cm import haline
from plottools.build_basemap import build_basemap
from plottools.draw_basemap import draw_basemap
from tcdiags.tcdiags import TCDiags
from tools import parser_interface
from utils import cli_interface
from utils.cli_interface import CLIParser
from utils.logger_interface import Logger

# ----

logger = Logger(caller_name=__name__)

# ----


class BE2002:
    """
    Description
    -----------

    This is the base-class object for all tropical cyclone potential
    intensity metric computations and plottings.

    Parameters
    ----------

    options_obj: SimpleNamespace

        A Python SimpleNamespace object containing the command line
        argument attributes.

    """

    def __init__(self: Generic, options_obj: SimpleNamespace):
        """
        Description
        -----------

        Creates a new BE2002 object.

        """

        # Define the base-class attributes.
        self.logger = Logger(caller_name=f"{__name__}.{self.__class__.__name__}")
        self.options_obj = options_obj
        self.options_obj.tcpi = True
        self.tcdiags_obj = TCDiags(options_obj=options_obj)

    def compute(self: Generic) -> SimpleNamespace:
        """
        Description
        -----------

        This method computes the tropical cyclone potential intensity
        metrics.

        Returns
        -------

        tcpi_obj: SimpleNamespace

            A Python SimpleNamespace object containing the computed
            tropical cyclone potential intensity metrics.

        """

        # Compute the potential intensity metric.
        tcpi_obj = self.tcdiags_obj.run().tcpi

        return tcpi_obj

    def plot(self: Generic, tcpi_obj: SimpleNamespace) -> None:
        """
        Description
        -----------

        This method plots the potential intensity metrics.

        Parameters
        ----------

        tcpi_obj: SimpleNamespace

            A Python SimpleNamespace object containing the computed
            tropical cyclone potential intensity metrics.

        """

        # Define the sea-level pressure potential intensity plotting
        # attributes.
        mslp_cint = 25.0
        mslp_cmax = 1025.0
        mslp_cmin = 850.0
        mslp_cmap = haline

        # Define the wind speed potential intensity plotting
        # attributes.
        vmax_cint = 20.0
        vmax_cmax = 120.0
        vmax_cmin = 0.0
        vmax_cmap = "jet"

        # Plot the sea-level pressure potential intensity.
        msg = "Plotting the tropical cyclone sea-level pressure potential intensity."
        self.logger.info(msg=msg)
        levels = numpy.linspace(mslp_cmin, mslp_cmax, 255)
        (basemap, x, y) = build_basemap(lat=tcpi_obj.lats, lon=tcpi_obj.lons)
        draw_basemap(basemap=basemap)
        basemap.contourf(x, y, tcpi_obj.pmin.values, levels=levels, cmap=mslp_cmap)
        ticks = numpy.arange(mslp_cmin, (mslp_cmax + 0.01), mslp_cint)
        plt.colorbar(
            orientation="horizontal",
            ticks=ticks,
            pad=0.1,
            aspect=50,
            label="Potential Intensity :: Sea-Level Pressure (hPa)",
        )
        plt.tight_layout()
        plt.show()

        # Plot the wind speed potential intensity.
        msg = "Plotting the tropical cyclone wind speed potential intensity."
        self.logger.info(msg=msg)
        levels = numpy.linspace(vmax_cmin, vmax_cmax, 255)
        (basemap, x, y) = build_basemap(lat=tcpi_obj.lats, lon=tcpi_obj.lons)
        draw_basemap(basemap=basemap)
        basemap.contourf(x, y, tcpi_obj.vmax.values, levels=levels, cmap=vmax_cmap)
        ticks = numpy.arange(vmax_cmin, (vmax_cmax + 0.01), vmax_cint)
        plt.colorbar(
            orientation="horizontal",
            ticks=ticks,
            pad=0.1,
            aspect=50,
            label="Potential Intensity :: Wind Speed (mps)",
        )
        plt.tight_layout()
        plt.show()

    def run(self: Generic) -> None:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Computes the tropical cyclone potential intensity metrics.

        (2) Plots the specified tropical cyclone potential intensity
            metrics.

        """

        # Compute and plot the tropical cyclone potential intensity
        # metrics.
        tcpi_obj = self.compute()
        self.plot(tcpi_obj=tcpi_obj)


# ----


def main() -> None:
    """
    Description
    -----------

    This is the driver-level function to invoke the tasks within this
    script.

    """

    # Collect the command line arguments.
    script_name = os.path.basename(__file__)
    start_time = time.time()
    msg = f"Beginning application {script_name}."
    logger.status(msg=msg)
    parser_interface.enviro_set(
        envvar="CLI_SCHEMA",
        value=os.path.join(os.getcwd(), "schema", "tcdiags.schema.yaml"),
    )
    args_objs = CLIParser().build()
    parser = cli_interface.init(
        args_objs=args_objs,
        description="Tropical cyclone potential intensity computation and plotting application interface.",
        prog=os.path.basename(__file__),
    )
    options_obj = cli_interface.options(parser=parser)

    # Launch the task.
    task = BE2002(options_obj=options_obj)
    task.run()
    stop_time = time.time()
    msg = f"Completed application {script_name}."
    logger.status(msg=msg)
    total_time = stop_time - start_time
    msg = f"Total Elapsed Time: {total_time} seconds."
    logger.status(msg=msg)


# ----


if __name__ == "__main__":
    main()
