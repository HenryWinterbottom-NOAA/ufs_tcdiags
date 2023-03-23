# =========================================================================

# Script: tools/tcv2yaml.py

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

    tcv2yaml.py

Description
-----------

    This script is the driver script to writing tropical cyclone (TC)
    observation-type attributes (e.g., TC-vitals) to a specified
    YAML-formatted file.

Classes
-------

    TCVtoYAML(options_obj)

        This is the base-class object for all TC-vitals to YAML-format
        applications.

Functions
---------

    main()

        This is the driver-level function to invoke the tasks within
        this script.

Usage
-----

    user@host:$ python tcv2yaml --tcv_path /path/to/input/tcvitals_file --yaml_file /path/to/output/yaml_file

Parameters
----------

    tcv_path: str

        A Python string specifying the path to the TC-vitals formatted
        file.

    yaml_file: str

        A Python string specifying the path to where the
        YAML-formatted TC-vitals record(s) is (are) to be written.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 22 March 2023

History
-------

    2023-03-22: Henry Winterbottom -- Initial implementation.

"""

# ----

import os
import time
from dataclasses import dataclass
from typing import Dict

from confs.yaml_interface import YAML
from ioapps import tcvitals_interface
from utils.arguments_interface import Arguments
from utils.logger_interface import Logger

from tools import parser_interface

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

# Specify whether to evaluate the format for the respective parameter
# values.
EVAL_SCHEMA = True

# Define the schema attributes.
CLS_SCHEMA = {"tcv_path": str, "yaml_file": str}

# ----


@dataclass
class TCVtoYAML:
    """
    Description
    -----------

    This is the base-class object for all TC-vitals to YAML-format
    applications.

    Parameters
    ----------

    options_obj: object

        A Python object containing the command line argument
        attributes.

    """

    def __init__(self, options_obj: object):
        """
        Description
        -----------

        Creates a new TCVtoYAML object.

        """

        # Define the base-class attributes.
        self.options_obj = options_obj
        self.tcvout_obj = parser_interface.object_define()

        self.yaml_attrs_list = ["lat", "lon",
                                "mslp", "poci", "rmw", "roci", "vmax"]

    def format_tcv(self) -> object:
        """
        Description
        -----------

        This method reads a TC-vitals record(s) and formats the
        relevant variables to their corresponding MKS system of units
        and writes a YAML-formatted record for each TC-vitals record.

        """

        # Read the TC-vitals records.
        tcv_obj = self.read_tcv()

        # Format the TC-vitals records accordingly.
        for tcv in vars(tcv_obj):

            # Collect the attributes for the respective TC-vitals
            # record.
            tcv_dict = parser_interface.object_getattr(
                object_in=tcv_obj, key=tcv)

            # Scale/format the TC-vitals record attributes
            # accordingly.
            tcvitals_interface.scale_tcvrec(tcv_dict=tcv_dict)

            # Scale the TC-vitals attributes for the respective record
            # and update the respective TC-vitals records.
            tcvout_obj = tcvitals_interface.scale_tcvrec(tcv_dict=tcv_dict)

            for item in self.yaml_attrs_list:
                tcv_dict[item] = parser_interface.object_getattr(
                    object_in=tcvout_obj, key=item
                )

            # Write the respective TC-vitals record YAMLs.
            self.write_yaml(tcv_dict=tcv_dict)

    def read_tcv(self) -> object:
        """
        Description
        -----------

        This method reads a TC-vitals record(s) and returns a Python
        object containing the respective record(s) attributes.

        Returns
        -------

        tcv_obj: object

            A Python object containing the respective TC-vitals
            record(s) attributes.

        """

        # Read the TC-vitals records.
        tcv_obj = tcvitals_interface.read_tcvfile(
            filepath=self.options_obj.tcv_path)

        return tcv_obj

    def write_yaml(self, tcv_dict: Dict) -> None:
        """
        Description
        -----------

        This method writes a YAML-formatted record, to a specified
        YAML-formatted file path, containing the respective TC-vitals
        record attributes.

        Parameters
        ----------

        tcv_dict: dict

             A Python dictionary containing the TC-vitals record
             attributes.

        """

        # Build the Python dictionary accordingly.
        yaml_dict = {}
        yaml_dict[tcv_dict["tcid"]] = dict(
            (key, tcv_dict[key]) for key in self.yaml_attrs_list
        )

        # Write the TC-vitals record as a YAML record.
        YAML().write_yaml(
            yaml_file=self.options_obj.yaml_file, in_dict=yaml_dict, append=True
        )

    def run(self):
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Reads a TC-vitals formatted file and returns the
            respective records.

        (2) Formats the respective TC-vitals record(s) attributes.

        (3) Writes the respective TC-vitals record(s) attributes to a
            specified YAML-formatted file path.

        """

        # Read, format, and write the TC-vitals records to the
        # specified YAML-formatted file path.
        self.format_tcv()


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
    Logger().info(msg=msg)
    options_obj = Arguments().run(eval_schema=EVAL_SCHEMA, cls_schema=CLS_SCHEMA)

    # Launch the task.
    task = TCVtoYAML(options_obj=options_obj)
    task.run()

    stop_time = time.time()
    msg = f"Completed application {script_name}."
    Logger().info(msg=msg)
    total_time = stop_time - start_time
    msg = f"Total Elapsed Time: {total_time} seconds."
    Logger().info(msg=msg)


# ----


if __name__ == "__main__":
    main()
