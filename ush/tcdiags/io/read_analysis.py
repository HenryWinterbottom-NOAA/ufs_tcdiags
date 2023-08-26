# =========================================================================

# Module: ush/tcdiags/io/read_analysis.py

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

    read_analysis.py

Description
-----------

    This module contains the base-class object for allnetCDF-formatted
    analysis file reading and diagnostic variable derivations and
    computations.

Classes
-------

    ReadAnalysis(yaml_dict)

        This is the base-class object for all netCDF-formatted file
        analysis variable reading, derivations and computations.

Requirements
------------

- ufs_pytils; https: // github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 08 March 2023

History
-------

    2023-03-08: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=consider-using-dict-items

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from importlib import import_module
from types import SimpleNamespace
from typing import Generic

from confs.yaml_interface import YAML
from tcdiags.exceptions import ReadAnalysisError
from tcdiags.io import vario
from tools import parser_interface
from utils import schema_interface
from utils.decorator_interface import privatemethod
from utils.logger_interface import Logger

# ----


class ReadAnalysis:
    """
    Description
    -----------

    This is the base-class object for all netCDF-formatted file and
    respective variable(s) reading.

    Parameters
    ----------

    yaml_dict: Dict

        A Python dictionary containing the input attributes as defined
        by the `inputs_yaml` attribute within the experiment
        configuration.

    Raises
    ------

    ReadAnalysisError:

        - raised if the attribute `inputs` can not be determined from
          the experiment configuration file.

    """

    def __init__(self: Generic, yaml_file: str):
        """
        Description
        -----------

        Creates a new ReadAnalysis object.

        """

        # Define the base-class attributes.
        self.logger = Logger(
            caller_name=f"{__name__}.{self.__class__.__name__}")
        self.variable_range_msg = "Variable %s range values: (%s, %s) %s."

        # Collect the variable attributes.
        try:
            self.inputs_obj = YAML().read_yaml(yaml_file=yaml_file, return_obj=True)
            self.varname_list = [
                item
                for item in vars(self.inputs_obj)
                if isinstance(
                    parser_interface.object_getattr(
                        object_in=self.inputs_obj, key=item
                    ),
                    dict,
                )
            ]
            if len(self.varname_list) <= 0:
                msg = (
                    "The following mandatory input variables could not be identified from "
                    f"the experiment configuration {yaml_file}. Aborting!!!"
                )
                raise ReadAnalysisError(msg=msg)
            self.cls_schema = schema_interface.build_schema(
                schema_def_dict=YAML().read_yaml(yaml_file=self.inputs_obj.schema)
            )

        except Exception as errmsg:
            msg = (
                f"Reading YAML-formatted file {yaml_file} failed with error "
                f"{errmsg}. Aborting!!!"
            )
            raise ReadAnalysisError(msg=msg) from errmsg

    @privatemethod
    def build_varobj(self: Generic, varname: str) -> SimpleNamespace:
        """
        Description
        -----------

        This method defines a Python SimpleNamespace object to contain
        the attributes for the respective netCDF-formatted variable.

        Parameters
        ----------

        varname: str

            A Python string specifying the variable name.

        Returns
        -------

        varobj: SimpleNamespace

            A Python SimpleNamespace object containing the initialized
            netCDF-formatted variable container.

        Raises
        ------

        ReadAnalysisError:

            - raised if an exception is encountered while building the
              container SimpleNamespace object for the specified
              variable `varname`.

        """

        # Build the netCDF-formatted variable container object; proceed
        # accordingly.
        try:
            vardict = parser_interface.object_getattr(
                object_in=self.inputs_obj, key=varname, force=True
            )
            varobj = parser_interface.dict_toobject(
                in_dict=schema_interface.validate_schema(
                    cls_schema=self.cls_schema, cls_opts=vardict, write_table=True
                )
            )
        except Exception as errmsg:
            msg = (
                f"Defining the variable container object for variable {varname} "
                f"failed with error {errmsg}. Aborting!!!"
            )
            raise ReadAnalysisError(msg=msg) from errmsg

        return varobj

    def compute_derived(self: Generic, inputs_obj: SimpleNamespace) -> SimpleNamespace:
        """
        Description
        -----------

        This method computes/derives the specified variables from the
        respective analysis variables.

        Parameters
        ----------

        inputs_obj: SimpleNamespace

            A Python SimpleNamespace object containing the input
            analysis variables.

        Returns
        -------

        inputs_obj: SimpleNamespace

            A Python SimpleNamespace updated to contain the
            computed/derived analysis variables.

        """

        # Check that the grid-projection geographical location
        # variables are 2-dimensional; proceed accordingly.
        (
            inputs_obj.latitude.values,
            inputs_obj.longitude.values,
        ) = vario.update_grid(
            xlat_in=inputs_obj.latitude.values,
            xlon_in=inputs_obj.longitude.values,
        )

        # Compute the specified analysis variables.
        for varname in self.varname_list:
            varobj = parser_interface.object_getattr(
                object_in=inputs_obj, key=varname)
            if varobj.derived:
                method_app = parser_interface.object_getattr(
                    import_module(varobj.module), key=f"{varobj.method}", force=False
                )
                varobj.values = method_app(varobj=inputs_obj)
                varobj.values = vario.define_units(
                    varin=varobj.values, varunits=varobj.units
                )
                inputs_obj = parser_interface.object_setattr(
                    object_in=inputs_obj, key=varname, value=varobj
                )

        return inputs_obj

    def read(self: Generic) -> SimpleNamespace:
        """
        Description
        -----------

        This method collects the mandatory variables from the
        experiment configuration specified YAML-formatted file
        containing the input variable attributes.

        Returns
        -------

        inputs_obj: SimpleNamespace

            A Python SimpleNamespace object containing the mandatory
            input variables.

        """

        # Check that all required variables are defined; proceed
        # accordingly.
        inputs_obj = parser_interface.object_define()
        for varname in self.varname_list:
            # Collect the respective variable and scale as necessary.
            varobj = self.build_varobj(varname=varname)
            if varobj.ncfile is not None:
                varobj = vario.read_ncvar(varname=varname, varobj=varobj)
                varobj.values = vario.update_varattrs(
                    varin=varobj.values,
                    flip_lat=varobj.flip_lat,
                    flip_z=varobj.flip_z,
                    scale_mult=varobj.scale_mult,
                    scale_add=varobj.scale_add,
                )
                varobj.values = vario.define_units(
                    varin=varobj.values, varunits=varobj.units
                )
            inputs_obj = parser_interface.object_setattr(
                object_in=inputs_obj, key=varname, value=varobj
            )
        inputs_obj = self.compute_derived(inputs_obj=inputs_obj)

        return inputs_obj
