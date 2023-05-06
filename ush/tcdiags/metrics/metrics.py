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

    tcdiags_obj: object

        A Python object containing all configuration attributes for
        the respective application including inputs (i.e., `inputs`
        and `tcinfo`) as well as the remaining (supported)
        applications (see base-class attribute `apps_list`).

    """

    def __init__(self: dataclass, tcdiags_obj: object):
        """
        Description
        -----------

        Creates a new Metrics object.

        """

        # Define the base-class attributes.
        self.logger = Logger(caller_name=f"{__name__}.{self.__class__.__name__}")
        self.tcdiags_obj = tcdiags_obj
