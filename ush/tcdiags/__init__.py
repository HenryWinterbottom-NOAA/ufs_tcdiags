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

from confs.yaml_interface import YAML
from tcdiags.exceptions import TCDiagsError
from tools import parser_interface
from utils.logger_interface import Logger

from tcdiags.io.gfs import GFS
# from tcdiags.metrics.steeringflows import SteeringFlows
# from tcdiags.metrics.tropcycmpi import TropCycMPI
# from tcdiags.tc import FilterVortex
# from tcdiags.tc.wnmsi import WNMSI

from utils.decorator_interface import privatemethod

# from tcdiags.tc.wnmsi import WNMSI

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
        self.logger = Logger()
        self.yaml_file = self.options_obj.yaml_file

        # Define the available application options.
#        self.apps_dict = {"tcfilt": FilterVortex, "tcmpi": TropCycMPI,
#                          "tcsteering": SteeringFlows, "tcwnmsi": WNMSI}

    @privatemethod
    def config(self: dataclass) -> object:
        """ """

        yaml_obj = YAML().read_yaml(yaml_file=self.yaml_file,
                                    return_obj=True)

        tcdiags_obj = parser_interface.object_define()

        inputs_io = GFS(yaml_file=yaml_obj.inputs)
        tcdiags_obj.inputs = inputs_io.read_inputs()

        quit()

        if "tcvitals" in self.yaml_dict:
            tcdiags_obj.tcinfo = YAML().read_yaml(
                yaml_file=self.yaml_dict["tcvitals"], return_obj=True)

        print(tcdiags_obj.tcinfo)

    def run(self: dataclass) -> None:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Reads the input variables from the specified file(s).

        (2) Launches the respective, and supported, TC diagnostics
            applications.

        """

        self.config()
        quit()

        # Read the input variables; proceed accordingly.
        inputs_obj = parser_interface.object_define()
        inputs_obj.fields = self.tcdiags_io.read_inputs()

        tcinfo_dict = parser_interface.dict_key_value(
            dict_in=self.yaml_dict, key="tcvitals", force=True)
        if tcinfo_dict is None:
            input_obj.tcinfo = None

        if tcinfo_dict is not None:
            inputs_obj.tcinfo = parser_interface.object_define()
            for tcinfo in tcinfo_dict:
                inputs_obj.tcinfo = parser_interface.object_setattr(
                    object_in=inputs_obj.tcinfo, key=tcinfo,
                    value=tcinfo_dict[tcinfo])

        # TODO: Clean this up; implement `import_lib` and build a
        # namespace for each application (e.g., `tcfilt`, `tcmpi`,
        # etc.,).

        quit()

        # Execute each of the specified applications.
        for app in self.apps_dict:

            # Check whether the application is to be executed; proceed
            # accordingly.
            opt_attr = parser_interface.object_getattr(
                object_in=self.options_obj, key=app, force=True
            )

            if opt_attr is not None:

                if parser_interface.str_to_bool(opt_attr):

                    # Define the respective application.
                    app_class = parser_interface.dict_key_value(
                        dict_in=self.apps_dict, key=app, no_split=True
                    )

                    # Collect the respective application configuration
                    # variables from the experiment configuration; if
                    # NoneType upon entry the respective application
                    # will define default values for the respective
                    # configuration variables.
                    yaml_app_dict = parser_interface.dict_key_value(
                        dict_in=self.yaml_dict, key=app, force=True
                    )

                    if yaml_app_dict is None:
                        msg = (
                            f"Configuration variable values for application {app} "
                            f"have not been defined in {self.yaml_file}; default values "
                            "will be used."
                        )
                        self.logger.warn(msg=msg)

                        yaml_app_dict = {}

                    try:
                        yaml_app_dict = parser_interface.dict_merge(dict1=yaml_app_dict,
                                                                    dict2=self.yaml_dict["tcvitals"]
                                                                    )
                    except KeyError:
                        msg = ("A YAML-formatted file containing the TC attributes could not be "
                               f"determined from the experiment configuration file {self.yaml_file} "
                               "and may cause some applications to fail."
                               )
                        self.logger.warn(msg=msg)

                    # Launch the respective application.
                    app_class(yaml_dict=yaml_app_dict,
                              inputs_obj=inputs_obj).run()

        # Clean up and deallocate memory accordingly.
        del inputs_obj
        collect()
