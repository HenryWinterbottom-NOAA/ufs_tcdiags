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


"""

# ----

import numpy

from typing import Dict, List

from dataclasses import dataclass

from tools import parser_interface

from utils.logger_interface import Logger

import pint_xarray

from exceptions import TCDiagsIOError

from xarray import DataArray, merge, open_dataset

# ----


@dataclass
class TCDiagsOutputsIO:
    """


    """

    # , varobj_list: List, unlimitdim: str = None):
    def __init__(self, output_file: str):
        """
        Description
        -----------

        Creates a new TCDiagsOutputsIO object.

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

    def write(self, var_obj: object, var_list: List, coords_3d=None, coords_2d=None,
              unlimited_dims: str = None, attrs_list: List = None) -> None:
        """

        """

        dataout_list = []

        for var in var_list:

            varout = parser_interface.object_getattr(
                object_in=var_obj, key=var, force=True)

            if varout is None:

                msg = (f"Variable {var} could not be determined from the input object "
                       "`var_obj` and will not be written to {self.output_file}."
                       )
                self.logger.warn(msg=msg)

            if varout is not None:

                data = numpy.array(varout)

                if len(data.shape) == 2:
                    coords = coords_2d

                elif len(data.shape) == 3:
                    coords = coords_3d

                else:

                    msg = (f"The coordinates for variable {var} could not be determined. "
                           "Aborting!!!"
                           )
                    raise TCDiagsIOError(msg=msg)

                dims = list(coords.keys())

                xarray_obj = DataArray(
                    name=var, data=varout, dims=dims, coords=(coords))

                if attrs_list is not None:
                    varout_attrs_dict = {}

                    for attr in attrs_list:
                        value = parser_interface.object_getattr(
                            object_in=varout, key=attr, force=True)

                        if value is None:
                            msg = (f"Attribute {attr} could not be determine for variable "
                                   f"{var} and will not be written to output file {self.output_file}."
                                   )
                            self.logger.warn(msg=msg)

                        if value is not None:

                            varout_attrs_dict[attr] = list(
                                value._units.keys())

                    xarray_obj.attrs = varout_attrs_dict

                dataout_list.append(xarray_obj.to_dataset(name=var))

        dataset_output = merge(dataout_list)
        dataset_output.to_netcdf(self.output_file)
