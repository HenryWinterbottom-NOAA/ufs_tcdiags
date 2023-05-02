# =========================================================================

# Module: ush/tcdiags/io/tcinfo.py

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

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from dataclasses import dataclass

from confs.yaml_interface import YAML

from utils.logger_interface import Logger

# ----


@dataclass
class TCInfo:

    def __init__(self: dataclass, yaml_dict: Dict):
        """
        Description
        -----------

        Creates a new TCInfo class.

        """

        # Define the base-class attributes.
        self.logger = Logger()
        self.yaml_dict = yaml_dict

    def read(self: dataclass) -> object:
        """

        """
