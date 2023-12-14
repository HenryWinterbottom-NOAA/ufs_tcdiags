#!/usr/bin/env python3

"""
Script
------

    tcinfo_yaml.py

Description
-----------

    This script is the driver script to create the tropical cyclone
    (TC) input attributes file.

Classes
-------

    TCInfoYAML(options_obj)

        This is the base-class object for all YAML-formatted TC
        information/attribute file creations from supported input
        types.

Functions
---------

    main()

        This is the driver-level function to invoke the tasks within
        this script.

Usage
-----

   user@host:$ ./tcinfo_yaml.py --help

   Usage: tcinfo_yaml.py [-h] [-atcf] input yaml

   Tropical cyclone diagnostics computation(s) application interface.

   Positional Arguments:
     input       An input file, of a supported type, containing the TC
                   information to be formatted.
     yaml        Path to the YAML-formatted TC information attributes file.

   Optional Arguments:
     -h, --help  show this help message and exit
     -atcf       TC information collected from a ATCF (e.g., TC-vitals)
                   formatted file.

Requirements
------------

- ufs_obs; https://github.com/HenryWinterbottom-NOAA/ufs_obs

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 12 September 2023

History
-------

    2023-09-12: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=no-value-for-parameter

# ----

import os
from types import SimpleNamespace
from typing import Generic

from atcf import ATCF
from confs.yaml_interface import YAML
from tools import parser_interface
from utils.decorator_interface import cli_wrapper, script_wrapper
from utils.logger_interface import Logger

# ----

logger = Logger(caller_name=__name__)

# ----


class TCInfoYAML:
    """
    Description
    -----------

    This is the base-class object for all YAML-formatted TC
    information/attribute file creations from supported input types.

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

        Creates a new TCInfoYAML object.

        """

        # Define the base-class attributes.
        self.logger = Logger(caller_name=f"{__name__}.{self.__class__.__name__}")
        self.options_obj = options_obj
        self.tcinfo_obj = parser_interface.object_define()
        self.atcf = ATCF()

    def write_yaml(self: Generic, tcinfo_obj: SimpleNamespace) -> None:
        """
        Description
        -----------

        This method writes a YAML-formatted file containing the
        respective TC event attributes.

        Parameters
        ----------

        tcinfo_obj: SimpleNamespace

            A Python SimpleNamespace object containing the respective
            TC event attributes.

        """

        msg = f"Creating YAML-formatted file {self.options_obj.yaml}."
        self.logger.info(msg=msg)
        yaml_dict = {}
        for item in vars(tcinfo_obj).keys():
            tcobj = parser_interface.object_getattr(
                object_in=tcinfo_obj, key=item, force=True
            )
            msg = f"Building record for TC {tcobj.tcid}."
            self.logger.info(msg=msg)
            yaml_dict[tcobj.tcid] = {
                "lat_deg": tcobj.lat.magnitude,
                "lon_deg": tcobj.lon.magnitude,
            }
        YAML().write_yaml(yaml_file=self.options_obj.yaml, in_dict=yaml_dict)

    def run(self: Generic) -> None:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Reads the TC event attributes from the specified input
            formatted file.

        (2) Builds a Python SimpleNamespace object containing the
            relevant TC event attributes.

        (3) Writes the TC event attributes to the specified
            YAML-formatted file path.

        """

        # Proceed according to the input file format type.
        if self.options_obj.atcf:
            tcinfo_obj = self.atcf.read(atcf_filepath=self.options_obj.input)

        # Write the YAML-formatted TC event(s) attributes.
        self.write_yaml(tcinfo_obj=tcinfo_obj)


# ----

DESCRIPTION = "Tropical cyclone diagnostics computation(s) application interface."
SCHEMA_FILE = os.path.join(
    parser_interface.enviro_get("TCDIAGS_ROOT"),
    "scripts",
    "schema",
    "tcinfo_yaml.schema.yaml",
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
    task = TCInfoYAML(options_obj=options_obj)
    task.run()


# ----


if __name__ == "__main__":
    main()
