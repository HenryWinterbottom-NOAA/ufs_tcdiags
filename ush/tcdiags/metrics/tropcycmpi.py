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

from tcdiags.atmos import moisture, pressures

from exceptions import TropCycMPIError

from dataclasses import dataclass

import numpy

from metpy.units import units

from tcpyPI import pi

from tools import parser_interface

from utils.logger_interface import Logger

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


@dataclass
class TropCycMPI:
    """

    """

    def __init__(self, inputs_obj: object):
        """
        Description
        -----------

        Creates a new TropCycMPI object.

        """

        # Define the base-class attributes.
        self.logger = Logger()
        self.inputs_obj = inputs_obj
        self.tcmpi_obj = parser_interface.object_define()

    def compute_inputs(self) -> None:
        """ """

        # Append the geographical coordinate grids to the base-class
        # object; proceed accordingly.
        for coord in ["lat", "lon"]:

            value = parser_interface.object_getattr(
                object_in=self.inputs_obj, key=coord, force=True)

            if value is None:
                msg = (f"The geographic coordinate variable {coord} cannot be "
                       "NoneType. Aborting!!!"
                       )
                raise TropCycMPIError(msg=msg)

            self.tcmpi_obj = parser_interface.object_setattr(
                object_in=self.tcmpi_obj, key=coord, value=value)

        # Append the variable arrays to the base-class object; proceed
        # accordingly.
        for var in ["pres", "psfc", "spfh", "temp", "zsfc"]:

            value = parser_interface.object_getattr(
                object_in=self.inputs_obj, key=var, force=True)

            if value is None:
                msg = f"The variable {var} cannot be NoneType. Aborting!!!"
                raise TropCycMPIError(msg=msg)

            self.tcmpi_obj = parser_interface.object_setattr(
                object_in=self.tcmpi_obj, key=var, value=value)

        # Compute the input variables.
        self.tcmpi_obj = moisture.spfh_to_mxrt(inputs_obj=self.tcmpi_obj)
        self.tcmpi_obj = pressures.pressure_to_sealevel(
            inputs_obj=self.tcmpi_obj)

        # Update variable array units.
        self.tcmpi_obj.mxrt = units.Quantity(self.tcmpi_obj.mxrt, "g / kg")
        self.tcmpi_obj.pres = units.Quantity(self.tcmpi_obj.pres, "hPa")
        self.tcmpi_obj.pslp = units.Quantity(self.tcmpi_obj.pslp, "hPa")
        self.tcmpi_obj.temp = units.Quantity(self.tcmpi_obj.temp, "celsius")

        # Initialize the output variables.
#        for (var, units) in {"mslp": "pascal", "pout": "pascal", "tout": "kelvin", "vmax": "m/s"}.items():

#            self.tcmpi_obj = parser_interface.

    def compute_tcmpi(self) -> None:
        """ """

        # Initialize/define the local variables.
        (nx, ny) = [self.tcmpi_obj.lat.shape[1], self.tcmpi_obj.lat.shape[0]]
        ndim = (nx*ny)

        sstc = numpy.array(self.tcmpi_obj.temp)[0, :, :].ravel()
        slp = numpy.array(self.tcmpi_obj.pslp).ravel()
        mxrt = numpy.reshape(numpy.array(self.tcmpi_obj.mxrt),
                             (self.tcmpi_obj.mxrt.shape[0], ndim))
        pres = numpy.reshape(numpy.array(self.tcmpi_obj.pres),
                             (self.tcmpi_obj.pres.shape[0], ndim))
        temp = numpy.reshape(numpy.array(self.tcmpi_obj.temp),
                             (self.tcmpi_obj.temp.shape[0], ndim))
        zsfc = numpy.array(self.tcmpi_obj.zsfc).ravel()

        # Initialize the local variables.
        (mslp, vmax, tout, pout) = [numpy.empty(ndim) for idx in range(4)]

        # Compute the tropical cyclone maximum potential intensity and
        # associated diagnostics; proceed accordingly.
        for idx in range(ndim):

            # Compute only for (near) ocean points.
            if zsfc[idx] <= 10.0:

                try:
                    (vmax[idx], mslp[idx], _, tout[idx], pout[idx]) = \
                        pi(SSTC=sstc[idx], MSL=slp[idx],
                           P=pres[:, idx], TC=temp[:, idx], R=mxrt[:, idx])

                except Exception as errmsg:
                    msg = (f"The TC maxmimum potential intensity computation failed at index "
                           f"{idx} with error {errmsg}. Aborting!!!"
                           )
                    raise TropCycMPIError(msg=msg)

        # Update the values accordingly.
        mslp = numpy.where(mslp > 2000.0, numpy.nan, mslp)*100.0
        pout = numpy.where(mslp == numpy.nan, numpy.nan, pout)*100.0
        tout = numpy.where(mslp == numpy.nan, numpy.nan, tout) + 273.15
        vmax = numpy.where(mslp == numpy.nan, numpy.nan, vmax)

        mslp = numpy.reshape(mslp, (ny, nx))
        pout = numpy.reshape(pout, (ny, nx))
        tout = numpy.reshape(tout, (ny, nx))
        vmax = numpy.reshape(vmax, (ny, nx))

    def run(self) -> None:
        """

        """

        # Define/compute the input variables.
        self.compute_inputs()

        # Compute the tropical cyclone maximaum potential intensity.
        self.compute_tcmpi()
