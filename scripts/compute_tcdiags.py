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

Keywords
--------

    tcfilt: bool, optional

        A Python boolean valued variable specifying whether to apply
        the tropical cyclone (TC) filtering application described in
        Winterbottom and Chassignet [2011] to the TCs defined within
        the syndat-formatted filepath defined in the experiment
        configuration; if not specified the attribute defaults to
        NoneType.

    tcmpi: bool, optional

        A Python boolean valued variable specifying whether to compute
        the tropical cyclone (TC) (maximum) potential intensity
        following the methodlogy of Bister and Emanuel [2002].

    tcwnmsi: bool, optional

        A Python boolean valued variable specifying whether to compute
        the wave-number decomposition and the tropical cyclone (TC)
        multi-scale intensity (MSI) indice values following Vukicevic
        et al., [2014].

Requirements
------------

- schema; https://github.com/keleshev/schema

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

import os
import time
from dataclasses import dataclass

from schema import Optional
from tcdiags import TCDiags
from utils.arguments_interface import Arguments
from utils.logger_interface import Logger

# ----

# Specify whether to evaluate the format for the respective parameter
# values.
EVAL_SCHEMA = True

# TODO: Only YAML-formatted file should be passed; from that information the application/compuations should be decided.
# Define the schema attributes.
CLS_SCHEMA = {
    "yaml_file": str,
    Optional("tcfilt", default=False): bool,
    Optional("tcmpi", default=False): bool,
    Optional("tcsteering", default=False): bool,
    Optional("tcwnmsi", default=False): bool
}

# ----


@dataclass
class ComputeTCDiags:
    """
    Description
    -----------

    This is the base-class object for all tcdiags applications.

    Parameters
    ----------

    options_obj: object

        A Python object containing the command line argument
        attributes.

    """

    def __init__(self: dataclass, options_obj: object):
        """
        Description
        -----------

        Creates a new ComputeTCDiags object.

        """

        # Define the base-class attributes.
        self.options_obj = options_obj
        self.tcdiags = TCDiags(options_obj=self.options_obj)

    def run(self: dataclass) -> None:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Executes the tcdiags application to compute and output
            tropical cyclone (TC) related diagnostics.

        """

        self.tcdiags.run()


# ----


def main() -> None:
    """
    Description
    -----------

    This is the driver-level function to invoke the tasks within this
    script.

    """

    # Collect the command line arguments.
    caller_name = __name__
    script_name = os.path.basename(__file__)
    start_time = time.time()
    msg = f"Beginning application {script_name}."
    Logger(caller_name=caller_name).info(msg=msg)
    options_obj = Arguments().run(eval_schema=EVAL_SCHEMA, cls_schema=CLS_SCHEMA)

    # Launch the task.
    task = ComputeTCDiags(options_obj=options_obj)
    task.run()

    stop_time = time.time()
    msg = f"Completed application {script_name}."
    Logger(caller_name=caller_name).info(msg=msg)
    total_time = stop_time - start_time
    msg = f"Total Elapsed Time: {total_time} seconds."
    Logger(caller_name=caller_name).info(msg=msg)


# ----


if __name__ == "__main__":
    main()
