# =========================================================================

# Module: ush/tcdiags/__init__.py

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

    __init__.py

Description
-----------

    This module contains the base-class object TCDiags.

Classes
-------

    TCDiags(options_obj)

        This is the base-class object for all tropical cyclone (TC)
        diagnostic computations and evaluations.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 11 March 2023

History
-------

    2023-03-11: Henry Winterbottom -- Initial implementation.

"""

# ----

from dataclasses import dataclass
from gc import collect
from importlib import import_module

from confs.yaml_interface import YAML
from tools import parser_interface
from utils.decorator_interface import privatemethod
from utils.logger_interface import Logger

from tcdiags.exceptions import TCDiagsError

# ----


@dataclass
class TCDiags:
    """
    Description
    -----------

    This is the base-class object for all tropical cyclone (TC)
    diagnostic computations and evaluations.

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

        Creates a new TCDiags object.

        """

        # Define the base-class attributes.
        self.options_obj = options_obj
        self.logger = Logger(caller_name=f"{__name__}.{self.__class__.__name__}")
        self.yaml_file = self.options_obj.yaml_file

        # Collect the experiment attributes from the YAML-formatted
        # configuration file; proceed accordingly.
        self.yaml_obj = YAML().read_yaml(yaml_file=self.yaml_file, return_obj=True)

        # Define the available applications.
        self.apps_list = ["tcmpi", "tcsteering", "tcwnmsi"]

    @privatemethod
    def config(self: dataclass) -> object:
        """
        Description
        -----------

        This method configures the application; the input attributes
        are collect for the respective input type (e.g., model,
        analysis, etc.,) and (if available) the information for the
        respective TCs to be analyzed.

        Returns
        -------

        tcdiags_obj: object

            A Python object containing all configuration attributes
            for the respective application including inputs (i.e.,
            `inputs` and `tcinfo`) as well as the remaining
            (supported) applications (see base-class attribute
            `apps_list`).

        Raises
        ------

        TCDiagsError:

            - raised if an exception is encountered while defining the
              input I/O module and/or class.

        """

        # Collect the mandatory/standard variables and attributes for
        # the respective input type.
        tcdiags_obj = parser_interface.object_define()

        yaml_obj = YAML().read_yaml(yaml_file=self.yaml_obj.inputs, return_obj=True)

        try:
            io_obj = parser_interface.object_getattr(
                import_module(yaml_obj.io_module),
                key=f"{yaml_obj.io_class}",
                force=True,
            )
        except Exception as errmsg:
            msg = (
                f"Defining the inputs I/O module failed with error {errmsg}. "
                "Aborting!!!"
            )
            raise TCDiagsError(msg=msg) from errmsg

        tcdiags_obj.inputs = io_obj(yaml_file=self.yaml_obj.inputs).read()

        # Check whether the TC information file has been provided;
        # proceed accordingly.
        if parser_interface.object_hasattr(object_in=self.yaml_obj, key="tcinfo"):
            tcdiags_obj.tcinfo = YAML().read_yaml(yaml_file=self.yaml_obj.tcinfo)

        else:
            msg = (
                "No TC-information attribute `tcvitals` was found in experiment "
                f"configuration file {self.yaml_file}; resetting to NoneType."
            )
            self.logger.warn(msg=msg)
            tcdiags_obj.tcinfo = None

        # Collect the information and configuration attributes for the
        # respective (supported) applications.
        for app in self.apps_list:
            if parser_interface.object_hasattr(object_in=self.yaml_obj, key=app):
                yaml_obj = YAML().read_yaml(
                    yaml_file=parser_interface.object_getattr(
                        object_in=self.yaml_obj, key=app, force=True
                    ),
                    return_obj=True,
                )

                if yaml_obj is None:
                    msg = (
                        "No configuration attributes have been specified for application "
                        f"{app}."
                    )
                    self.logger.warn(msg=msg)

                tcdiags_obj = parser_interface.object_setattr(
                    object_in=tcdiags_obj, key=app, value=yaml_obj
                )

        return tcdiags_obj

    def run(self: dataclass) -> None:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Reads the input variables from the specified file(s).

        (2) Launches the respective, and supported, TC diagnostics
            applications.

        """

        # Collect the configuration attributes.
        tcdiags_obj = self.config()

        # Execute each application; proceed accordingly.
        for app in self.apps_list:
            if (
                not parser_interface.object_getattr(
                    object_in=tcdiags_obj, key=app, force=True
                )
                is None
            ):
                msg = f"Executing application {app}."
                self.logger.info(msg=msg)

                app_obj = parser_interface.object_getattr(
                    object_in=tcdiags_obj, key=app, force=True
                )
                app_method = parser_interface.object_getattr(
                    import_module(app_obj.app_module), key=app_obj.app_class
                )
                app_method(tcdiags_obj=tcdiags_obj).run()
