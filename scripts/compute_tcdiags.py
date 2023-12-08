#!/usr/bin/env python3

# ----

# pylint: disable=line-too-long
# pylint: disable=no-value-for-parameter

# ----

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

    Usage: compute_tcdiags.py [-h] [-tcmsi] [-tcpi] [-tcohc] [-tcstrflw] yaml

    Tropical cyclone diagnostics interface.

    Positional Arguments:
      yaml        YAML-formatted tropical cyclone diagnostics configuration file.

    Optional Arguments:
      -h, --help  show this help message and exit
      -tcmsi      YAML-formatted file containing the TC multi-scale intensity application configuration.
      -tcpi       YAML-formatted file containing the TC potential intensity application configuration.
      -tcohc      YAML-formatted file containing the TC relative ocean heat-content application configuration.
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
from types import SimpleNamespace

from tcdiags.tcdiags import TCDiags
from tools import parser_interface
from utils.decorator_interface import cli_wrapper, script_wrapper

# ----

DESCRIPTION = "Tropical cyclone diagnostics interface."
SCHEMA_FILE = os.path.join(
    parser_interface.enviro_get("TCDIAGS_ROOT"),
    "scripts",
    "schema",
    "compute_tcdiags.schema.yaml",
)
SCRIPT_NAME = os.path.basename(__file__)


@cli_wrapper(description=DESCRIPTION, schema_file=SCHEMA_FILE, script_name=SCRIPT_NAME)
@script_wrapper(script_name=SCRIPT_NAME)
def main(options_obj: SimpleNamespace) -> None:
    """
    Description
    -----------

    This is the driver-level function to invoke the tasks within this
    script.

    """

    # Launch the task.
    task = TCDiags(options_obj=options_obj)
    task.run()


# ----


if __name__ == "__main__":
    main()
