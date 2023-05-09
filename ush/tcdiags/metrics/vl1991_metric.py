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
Module
------

    vl1991_metric.py

Description
-----------

    This module contains the base-class object for tropical cyclone
    (TC) steering flow evalutions as described in Velden and Leslie
    [1991].

Classes
-------

    VL1991(tcdiags_obj)

        This is the base-class object for all tropical cyclone (TC)
        steering flow evaluations presented in Velden and Leslie
        [1991]; it is a sub-class of Metrics.

References
----------

    Velden, C. S. and L. M. Leslie. "The Basic Relationship between
    Tropical Cyclone Intensity and the Depth of the Environmental
    Steering Layer in the Australian Region". Weather and Forecasting
    6 (1991): 244-253.

    DOI: https://doi.org/10.1175/1520-0434(1991)006<0244:TBRBTC>2.0.CO;2

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 05 May 2023

History
-------

    2023-05-03: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import ast
from typing import Tuple

import numpy
from tcdiags import interp
from tcdiags.derived.atmos import winds
from tcdiags.geomets import radial_distance
from tcdiags.interp import radial, vertical
from tcdiags.io.nc_write import NCWrite
from tcdiags.metrics.metrics import Metrics
from tools import parser_interface
from utils.decorator_interface import privatemethod
from xarray import DataArray

# ----


class VL1991(Metrics):
    """
    Description
    -----------

    This is the base-class object for all tropical cyclone (TC)
    steering flow evaluations presented in Velden and Leslie [1991];
    it is a sub-class of Metrics.

    Parameters
    ----------

    tcdiags_obj: object

        A Python object containing all configuration attributes for
        the respective application including inputs (i.e., `inputs`
        and `tcinfo`) as well as the remaining (supported)
        applications (see base-class attribute `apps_list`).

    References
    ----------

    Velden, C. S. and L. M. Leslie. "The Basic Relationship between
    Tropical Cyclone Intensity and the Depth of the Environmental
    Steering Layer in the Australian Region". Weather and Forecasting
    6 (1991): 244-253.

    DOI: https://doi.org/10.1175/1520-0434(1991)006<0244:TBRBTC>2.0.CO;2

    """

    def __init__(self: Metrics, tcdiags_obj: object):
        """
        Description
        -----------

        Creates a new VL1991 object.

        """

        # TODO: Add schema interface to evaluate input values and/or
        # set defaults.

        # Define the base-class attributes.
        super().__init__(tcdiags_obj=tcdiags_obj)

        self.rdlintrp_obj = parser_interface.object_define()
        self.tcstrflw_obj = parser_interface.object_define()

        self.latgrid = numpy.array(
            self.tcdiags_obj.inputs.latitude.values).ravel()
        self.longrid = numpy.array(
            self.tcdiags_obj.inputs.longitude.values).ravel()

        self.plevs = numpy.array(
            [
                ast.literal_eval(plev)
                for plev in self.tcdiags_obj.tcsteering.isolevels.split()
            ]
        )[:, 0]

        self.tcstrflw_obj.dims = {
            "plevs": (["plevs"], self.plevs),
            "lat": (["lat"], self.tcdiags_obj.inputs.latitude.values[:, 0]),
            "lon": (
                ["lon"],
                self.tcdiags_obj.inputs.longitude.values[0, :]
                - self.tcdiags_obj.inputs.longitude.scale_add,
            ),
        }

        self.output_varlist = [
            "chi",
            "divg",
            "psi",
            "udiv",
            "uhrm",
            "uvor",
            "uwnd",
            "vort",
            "vdiv",
            "vhrm",
            "vvor",
            "vwnd",
        ]

    @privatemethod
    def compute_diags(self: Metrics, vararr: DataArray) -> None:
        """
        Description
        -----------

        This method computes the diagnostic wind components; the
        following quantities are diagnosed on the respective isobaric
        levels define by attribute `plevs`.

        - Divergence (`divg`)

        - Divergent wind components (`udiv`, `vdiv`)

        - Harmonic (e.g., residual) wind components (`uhrm`, `vhrm`)

        - Rotational wind components (`urot`, `vrot`)

        - Streamfunction (`psi`)

        - Vorticity (`vort`)

        - Velocity potential (`chi`)

        Parameters
        ----------

        vararr: DataArray

            A Python array-type variable used to initialize the
            DataArray containers for the respective variables.

        """

        # Compute the diagnostic wind components.
        (chi, divg, psi, udiv, uhrm, uvor, vdiv, vhrm, vvor, vort) = [
            vararr for idx in range(10)
        ]

        self.tcstrflw_obj.divg = divg.assign_attrs(
            {"units": "1/second", "name": "divergence"}
        )
        self.tcstrflw_obj.divg.values = winds.global_divg(
            varobj=self.tcstrflw_obj)

        self.tcstrflw_obj.vort = vort.assign_attrs(
            {"units": "1/second", "name": "vorticity"}
        )
        self.tcstrflw_obj.vort.values = winds.global_vort(
            varobj=self.tcstrflw_obj)

        self.tcstrflw_obj.chi = chi.assign_attrs(
            {"units": "meters^2/second", "name": "velocity potential"}
        )
        self.tcstrflw_obj.psi = psi.assign_attrs(
            {"units": "meters^2/second", "name": "streamfunction"}
        )
        (
            self.tcstrflw_obj.chi.values,
            self.tcstrflw_obj.psi.values,
        ) = winds.global_psichi(varobj=self.tcstrflw_obj)

        self.tcstrflw_obj.udiv = udiv.assign_attrs(
            {"units": "meter_per_second", "name": "divergent zonal wind"}
        )
        self.tcstrflw_obj.vdiv = vdiv.assign_attrs(
            {"units": "meter_per_second", "name": "divergent meridional wind"}
        )

        self.tcstrflw_obj.uhrm = uhrm.assign_attrs(
            {"units": "meter_per_second", "name": "residual zonal wind"}
        )
        self.tcstrflw_obj.vhrm = vhrm.assign_attrs(
            {"units": "meter_per_second", "name": "residual meridional wind"}
        )

        self.tcstrflw_obj.uvor = uvor.assign_attrs(
            {"units": "meter_per_second", "name": "rotational zonal wind"}
        )
        self.tcstrflw_obj.vvor = vvor.assign_attrs(
            {"units": "meter_per_second", "name": "rotational meridional wind"}
        )
        (
            self.tcstrflw_obj.udiv.values,
            self.tcstrflw_obj.vdiv.values,
            self.tcstrflw_obj.uhrm.values,
            self.tcstrflw_obj.vhrm.values,
            self.tcstrflw_obj.uvor.values,
            self.tcstrflw_obj.vvor.values,
        ) = winds.global_wind_part(varobj=self.tcstrflw_obj)

    @privatemethod
    def plev_interp(self: Metrics, varin: numpy.array) -> numpy.array:
        """
        Description
        -----------

        This method interpolates a variable `varin` to the isobaric
        vertical level(s) specified in `plevs`.

        Parameters
        ----------

        varin: numpy.array

            A Python array-type variable containing the variable to be
            interpolated to the specified vertical levels.

        Returns
        -------

        varout: numpy.array

            A Python array-type containing the interpolated variable;
            the output variable is of dimension (nz, ny, nx) where
            `nz` is the number of levels specified by `plevs` and `ny`
            and `nx` are the respective horizontal dimensions resolved
            from `varin`.

        """

        # Interpolate the variable `varin` to the specified vertical
        # levels (`plevs`).
        varout = vertical.interp(
            varin=varin, zarr=self.tcdiags_obj.inputs.pressure.values, levs=self.plevs
        )

        return varout

    @privatemethod
    def radial_filter(
        self: Metrics,
        rdlintrp_obj: object,
        tcevent: str,
        uplev: numpy.array,
        vplev: numpy.array,
    ) -> Tuple[numpy.array, numpy.array]:
        """
        Description
        -----------

        This method filters the region relative to the TC position
        using a successive radial filtering (e.g., interpolation)
        application.

        Parameters
        ----------

        rdlintrp_obj: object

            A Python object containing the radial interpolation and
            filtering attributes.

        tcevent: str

            A Python string defining the TC event identifier for which
            the radial filtering application is being performed.

        uplev: numpy.array

            A Python array-type variable containing the zonal wind
            interpolated to the pressure levels specified in `plevs`.

        vplev: numpy.array

            A Python array-type variable containing the meridional
            wind interpolated to the pressure levels specified in
            `plevs`.

        Returns
        -------

        uplev: numpy.array

            A Python array-type variable containing the respective TC
            relative radially filtered zonal wind interpolated to the
            pressure levels specified in `plevs`.

        vplev: numpy.array

            A Python array-type variable containing the respective TC
            relative radially filtered meridional wind interpolated to
            the pressure levels specified in `plevs`.

        """

        # Filter the TC event from the analysis using
        # successive radial interpolations.
        for idx in range(numpy.shape(uplev[:, 0, 0])[0]):
            msg = (
                f"Filtering zonal wind component for TC {tcevent} isobaric "
                f"level {self.plevs[idx]}."
            )
            self.logger.info(msg=msg)
            rdlintrp_obj.vararray = uplev[idx, :, :]
            uplev[idx, :, :] = radial.interp(
                interp_obj=rdlintrp_obj, method="linear")

            msg = (
                f"Filtering meridional wind component for TC {tcevent} isobaric "
                f"level {self.plevs[idx]}."
            )
            self.logger.info(msg=msg)
            rdlintrp_obj.vararray = vplev[idx, :, :]
            vplev[idx, :, :] = interp.radial.interp(
                interp_obj=rdlintrp_obj, method="linear"
            )

        return (uplev, vplev)

    @privatemethod
    def radial_dist(self: Metrics, rdlintrp_obj: object) -> object:
        """
        Description
        -----------

        This method computes the radial distance relative to a
        reference geographical location defined by the tuple `loc`
        attribute of `rdlintrp_obj`.

        Parameter
        ---------

        rdlintrp_obj: object

            A Python object containing the radial interpolation
            attributes; the tuple `loc` is assumed to be defined prior
            to entry.

        Returns
        -------

        rdlintrp_obj: object

            A Python object now containing attribute `raddist` which
            contains the radial distance relative to the reference
            location defined by `loc`; units are meters.

        """

        # Compute the radial distance.
        rdlintrp_obj.raddist = numpy.reshape(
            radial_distance(
                refloc=rdlintrp_obj.loc, latgrid=self.latgrid, longrid=self.longrid
            ),
            numpy.shape(self.tcdiags_obj.inputs.latitude.values),
        )

        return rdlintrp_obj

    @privatemethod
    def write_output(self: Metrics) -> None:
        """
        Description
        -----------

        This method writes the computed quantities to the external
        netCDF-formatted file path.

        """

        # Define the netCDF output object and write the respective
        # variables to the external netCDF-formatted file path.
        ncwrite = NCWrite(output_file=self.tcdiags_obj.tcsteering.output_file)

        ncwrite.write(
            var_obj=self.tcstrflw_obj,
            var_list=self.output_varlist,
            coords_2d=None,
            coords_3d=self.tcstrflw_obj.dims,
        )

    def run(self: Metrics) -> None:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Interpolates the wind-vector components to the isobaric
            levels specified in the TC steering flow configuration.

        (2) For each TC event the respective wind-fields is "filtered"
            using a successive radial interpolation application.

        (3) Compute diagnostic quantities from the "filtered"
            wind-vector components.

        (4) Write the results to the specified netCDF-formatted output
            file `output_file`.

        """

        # Compute/interpolate the respective wind-vector components to
        # the specified vertical levels.
        uplev = self.plev_interp(varin=self.tcdiags_obj.inputs.uwind.values)
        vplev = self.plev_interp(varin=self.tcdiags_obj.inputs.vwind.values)

        self.tcstrflw_obj.uwnd = uplev.assign_attrs(
            {"units": "meter_per_second", "name": "zonal wind"}
        )
        self.tcstrflw_obj.vwnd = vplev.assign_attrs(
            {"units": "meter_per_second", "name": "meridional wind"}
        )

        rdlintrp_obj = parser_interface.object_define()
        rdlintrp_obj.ddist = self.tcdiags_obj.tcsteering.ddist
        rdlintrp_obj.distance = self.tcdiags_obj.tcsteering.distance

        # Check whether TC information has been provided via the
        # experiment configuration; proceed accordingly.
        if self.tcdiags_obj.tcinfo is not None:
            for tcevent in self.tcdiags_obj.tcinfo:
                # Compute the radial distance grid relative to the
                # respective TC event position.
                tcevent_obj = parser_interface.dict_toobject(
                    in_dict=parser_interface.dict_key_value(
                        dict_in=self.tcdiags_obj.tcinfo, key=tcevent
                    )
                )

                msg = (
                    f"Computing the radial distance relative to TC {tcevent} "
                    f"centered at {tcevent_obj.lat_deg}, {tcevent_obj.lon_deg}."
                )
                self.logger.info(msg=msg)
                rdlintrp_obj.loc = (tcevent_obj.lat_deg, tcevent_obj.lon_deg)
                rdlintrp_obj = self.radial_dist(rdlintrp_obj)

                # Filter the respective TC event from the wind
                # analysis.
                (uplev.values, vplev.values) = self.radial_filter(
                    rdlintrp_obj=rdlintrp_obj,
                    tcevent=tcevent,
                    uplev=uplev.values,
                    vplev=vplev.values,
                )

            # Update the filtered variables.
            self.tcstrflw_obj.uwnd = uplev
            self.tcstrflw_obj.vwnd = vplev

        # Compute the diagnostic variables.
        self.compute_diags(vararr=self.tcstrflw_obj.uwnd)

        # Write the results to the specifed netCDF-formatted file
        # path.
        self.write_output()
