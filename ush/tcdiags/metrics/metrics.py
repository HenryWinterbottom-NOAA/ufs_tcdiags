# =========================================================================

# Module: ush/tcdiags/metrics/metrics.py

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

    metrics.py

Description
-----------

    This module contains the base-class object Metrics.

Classes
-------

    Metrics(tcdiags_obj, app_obj)

        This is the base-class object for all Metrics sub-classes.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 03 May 2023

History
-------

    2023-05-03: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Dict, List

from confs.yaml_interface import YAML
from tcdiags.io.nc_write import NCWrite
from tools import parser_interface
from utils import schema_interface
from utils.logger_interface import Logger

# ----


@dataclass
class Metrics:
    """
    Description
    -----------

    This is the base-class object for all Metrics sub-classes.

    Parameters
    ----------

    tcdiags_obj: SimpleNamespace

        A Python SimpleNamespace object containing all configuration
        attributes including inputs (i.e., `inputs` and `tcinfo`) as
        well as the remaining (supported) applications (see base-class
        attribute `apps_list`).

    app_obj: SimpleNamespace

        A Python SimpleNamespace object containing the attributes for
        the respective sub-class application.

    """

    def __init__(
        self: dataclass, tcdiags_obj: SimpleNamespace, app_obj: SimpleNamespace
    ):
        """
        Description
        -----------

        Creates a new Metrics object.

        """

        # Define the base-class attributes.
        self.logger = Logger(caller_name=f"{__name__}.{self.__class__.__name__}")
        self.tcdiags_obj = tcdiags_obj

        cls_opts = parser_interface.object_todict(
            object_in=parser_interface.object_getattr(
                object_in=self.tcdiags_obj, key=app_obj
            )
        )
        self.options_obj = self.schema(
            cls_schema_file=parser_interface.object_getattr(
                object_in=self.tcdiags_obj, key=app_obj
            ).schema,
            cls_opts=cls_opts,
        )

    def schema(
        self: dataclass, cls_schema_file: str, cls_opts: Dict
    ) -> SimpleNamespace:
        """
        Description
        -----------

        This method evaluates the schema corresponding to the
        respective application.

        cls_schema_file: str

            A Python string specifying the file path for the
            YAML-formatted file containing the schema attributes for
            the respective application (base-class attribute
            `app_obj`).

        cls_opts: Dict

            A Python dictionary containing the configuration defined
            options for the respective application (base-class
            attribute `app_obj`).

        Returns
        -------

        options_obj: SimpleNamespace

            A Python SimpleNamespace containing the respective
            application configuration.

        """

        # Evaluate the schema and define the configuration for the
        # respective application.
        schema_def_dict = YAML().read_yaml(yaml_file=cls_schema_file)
        cls_schema = schema_interface.build_schema(schema_def_dict=schema_def_dict)
        options_obj = parser_interface.dict_toobject(
            in_dict=schema_interface.validate_schema(
                cls_schema=cls_schema, cls_opts=cls_opts, write_table=True
            )
        )

        return options_obj

    @staticmethod
    def write_output(
        output_file: str,
        var_obj: SimpleNamespace,
        var_list: List,
        coords_2d: Dict = None,
        coords_3d: Dict = None,
    ) -> None:
        """
        Description
        -----------

        This method writes the quantities within the calling class
        SimpleNamespace (`var_obj`) to the specified external
        netCDF-formatted file path.

        Parameters
        ----------

        output_file: str

            A Python string defining the path to the output
            netCDF-formatted file.

        var_obj: SimpleNamespace

            A Python SimpleNamespace object containing the quantities
            to be written to the output netCDF-formatted file.

        var_list: List

            A Python list of output variables.

        Keywords
        --------

        coords_2d: Dict, optional

            A Python dictionary containing the 2-dimensional
            coordinate and dimension attributes; this is assumes CF
            compliance.

        coords_3d: Dict, optional

            A Python dictionary containing the 3-dimensional
            coordinate and dimension attributes; this is assumes CF
            compliance.

        """

        # Write the netCDF-formatted output file acccordingly.
        ncwrite = NCWrite(output_file=output_file)
        ncwrite.write(
            var_obj=var_obj, var_list=var_list, coords_2d=coords_2d, coords_3d=coords_3d
        )
