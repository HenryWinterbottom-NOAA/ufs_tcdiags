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

# import cartopy.crs as ccrs

# from metpy.interpolate import interpolate_to_grid, remove_nan_observations
# from metpy.calc import smooth_n_point, smooth_gaussian

# from tcdiags.analysis.fft import forward_fft2d, inverse_fft2d

from scipy import linalg

from tcdiags.atmos.pressures import pressure_to_sealevel

from scipy import interpolate

# from global_land_mask import globe

from typing import Dict
import numpy

from dataclasses import dataclass

from exceptions import TropCycSteeringFlowsError

from tcdiags.geomets import radial_distance
from tcdiags.interp import radial
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

    def radial_interp(self, interp_obj: object) -> object:
        """

        """

    def run(self):
        """ """

        # Compute the radial distance.
        loc = (13.4, -72.0)  # 14L
        # loc = (16.1, 135.3)  # 21W
        latgrid = numpy.array(self.inputs_obj.lat).ravel()
        longrid = numpy.roll(numpy.array(
            (self.inputs_obj.lon) + (360.0 - 180.0)), 180, axis=1).ravel()

        self.tcsteer_obj.raddist = numpy.reshape(radial_distance(
            refloc=loc, latgrid=latgrid, longrid=longrid), numpy.shape(self.inputs_obj.lat))

        # self.inputs_obj = pressure_to_sealevel(inputs_obj=self.inputs_obj)

        # ocean_grid = globe.is_ocean(
        #    latgrid, longrid).reshape(numpy.shape(self.inputs_obj.lat))

        # land_grid = globe.is_land(
        #    latgrid, longrid).reshape(numpy.shape(self.inputs_obj.lat))

        variable = numpy.array(self.inputs_obj.uwnd[0, :, :])

        # quit()

        distance = 2000.0*1000.0

        interp_obj = parser_interface.object_define()
        interp_obj.vararray = variable
        interp_obj.distance = distance
        interp_obj.ddist = 25.0*1000.0
        interp_obj.raddist = numpy.array(self.tcsteer_obj.raddist)

        outvar = radial.interp(interp_obj)

        import matplotlib.pyplot as plt
        levels = numpy.linspace(
            variable.min(), variable.max(), 255)

        # plt.contourf(test, levels=levels, cmap="jet")
        # plt.savefig("mask.png")

        plt.contourf(outvar, levels=levels, cmap="jet")
        plt.savefig("steering_test.png")

        # test = numpy.where(
        #    (numpy.array(self.tcsteer_obj.raddist) <= distance) & (numpy.array(self.tcsteer_obj.raddist) > 1.1*distance), numpy.nan, variable)

        # test = numpy.where(
        #    (numpy.array(self.tcsteer_obj.raddist) > 1.1*distance), numpy.nan, test)

        # variable = numpy.where((numpy.array(self.tcsteer_obj.raddist) > 2.0*distance),
        #                       numpy.nan, test)

        # START: WORKING

        test = numpy.where(
            (numpy.array(self.tcsteer_obj.raddist) <= distance), numpy.nan, variable)  # | (numpy.array(self.tcsteer_obj.raddist) >= 1.25*distance) | land_grid, numpy.nan, variable)

        array = numpy.ma.masked_invalid(test)
        x = self.inputs_obj.lon
        y = self.inputs_obj.lat
        x1 = x[~array.mask]
        y1 = y[~array.mask]
        invar = test[~array.mask]

        interp = interpolate.griddata(
            (x1, y1), invar, (x, y), method="linear")

        plt.contourf(interp, levels=levels, cmap="jet")
        plt.savefig("old.png")

        plt.contourf((interp-outvar), levels=levels, cmap="jet")
        plt.savefig("diff.png")

        # valid = numpy.ma.masked_invalid(interp)
        # interp[valid.mask] = variable[valid.mask]

        # END: WORKING

        # CAN MAYBE DO ANOTHER PASS HERE.

        # interp = smooth_gaussian(interp, 9)  # , 10)

        # interp[valid.mask] = variable[valid.mask]

        # interp = numpy.where(
        #    (numpy.array(self.tcsteer_obj.raddist) >= 1.5*distance) | land_grid, variable, interp)
        # valid = numpy.ma.masked_invalid(interp)
        # interp = variable[valid.mask]

        # interp = smooth_n_point(interp, 9, 1)

        # test = numpy.where(
        #    ((numpy.array(self.tcsteer_obj.raddist) <= distance)), numpy.nan, variable)

        # test = numpy.where(
        #    ((numpy.array(self.tcsteer_obj.raddist) > 1.5*distance)), numpy.nan, test)

        # to_proj = ccrs.AlbersEqualArea(
        #    central_longitude=135.3, central_latitude=16.1)
        # lon = self.inputs_obj.lon
        # lat = self.inputs_obj.lat
        # variable = test.T

        # (xp, yp, _) = to_proj.transform_points(ccrs.Geodetic(), lon, lat).T

        # (xm, ym, invar) = remove_nan_observations(xp, yp, variable)

        # (x, y, outvar) = interpolate_to_grid(xm, ym, invar, interp_type="cressman",
        #                                     minimum_neighbors=1,
        #                                     search_radius=400000, hres=100000)

        # print(outvar)

        # array = numpy.ma.masked_invalid(test)

        # x1 = x[~array.mask]
        # y1 = y[~array.mask]
        # newarr = array[~array.mask]

        # xp = x[array.mask]
        # yp = y[array.mask]

        # (xx, yy, value) = interpolate_to_grid(
        #    x1, y1, newarr, interp_type="cressman", minimum_neighbors=1,
        #    search_radius=400000, hres=100000)

        # print(xx, yy, value)

        # interp = interpolate.griddata((x1, y1), newarr.ravel(),
        #                              (x, y), method="cubic")

        import matplotlib.pyplot as plt
        levels = numpy.linspace(
            variable.min(), variable.max(), 255)

        # plt.contourf(test, levels=levels, cmap="jet")
        # plt.savefig("mask.png")

        plt.contourf(variable, levels=levels, cmap="jet")
        plt.savefig("full.png")

        plt.contourf((variable - outvar), levels=levels, cmap="jet")
        plt.savefig("diff-full.png")

        # plt.clf()
        # plt.contourf(variable, levels=levels, cmap="jet")
        # plt.savefig("orig.png")

        # plt.clf()
        # plt.contourf(test, levels=levels, cmap="jet")
        # plt.savefig("mask.png")

        # plt.clf()
        # plt.contourf(interp-variable)
        # plt.savefig("diff.png")
