# =========================================================================

# Script: scripts/cli/parser.py

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

    parser.py

Description
-----------

    This module contains the base-class object for all command-line
    interface (CLI) configuration parsing.

Classes
-------

    Parser()

        This is the base-class object for the command-line interface
        (CLI) argument parser.

Author(s)
---------

    Henry R. Winterbottom; 07 June 2023

History
-------

    2023-06-07: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from types import SimpleNamespace
from typing import Generic, Tuple

from tools import parser_interface
from utils.decorator_interface import privatemethod
from utils.exceptions_interface import CLIInterfaceError

# ----


class Parser:
    """
    Description
    -----------

    This is the base-class object for the command-line interface (CLI)
    argument parser; for each Python SimpleNamespace object for the
    respective mandatory, optional, and/or task argument the ancillary
    variables to those found at https://tinyurl.com/argparse-objects
    are as follows.

    - longname: a Python string defining the argument name; this is
      the string prefixed as `--longname` when passing the arguments
      to CLI; this is mandatory.

    - shortname: a Python string defining the argument shortened name;
      this is the string prefixed as `-shortname`; if NoneType, the
      respective argument help message will not include this string.

    """

    def __init__(self: Generic):
        """
        Description
        -----------

        Creates a new Parser object.

        """

    def build(self: Generic) -> Tuple[SimpleNamespace]:
        """
        Description
        -----------

        This method defines and collects the mandatory, optional, and
        task argument SimpleNamespace object tuples.

        Returns
        -------

        args_objs: Tuple[SimpleNamespace]

            A Python tuple of SimpleNamespace objects containing the
            mandatory, optional, and task arguments.

        """

        # Collect the mandatory, optional, and task argument
        # SimpleNamespace object tuples.
        args_objs = self.mandargs() + self.optargs() + self.taskargs()

        return args_objs

    @privatemethod
    def mandargs(self: Generic) -> Tuple[SimpleNamespace]:
        """
        Description
        -----------

        This method defines the tuple containing the mandatory
        argument SimpleNamespace objects.

        Returns
        -------

        args_objs: Tuple[SimpleNamespace]

            A Python tuple of SimpleNamespace objects for the
            mandatory arguments.

        Raises
        ------

        CLIInterfaceError:

            - raised if an exception is encountered while defining the
              respective CLI arguments.

        """

        # Build the SimpleNamespace objects for each mandatory argument.
        try:
            yaml_file = parser_interface.object_define()
            yaml_file.longname = "yaml_file"
            yaml_file.shortname = "y"
            yaml_file.required = True
            yaml_file.nargs = "?"
            yaml_file.type = str
            yaml_file.help = ("YAML-formatted tropical cyclone diagnostics "
                              "configuration file."
                              )

            args_objs = (yaml_file,)
        except Exception as errmsg:
            msg = (
                f"Defining the mandatory arguments failed with error {errmsg}. "
                "Aborting!!!"
            )
            raise CLIInterfaceError(msg=msg) from errmsg

        return args_objs

    @privatemethod
    def optargs(self: Generic) -> Tuple[SimpleNamespace]:
        """
        Description
        -----------

        This method defines the tuple containing the optional argument
        SimpleNamespace objects.

        Returns
        -------

        args_objs: Tuple[SimpleNamespace]

            A Python tuple of SimpleNamespace objects for the optional
            arguments.

        Raises
        ------

        CLIInterfaceError:

            - raised if an exception is encountered while defining the
              respective CLI arguments.

        """

        # Build the SimpleNamespace for each optional argument.
        try:
            schema = parser_interface.object_define()
            schema.longname = "schema"
            schema.shortname = "s"
            schema.required = False
            schema.nargs = "?"
            schema.type = str
            schema.help = "YAML-formatted file containing the CLI argument(s) schema."

            args_objs = (schema,)
        except Exception as errmsg:
            msg = (
                f"Defining the optional arguments failed with error {errmsg}. "
                "Aborting!!!"
            )
            raise CLIInterfaceError(msg=msg) from errmsg

        return args_objs

    @privatemethod
    def taskargs(self: Generic) -> Tuple[SimpleNamespace]:
        """
        Description
        -----------

        This method defines the tuple containing the task application
        argument SimpleNamespace objects.

        Returns
        -------

        args_objs: Tuple[SimpleNamespace]

            A Python tuple of SimpleNamespace objects for the task
            application arguments.

        Raises
        ------

        CLIInterfaceError:

            - raised if an exception is encountered while defining the
              respective CLI arguments.

        """

        # Build the SimpleNamespace objects for each task application
        # argument.
        try:
            tcfilter = parser_interface.object_define()
            tcfilter.longname = "tcfilter"
            tcfilter.action = "store_true"
            tcfilter.help = ("Run the tropical clone filtering application described by "
                             "Winterbottom and Chassignet [2011]"
                             )

            tcpi = parser_interface.object_define()
            tcpi.longname = "tcpi"
            tcpi.action = "store_true"
            tcpi.help = ("Run supported tropical cyclone potential intensity metric "
                         "applications."
                         )

            tcsteering = parser_interface.object_define()
            tcsteering.longname = "tcsteering"
            tcsteering.action = "store_true"
            tcsteering.help = ("Run supported tropical cyclone potential environmental "
                               "steering applications."
                               )

            tcmsi = parser_interface.object_define()
            tcmsi.longname = "tcmsi"
            tcmsi.action = "store_true"
            tcmsi.help = ("Run the tropical cyclone multi-scale intensity index application "
                          "described by Vukicevic et al., [2014]."
                          )

            args_objs = (tcfilter, tcpi, tcsteering, tcmsi)
        except Exception as errmsg:
            msg = (
                f"Defining the task application arguments failed with error {errmsg}. "
                "Aborting!!!"
            )
            raise CLIInterfaceError(msg=msg) from errmsg

        return args_objs
