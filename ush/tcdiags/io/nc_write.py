# =========================================================================

# Module: ush/tcdiags/io/nc_write.py

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

    nc_write.py

Description
-----------

    This module contains the base-class object for all
    netCDF-formatted output file writing.

Classes
-------

    NCWrite(output_file)

        This is the base-class object for all netCDF-formatted file
        writing.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

- xarray; https://github.com/pydata/xarray

Author(s)
---------

    Henry R. Winterbottom; 13 March 2023

History
-------

    2023-03-13: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=unused-argument

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Dict, List

import numpy
from tcdiags.exceptions import IoNcWriteError
from tools import parser_interface
from utils.logger_interface import Logger
from xarray import DataArray, merge

# ----


@dataclass
class NCWrite:
    """
    Description
    -----------

    This is the base-class object for all netCDF-formatted file
    writing.

    Parameters
    ----------

    output_file: str

        A Python string specifying the path to the netCDF-formatted
        file to be written.

    """

    def __init__(self: dataclass, output_file: str):
        """
        Description
        -----------

        Creates a new NCWrite object.

        """

        # Define the base-class attributes
        self.logger = Logger(
            caller_name=f"{__name__}.{self.__class__.__name__}")
        self.output_file = output_file

    def write(
        self: dataclass,
        var_obj: SimpleNamespace,
        var_list: List,
        coords_3d: Dict = None,
        coords_2d: Dict = None,
        unlimited_dims: str = None,
        attrs_list: List = None,
        global_attrs_dict: Dict = None,
    ) -> None:
        """
        Description
        -----------

        This method writes a netCDF-formatted output file using
        xarray.

        Parameters
        ----------

        var_obj: SimpleNamespace

            A Python SimpleNamespace object containing all variables
            to be written to the netCDF-formatteed output file path.

        var_list: List

            A Python list of variable names to be collected from the
            `var_obj` parameters specified upon entry.

        Keywords
        --------

        coords_2d: Dict, optional

            A Python object describing the coordinate dimensions for
            (any) 2-dimensional variables.

        coords_3d: Dict, optional

            A Python object describing the coordinate dimensions for
            (any) 3-dimensional variables.

        attrs_list: List, optional

            A Python list of attributes to be used for a respective
            variable metadata (if available).

        unlimited_dims: str, optional

            A Python string specifying the netCDF coordinate dimension
            variable which is to be set as unlimited.

        Raises
        ------

        IoNcWriteError:

            - raised if the coordinate dimensions cannot be determined
              for specified output variable.

        """

        # Build, define, and collect the variable objects from which
        # to build the netCDF-formatted output file.
        msg = f"Writing output file {self.output_file}."
        self.logger.info(msg=msg)

        dataout_list = []

        for var in var_list:
            # Define the output variable attributes; proceed
            # accordingly.
            varout = parser_interface.object_getattr(
                object_in=var_obj, key=var, force=True
            )
            if varout is None:
                msg = (
                    f"Variable {var} could not be determined from the input object "
                    "`var_obj` and will not be written to {self.output_file}."
                )
                self.logger.warn(msg=msg)

            # Collect (any) attributes for the respective variable.
            if varout is not None:
                try:
                    attributes = {
                        key: value
                        for (key, value) in varout.attrs.items()
                        if value is not None
                    }
                except AttributeError:
                    msg = (
                        f"No attributes have been defined for variable {var}; attributes "
                        f"for variable will not be written to {self.output_file}."
                    )
                    self.logger.warn(msg=msg)
                    attributes = {}

                # Build the data array for the respective variables
                # and setup the xarray object.
                data = numpy.array(varout.values)

                # Define the coordinate dimensions for the respective
                # variable.
                if data.ndim == 2:
                    coords = coords_2d
                elif data.ndim == 3:
                    coords = coords_3d
                else:
                    msg = (
                        f"The coordinates for variable {var} could not be determined. "
                        "Aborting!!!"
                    )
                    raise IoNcWriteError(msg=msg)
                dims = list(coords.keys())

                # Build the xarray object corresponding to the
                # respective variable.
                xarray_obj = DataArray(
                    name=var, data=data, dims=dims, coords=(coords)
                ).assign_attrs(attributes)

                dataout_list.append(xarray_obj.to_dataset(name=var))

        # Build and write the netCDF-formatted output file.
        dataset_output = merge(dataout_list)
        dataset_output.to_netcdf(self.output_file)
