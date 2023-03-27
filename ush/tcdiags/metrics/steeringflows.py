# =========================================================================

# Module: ush/tcdiags/metrics/steeringflows.py

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

from tcdiags.interp import barnes

from tcdiags.atmos.pressures import pressure_to_sealevel

from scipy import interpolate

from global_land_mask import globe

from typing import Dict
import numpy

from dataclasses import dataclass

from exceptions import TropCycSteeringFlowsError

from tcdiags.geomets import radial_distance
from tools import parser_interface

from utils.logger_interface import Logger

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


@dataclass
class SteeringFlows:
    """

    """

    def __init__(self, yaml_dict: Dict, inputs_obj: object):
        """
        Description
        -----------

        Creates a new SteeringFlows object.

        """

        # Define the base-class attributes.
        self.logger = Logger()
        self.inputs_obj = inputs_obj
        self.yaml_dict = yaml_dict
        self.tcsteer_obj = parser_interface.object_define()

    def run(self):
        """ """

        # Compute the radial distance.
        loc = (13.4, -72.0)
        latgrid = numpy.array(self.inputs_obj.lat).ravel()
        longrid = numpy.roll(numpy.array(
            (self.inputs_obj.lon) + (360.0 - 180.0)), 180, axis=1).ravel()  # NEEDED

        print(longrid.min(), longrid.max())
        print(longrid.shape, latgrid.shape)

        self.tcsteer_obj.raddist = numpy.reshape(radial_distance(
            refloc=loc, latgrid=latgrid, longrid=longrid), numpy.shape(self.inputs_obj.lat))

        self.inputs_obj = pressure_to_sealevel(inputs_obj=self.inputs_obj)

        ocean_grid = globe.is_ocean(
            latgrid, longrid).reshape(numpy.shape(self.inputs_obj.lat))

        land_grid = globe.is_land(
            latgrid, longrid).reshape(numpy.shape(self.inputs_obj.lat))

        variable = self.inputs_obj.uwnd[0, :, :]

        distance = 2000.0*1000.0

        test = numpy.where(
            (numpy.array(self.tcsteer_obj.raddist) <= distance) & ocean_grid, numpy.nan, variable)

        outside = numpy.where((numpy.array(
            self.tcsteer_obj.raddist) > distance) & land_grid, variable, test)

        test = outside
        # test = numpy.where(ocean_grid, self.inputs_obj.pslp, test)

        # test = numpy.where((numpy.array(self.tcsteer_obj.raddist) <= 1200.0*1000.0),
        #                   numpy.nan,
        #                   self.inputs_obj.psfc)

        # newtest = numpy.where((test == numpy.nan) & (numpy.array(self.inputs_obj.zsfc) > 10.0), numpy.nan,
        #                      test)

        # test = newtest

        # array = numpy.ma.masked_invalid(test)

        # print(numpy.shape(array))
        # quit()

        # test = numpy.where((numpy.array(self.inputs_obj.zsfc) > 10.0) & (numpy.array(self.tcsteer_obj.raddist) <= 1200.0*1000.0), numpy.nan,
        #                   self.inputs_obj.pslp)

        # test = numpy.where(numpy.array(self.inputs_obj.zsfc)
        #                   >= 10.0 and numpy.array(self.tcsteer_obj.raddist < 1600.0), numpy.nan, test)

        x = self.inputs_obj.lon
        y = self.inputs_obj.lat
        array = numpy.ma.masked_invalid(test)
        x1 = x[~array.mask]
        y1 = y[~array.mask]

        # print(len(x1))
        # print(len(x))
        # quit()

        newarr = array[~array.mask]

        interp = interpolate.griddata((x1, y1), newarr.ravel(),
                                      (x, y), method="cubic")
        # interp = numpy.where(land_grid, numpy.array(
        #    self.inputs_obj.psfc), interp)

        import matplotlib.pyplot as plt
        levels = numpy.linspace(
            variable.min(), variable.max(), 255)
        plt.contourf(interp, levels=levels, cmap="jet")
        plt.savefig("steering_test.png")

        plt.clf()
        plt.contourf(variable, levels=levels, cmap="jet")
        plt.savefig("orig.png")

        plt.clf()
        plt.contourf(test, levels=levels, cmap="jet")
        plt.savefig("mask.png")

        plt.clf()
        plt.contourf(interp-numpy.array(variable))
        plt.savefig("diff.png")

        plt.clf()
        plt.contourf(land_grid)
        plt.savefig("land.png")