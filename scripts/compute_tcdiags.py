#!/usr/bin/env python3

"""
Script
------

    compute_tcdiags.py

Description
-----------

    This script is the driver script for tropical cyclone (TC) related
    diagnostics and evaluations.

Classes
-------

    ComputeTCDiags(options_obj)

        This is the base-class object for all tcdiags applications.

Functions
---------

    main()

        This is the driver-level function to invoke the tasks within
        this script.

Usage
-----

    user@host:$ python compute_tcdiags.py --help

    Usage: compute_tcdiags.py [-h] [-tcmsi] [-tcpi] [-tcstrflw] yaml

    Tropical cyclone diagnostics computation(s) application interface.

    Positional Arguments:
      yaml        YAML-formatted tropical cyclone diagnostics configuration file.

    Optional Arguments:
      -h, --help  show this help message and exit
      -tcmsi      YAML-formatted file containing the TC multi-scale intensity application configuration.
      -tcpi       YAML-formatted file containing the TC potential intensity application configuration.
      -tcstrflw   YAML-formatted file containing the TC steering application configuration.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 03 March 2023

History
-------

    2023-03-03: Henry Winterbottom -- Initial implementation.

"""

# ----

import os
import time
from tcdiags.tcdiags import TCDiags
from tools import fileio_interface, parser_interface
from utils import cli_interface
from utils.cli_interface import CLIParser
from utils.logger_interface import Logger
from utils.logger_interface import Logger

# ----

logger = Logger(caller_name=__name__)

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
        value=os.path.join(os.getcwd(), "schema",
                           "compute_tcdiags.schema.yaml"),
    )
    args_objs = CLIParser().build()
    parser = cli_interface.init(
        args_objs=args_objs,
        description="Tropical cyclone diagnostics computation(s) application interface.",
        prog=os.path.basename(__file__),
    )
    options_obj = cli_interface.options(parser=parser)

    # Launch the task.
    task = TCDiags(options_obj=options_obj)
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
