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

    Metrics(tcdiags_obj)

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

from utils import schema_interface

from confs.yaml_interface import YAML

from utils.logger_interface import Logger

from typing import Dict

# ----


@dataclass
class Metrics:
    """
    Description
    -----------

    This is the base-class object for all Metrics sub-classes.

    Parameters
    ----------

    tcdiags_obj: object

        A Python object containing all configuration attributes for
        the respective application including inputs (i.e., `inputs`
        and `tcinfo`) as well as the remaining (supported)
        applications (see base-class attribute `apps_list`).

    """

    def __init__(self: dataclass, tcdiags_obj: SimpleNamespace):
        """
        Description
        -----------

        Creates a new Metrics object.

        """

        # Define the base-class attributes.
        self.logger = Logger(
            caller_name=f"{__name__}.{self.__class__.__name__}")
        self.tcdiags_obj = tcdiags_obj

    def schema(self: dataclass, cls_schema_file: str, cls_opts: Dict) -> None:
        """ """

        schema_def_dict = YAML().read_yaml(yaml_file=cls_schema_file)
        cls_schema = schema_interface.build_schema(
            schema_def_dict=schema_def_dict)
        options_obj = schema_interface.validate_schema(
            cls_schema=cls_schema, cls_opts=cls_opts, write_table=True)

        return options_obj
