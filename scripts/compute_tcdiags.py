#!/usr/bin/env python3

# =========================================================================

# Script: scripts/compute_tcdiags.py

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

    user@host:$ python compute_tcdiags.py --yaml_file /path/to/yaml_file [--tcfilt True] [--tcmpi True] [--tcwnmsi True]

Parameters
----------

    yaml_file: str

        A Python string specifying the path to the YAML-formatted
        configuration file for the tropical cyclone (TC) diagnostics
        applications.

Directives
----------

    tcfilt: bool, optional

        A Python boolean valued variable specifying whether to apply
        the tropical cyclone (TC) filtering application described in
        Winterbottom and Chassignet [2011] to the TCs defined within
        the syndat-formatted filepath defined in the experiment
        configuration; if not specified the attribute defaults to
        NoneType.

    tcmpi: None

        A Python boolean valued variable specifying whether to compute
        the tropical cyclone (TC) (maximum) potential intensity
        following the methodlogy of Bister and Emanuel [2002].

    tcwnmsi: None

        A Python boolean valued variable specifying whether to compute
        the wave-number decomposition and the tropical cyclone (TC)
        multi-scale intensity (MSI) indice values following Vukicevic
        et al., [2014].

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

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from argparse import ArgumentParser
import os
import time

from tools import fileio_interface

from tools import parser_interface

from cli.parser import Parser
from utils import cli_interface

from tcdiags.tcdiags import TCDiags

from utils.logger_interface import Logger

# ----

logger = Logger(caller_name=__name__)

# ----

# Define the default schema; values specified for the `--schema`
# argument will override this value.
schema_path = os.path.join(os.path.dirname(os.getcwd()),
                           "parm",
                           "schema",
                           "schema.scripts_compute_tcdiags.yaml",
                           )
if not fileio_interface.fileexist(path=schema_path):
    msg = (
        f"The YAML-formatted default schema file {schema_path} does not exist. "
        "Aborting!!!"
    )
    logger.error(msg=msg)
    raise FileNotFoundError()

# ----


def __getparser__() -> ArgumentParser:
    """
    Description
    -----------

    This function collect the command-line arguments; optional
    arguments maybe pass as specified within the YAML formatted file
    containing the schema description.

    Returns
    -------

    parser: ArgumentParser

        A Python ArgumentParser object containing the specified
        command line arguments/attributes.

    """

    # Collect the command-line arguments and define the CLI argument
    # parser.
    args_objs = Parser().build()
    parser = cli_interface.init(
        args_objs=args_objs,
        description="Experiment script for UFS tropical cyclone "
        "diagnostics applications.", prog="compute_tcdiags.py",
    )

    return parser

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
    logger.info(msg=msg)
    parser = __getparser__()
    options_obj = cli_interface.options(
        parser=parser, validate_schema=True, schema_path=schema_path
    )

    # Launch the task.
    task = TCDiags(options_obj=options_obj)
    task.run()

    stop_time = time.time()
    msg = f"Completed application {script_name}."
    logger.info(msg=msg)
    total_time = stop_time - start_time
    msg = f"Total Elapsed Time: {total_time} seconds."
    logger.info(msg=msg)


# ----


if __name__ == "__main__":
    main()
