# =========================================================================

# Module: ush/tcdiags/metrics/__init__.py

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

from collections import OrderedDict

from tcdiags.atmos import moisture, pressures

from exceptions import TropCycMPIError

from dataclasses import dataclass

import numpy

#import pint
#import pint_xarray

from metpy.units import units

from tcpyPI import pi

from tools import parser_interface

from utils.logger_interface import Logger

from typing import Dict

from tcdiags.io.outputs import TCDiagsOutputsIO

#from xarray import DataArray, merge, open_dataset

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


@dataclass
class TropCycMPI:
    """

    """

    def __init__(self, yaml_dict: Dict, inputs_obj: object):
        """
        Description
        -----------

        Creates a new TropCycMPI object.

        """

        # Define the base-class attributes.
        self.logger = Logger()
        self.inputs_obj = inputs_obj
        self.yaml_dict = yaml_dict

        self.tcmpi_obj = parser_interface.object_define()
        self.tcmpi_var_list = ["mslp", "pout", "tout", "vmax"]

        self.tcmpi_var_dict = {"mslp_max": 2000.0,
                               "zmax": 10.0,
                               "output_file": "tcmpi.nc"
                               }

        (self.nx, self.ny) = [
            self.inputs_obj.lat.shape[1], self.inputs_obj.lat.shape[0]]
        self.ndim = (self.nx*self.ny)

        self.nlevs = self.inputs_obj.temp.shape[0]

        # Initialize the local variables.
        (self.mslp, self.vmax, self.tout, self.pout) = [
            numpy.empty(self.ndim) for idx in range(4)]

        # Compute the input variables.
        self.compute_inputs()

        # Define the local variables.
        self.define_locals()

        # Define the configuration variables.
        self.init_config()

        # Build the dimensional and CF compliant dimensions.
        self.coords_2d = OrderedDict({"lat": (["lat"], numpy.array(self.inputs_obj.lat)[:, 0]),
                                      "lon": (["lon"], numpy.array(self.inputs_obj.lon)[0, :])
                                      })

        self.coords_3d = OrderedDict({"level": (["level"], numpy.arange(0, self.nlevs)),
                                      "lat": (["lat"], numpy.array(self.inputs_obj.lat)[:, 0]),
                                      "lon": (["lon"], numpy.array(self.inputs_obj.lon)[0, :])
                                      })

        # Define the output variables list.
        self.output_varlist = ["mslp", "mxrt", "pout",
                               "pres", "pslp", "temp", "tout", "vmax", "zsfc"]

    def define_locals(self) -> None:
        """
        Description
        -----------

        This method defines the input variables for the tropical
        cyclone maximum potential intensity calculations.

        """

        # Initialize the input variable arrays for the tropical
        # cyclone maximum potential intensity calculation.
        self.sstc = numpy.array(self.inputs_obj.temp)[0, :, :].ravel()
        self.slp = numpy.array(self.tcmpi_obj.pslp).ravel()
        self.mxrt = numpy.reshape(numpy.array(self.tcmpi_obj.mxrt),
                                  (self.tcmpi_obj.mxrt.shape[0], self.ndim))
        self.pres = numpy.reshape(numpy.array(self.tcmpi_obj.pres),
                                  (self.tcmpi_obj.pres.shape[0], self.ndim))
        self.temp = numpy.reshape(numpy.array(self.tcmpi_obj.temp),
                                  (self.tcmpi_obj.temp.shape[0], self.ndim))
        self.zsfc = numpy.array(self.inputs_obj.zsfc).ravel()

    def init_config(self) -> None:
        """
        Description
        -----------

        This method defines the base-class attribute values collected
        from the experiment configuration variables.

        """

        for tcmpi_var in self.tcmpi_var_dict:
            value = parser_interface.dict_key_value(
                dict_in=self.yaml_dict, key=tcmpi_var, force=True,
                no_split=True)

            if value is None:
                value = parser_interface.dict_key_value(
                    dict_in=self.tcmpi_var_dict, key=tcmpi_var, force=True,
                    no_split=None)

                if value is None:
                    msg = (f"The attribute variable {tcmpi_var} could not be determined. "
                           "Aborting!!!"
                           )
                    raise TCDiagsError(msg=msg)

                msg = (f"Setting configuration variable {tcmpi_var} to default value "
                       f"{value}."
                       )
                self.logger.warn(msg=msg)

            self = parser_interface.object_setattr(
                object_in=self, key=tcmpi_var, value=value)

    def compute_inputs(self) -> None:
        """ """

        # Compute the input variables.
        self.tcmpi_obj = moisture.spfh_to_mxrt(inputs_obj=self.inputs_obj)
        self.tcmpi_obj = pressures.pressure_to_sealevel(
            inputs_obj=self.inputs_obj)

        # Update the input variable units accordingly.
        self.tcmpi_obj.pslp = units.Quantity(
            self.inputs_obj.pslp, "hectopascal")
        self.tcmpi_obj.pres = units.Quantity(
            self.inputs_obj.pres, "hectopascal")
        self.tcmpi_obj.temp = units.Quantity(self.inputs_obj.temp, "celsius")

    def compute_tcmpi(self) -> None:
        """ """

        # Compute the tropical cyclone maximum potential intensity
        # attributes.
        #[self.tcpi(idx=idx) for idx in range(self.ndim)]

        self.mslp = units.Quantity(self.mslp, "hectopascal")
        self.pout = units.Quantity(self.pout, "hectopascal")
        self.tout = units.Quantity(self.tout, "celsius")
        self.vmax = units.Quantity(self.vmax, "mps")

        # Define the base-class attribute values.
        self.tcmpi_obj = parser_interface.object_setattr(
            object_in=self.tcmpi_obj, key="mslp", value=self.mslp)
        self.tcmpi_obj.mslp = numpy.reshape(
            self.tcmpi_obj.mslp, (self.ny, self.nx))
        self.tcmpi_obj.mslp = units.Quantity(self.tcmpi_obj.mslp, "pascal")

        self.tcmpi_obj = parser_interface.object_setattr(
            object_in=self.tcmpi_obj, key="pout", value=self.pout)
        self.tcmpi_obj.pout = numpy.reshape(
            self.tcmpi_obj.pout, (self.ny, self.nx))
        self.tcmpi_obj.pout = units.Quantity(self.tcmpi_obj.pout, "pascal")

        self.tcmpi_obj = parser_interface.object_setattr(
            object_in=self.tcmpi_obj, key="tout", value=self.tout)
        self.tcmpi_obj.tout = numpy.reshape(
            self.tcmpi_obj.tout, (self.ny, self.nx))
        self.tcmpi_obj.tout = units.Quantity(self.tcmpi_obj.tout, "kelvin")

        self.tcmpi_obj = parser_interface.object_setattr(
            object_in=self.tcmpi_obj, key="vmax", value=self.vmax)
        self.tcmpi_obj.vmax = numpy.reshape(
            self.tcmpi_obj.vmax, (self.ny, self.nx))

        # Correct the units for output.
        self.tcmpi_obj.pres = units.Quantity(self.tcmpi_obj.pres, "pascal")
        self.tcmpi_obj.temp = units.Quantity(self.tcmpi_obj.temp, "kelvin")

    def tcpi(self, idx: int) -> None:
        """ """

        if self.zsfc[idx] <= self.zmax:

            (self.vmax[idx], self.mslp[idx], _, self.tout[idx], self.pout[idx]) = \
                pi(SSTC=self.sstc[idx], MSL=self.slp[idx], P=self.pres[:, idx],
                   TC=self.temp[:, idx], R=self.mxrt[:, idx])

        else:

            (self.vmax[idx], self.mslp[idx], self.tout[idx],
             self.pout[idx]) = [numpy.nan for count in range(4)]

    def write_output(self):
        """ """

        tcdiags_out = TCDiagsOutputsIO(output_file=self.output_file)

        tcdiags_out.write(var_obj=self.tcmpi_obj, var_list=self.output_varlist,
                          coords_3d=self.coords_3d, coords_2d=self.coords_2d,
                          attrs_list=["units"])

    def run(self) -> None:
        """

        """

        # Compute the tropical cyclone maximum potential intensity.
        self.compute_tcmpi()

        self.write_output()
