# =========================================================================

# Module: ush/tcdiags/io/gfs.py

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

    gfs.py

Description
-----------

    This module contains the base-class object for all Global Forecast
    System (GFS) netCDF-formatted file and reading and diagnostic
    variable derivations and computations.

Classes
-------

    GFS(yaml_dict)

        This is the base-class object for all GFS netCDF-formatted
        file reading and variable derivations and computations.

Requirements
------------

- metpy; https://unidata.github.io/MetPy/latest/index.html

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 08 March 2023

History
-------

    2023-03-08: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=consider-using-dict-items
# pylint: disable=line-too-long

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from dataclasses import dataclass
from typing import Dict

import numpy
from tcdiags.exceptions import GFSError
from ioapps import netcdf4_interface
from metpy.units import units

from tools import parser_interface
from utils.logger_interface import Logger

from tcdiags.derived import derived
from tcdiags.io import vario

from confs.yaml_interface import YAML

from utils.decorator_interface import privatemethod

# ----


@dataclass
class GFS:
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

    GFSError:

        - raised if the attribute `inputs` can not be determined from
          the experiment configuration file.

    """

    # Check that the input file contains all of the mandatory
    # variables.
    INPUTS_DICT = {
        "latitude": {"name": "lat", "units": "degree"},
        "longitude": {"name": "lon", "units": "degree"},
        "pressure": {"name": "pres", "units": "pascals"},
        "specific_humidity": {"name": "spfh", "units": "kg/kg"},
        "surface_height": {"name": "zsfc", "units": "gpm"},
        "surface_pressure": {"name": "psfc", "units": "Pa"},
        "temperature": {"name": "temp", "units": "K"},
        "uwind": {"name": "uwnd", "units": "mps"},
        "vwind": {"name": "vwnd", "units": "mps"},
    }

    # Global variable range string.
    VARRANGE_STRING = "Variable %s range values: (%s, %s) %s."

    def __init__(self: dataclass, yaml_file: str):
        """
        Description
        -----------

        Creates a new TCDiagsInputsNetCDFIO object.

        """

        # Define the base-class attributes.
        self.logger = Logger()

        try:
            self.inputs_dict = YAML().read_yaml(yaml_file=yaml_file)
        except Exception as errmsg:
            msg = (f"Reading YAML-formatted file {yaml_file} failed with error "
                   f"{errmsg}. Aborting!!!"
                   )
            raise GFSError(msg=msg) from errmsg

        self.variable_range_msg = self.VARRANGE_STRING

        self.inputs_obj = parser_interface.object_define()

    @privatemethod
    def build_varobj(self: dataclass, varname: str) -> object:
        """ 
        # TODO



        """

        varobj = parser_interface.object_define()

        vardict = parser_interface.dict_key_value(
            dict_in=self.inputs_dict, key=varname, force=True,
            no_split=True
        )

        varobj = vario.init_ncvar(varname=varname, vardict=vardict)

        return varobj

    @privatemethod
    def get_pressure(self: dataclass) -> None:
        """
        Description
        -----------

        This method computes the pressure profile in accordance with
        the experiment configuration attributes.

        Parameters
        ----------

        inputs_obj: object

            A Python object containing the mandatory input variables;
            this includes, at minimum, the pressure and surface
            pressure values; see below for additional information.

        Returns
        -------

        inputs_obj: object

            A Python object updated to contain the pressure profile
            array in accordance with the method defined in the
            experiment configuration.

        Raises
        ------

        GFSError:

            - raised if the pressure variable attributes cannot be
              determined from the experiment configuration or are not
              defined within this module (see base-class attribute
              `PRES_PROF_COMP_METHODS_DICT` above).

        Notes
        -----

        For the respective pressure profile computations, the
        respective methods assume the pressure array upon entry
        contains the following:

        1: pressure_from_thickness :: pres = the layer thickness; this
           is used to derive the pressure profile by integrating from
           the top layer thickness to the surface.

        """

        # Define the method to be used for the pressure profile and
        # compute the pressure profile accordingly.
        try:
            app = parser_interface.dict_key_value(
                dict_in=self.PRES_PROF_COMP_METHODS_DICT,
                key=self.inputs_obj.pressure.method, force=True
            )
        except Exception as errmsg:
            msg = ("Detemining the pressure profile computation methodology failed "
                   f"with error {errmsg}. Aborting!!!"
                   )
            raise GFSError(msg=msg)

        self.inputs_obj = app(inputs_obj=self.inputs_obj)
        msg = self.variable_range_msg % (
            "pressure",
            (self.inputs_obj.pressure.values).min(),
            (self.inputs_obj.pressure.values).max(),
            self.inputs_obj.pressure.units
        )
        self.logger.info(msg=msg)

    def read_inputs(self: dataclass) -> object:
        """
        Description
        -----------

        This method collects the mandatory variables from the
        experiment configuration specified YAML-formatted file
        containing the input variable attributes.

        Returns
        -------

        inputs_obj: object

            A Python object containing the mandatory input variables.

        Raises
        ------

        GFSError:

            - raised if a mandatory input variable has not been
              specified in the YAML-formatted file containing the
              input variable attributes.

            - raised if a required input variable attribute is
              NoneType after parsing the YAML-formatted file
              containing the input variable attributes.

        """

        # Check that all required variables are defined; proceed
        # accordingly.
        mand_inputs = set(list(sorted(self.INPUTS_DICT.keys())))
        yaml_inputs = set(list(sorted(self.inputs_dict.keys())))
        missing_vars = list(sorted(mand_inputs - yaml_inputs))

        if len(missing_vars) > 0:
            msg = (
                "The following mandatory input variables could not be found in the "
                f"experiment configuration: {missing_vars}. Aborting!!!"
            )
            raise GFSError(msg=msg)

        for varname in self.INPUTS_DICT:

            vardict = parser_interface.dict_key_value(
                dict_in=self.inputs_dict, key=varname, force=True,
                no_split=True
            )

            # Collect the respective variable and scale as necessary.
            varobj = self.build_varobj(varname=varname)
            varobj = vario.read_ncvar(varname=varname, varobj=varobj)
            varobj.values = \
                vario.update_varattrs(varin=varobj.values,
                                      flip_lat=varobj.flip_lat, flip_z=varobj.flip_z,
                                      scale_mult=varobj.scale_mult, scale_add=varobj.scale_add
                                      )

            units = parser_interface.dict_key_value(
                dict_in=self.INPUTS_DICT[varname], key="units", no_split=True)
            varobj.values = vario.define_units(varin=varobj.values,
                                               varunits=units)

            msg = self.variable_range_msg % (
                varname,
                numpy.array(varobj.values.min()),
                numpy.array(varobj.values.max()),
                varobj.values.units,
            )
            self.logger.info(msg=msg)

            self.inputs_obj = parser_interface.object_setattr(
                object_in=self.inputs_obj, key=varname, value=varobj)

        # Check that the grid-projection geographical location
        # variables are 2-dimensional; proceed accordingly.
        (self.inputs_obj.latitude.values, self.inputs_obj.longitude.values) = \
            vario.update_grid(xlat_in=self.inputs_obj.latitude.values,
                              xlon_in=self.inputs_obj.longitude.values
                              )

        # Compute/define the remaining diagnostic variables.
        self.inputs_obj.pressure.values = vario.define_units(
            varin=derived.compute_pressure(varobj=self.inputs_obj,
                                           method="pressure_from_thickness"),
            varunits="Pa")

        self.inputs_obj.heights = self.build_varobj(varname=varname)
        self.inputs_obj.heights.values = vario.define_units(
            varin=derived.compute_height(varobj=self.inputs_obj,
                                         method="height_from_pressure"),
            varunits="m")

        return self.inputs_obj
