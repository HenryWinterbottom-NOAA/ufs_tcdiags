# =========================================================================

# Module: ush/tcdiags/io/outputs.py

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

    outputs.py

Description
-----------

    This module contains the base-class object for all output file
    writing.

Classes
-------

    TCDiagsOutputsCetCDFIO(output_file)

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

# pylint: disable=protected-access
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=unused-argument

# ----

from dataclasses import dataclass
from typing import Dict, List

import numpy
from exceptions import TCDiagsIOError
from tools import parser_interface
from utils.logger_interface import Logger
from xarray import DataArray, merge

# ----


@dataclass
class TCDiagsOutputsNetCDFIO:
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

    def __init__(self, output_file: str):
        """
        Description
        -----------

        Creates a new TCDiagsOutputsNetCDFIO object.

        """

        # Define the base-class attributes
        self.logger = Logger()
        self.output_file = output_file

    def build_varobj(self, ncvarname: str) -> object:
        """
        Description
        -----------

        This method defines a Python object to be used by the xarray
        library/package to define/update the respective netCDF output
        file/variables.

        Parameters
        ----------

        ncvarname: str

            A Python string specifying the netCDF variable name to be
            defined and/or written within the output netCDF file.

        Returns
        -------

        var_obj: object

            A Pyton object containing the netCDF variable attributes
            to be used by xarray library/package to define/update the
            respective netCDF output file/variables.

        """

        # Define the Python object containing the netCDF variable
        # attributes.
        var_obj = parser_interface.object_define()
        var_obj = parser_interface.object_setattr(
            object_in=var_obj, key="ncvarname", value=ncvarname
        )

    def write(
        self,
        var_obj: object,
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

        var_obj: object

            A Python object containing all variables to be written to
            the netCDF-formatteed output file path.

        var_list: list

            A Python list of variable names to be collected from the
            `var_obj` parameters specified upon entry.

        Keywords
        --------

        coords_2d: dict, optional

            A Python object describing the coordinate dimensions for
            (any) 2-dimensional variables.

        coords_3d: dict, optional

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

        TCDiagsIOError:

            * raised if the coordinate dimensions cannot be determined
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

            if varout is not None:
                # Build the data array for the respective variables
                # and setup the xarray object.
                data = numpy.array(varout)
                if len(data.shape) == 2:
                    coords = coords_2d

                elif len(data.shape) == 3:
                    coords = coords_3d

                else:
                    msg = (
                        f"The coordinates for variable {var} could not be determined. "
                        "Aborting!!!"
                    )
                    raise TCDiagsIOError(msg=msg)

                dims = list(coords.keys())

                xarray_obj = DataArray(
                    name=var, data=varout, dims=dims, coords=(coords)
                )

                # If applicable, define the netCDF-formatted
                # attributes for the respective variable.
                if attrs_list is not None:
                    varout_attrs_dict = {}

                    for attr in attrs_list:
                        value = parser_interface.object_getattr(
                            object_in=varout, key=attr, force=True
                        )

                        if value is None:
                            msg = (
                                f"Attribute {attr} could not be determined for variable "
                                f"{var} and will not be written to output file {self.output_file}."
                            )
                            self.logger.warn(msg=msg)

                        if value is not None:
                            varout_attrs_dict[attr] = list(value._units.keys())

                        xarray_obj.attrs = varout_attrs_dict

                # Update the xarray objects list.
                dataout_list.append(xarray_obj.to_dataset(name=var))

        # Build and write the netCDF-formatted output file.
        dataset_output = merge(dataout_list)

        # Write the global attributes (if applicable).
        if global_attrs_dict is not None:
            for global_attr in global_attrs_dict:
                dataset_output.attrs[global_attr] = parser_interface.dict_key_value(
                    dict_in=global_attrs_dict, key=global_attr, no_split=None
                )

        dataset_output.to_netcdf(self.output_file)
