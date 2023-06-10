# =========================================================================

# Module: ush/tcdiags/metrics/vl1991_metric.py

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
from types import SimpleNamespace
from typing import Tuple

from confs.yaml_interface import YAML
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

from tcdiags.analysis import svd

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

    tcdiags_obj: SimpleNamespace

        A Python SimpleNamespace object containing all configuration
        attributes for the respective application including inputs
        (i.e., `inputs` and `tcinfo`) as well as the remaining
        (supported) applications (see base-class attribute
        `apps_list`).

    References
    ----------

    Velden, C. S. and L. M. Leslie. "The Basic Relationship between
    Tropical Cyclone Intensity and the Depth of the Environmental
    Steering Layer in the Australian Region". Weather and Forecasting
    6 (1991): 244-253.

    DOI: https://doi.org/10.1175/1520-0434(1991)006<0244:TBRBTC>2.0.CO;2

    """

    def __init__(self: Metrics, tcdiags_obj: SimpleNamespace):
        """
        Description
        -----------

        Creates a new VL1991 object.

        """

        # Define the base-class attributes.
        super().__init__(tcdiags_obj=tcdiags_obj)
        self.options_obj = parser_interface.dict_toobject(
            in_dict=self.schema(cls_schema_file=tcdiags_obj.tcsteering.schema,
                                cls_opts=parser_interface.object_todict(
                                    object_in=tcdiags_obj.tcsteering)
                                )
        )

        self.output_varlist = list(self.options_obj.output_varlist.keys())
        self.tcstrflw_obj = parser_interface.object_define()

        self.plevs = numpy.array([plev for plev in self.options_obj.isolevels])
        self.tcstrflw_obj.dims = {
            "plevs": (["plevs"], self.plevs),
            "lat": (["lat"], self.tcdiags_obj.inputs.latitude.values[:, 0]),
            "lon": (
                ["lon"],
                self.tcdiags_obj.inputs.longitude.values[0, :]
                - self.tcdiags_obj.inputs.longitude.scale_add,
            ),
        }

    @privatemethod
    def compute_diags(self: Metrics, uwnd: numpy.array, vwnd: numpy.array) -> None:
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

        # Initialize the diagnostic variable quantities.
        varobj = parser_interface.object_define()
        diagvars_obj = parser_interface.dict_toobject(
            in_dict=self.options_obj.output_varlist)
        (nx, ny, nz) = [len(self.tcdiags_obj.inputs.longitude.values[0, :]),
                        len(self.tcdiags_obj.inputs.latitude.values[:, 0]),
                        len(self.plevs)
                        ]
        for output_var in self.output_varlist:
            self.tcstrflw_obj = parser_interface.object_setattr(
                object_in=self.tcstrflw_obj, key=output_var,
                value=parser_interface.object_define())

        # Interpolate the winds to the specified isobaric levels.
        varobj.uwnd = self.plev_interp(varin=uwnd)
        varobj.vwnd = self.plev_interp(varin=vwnd)
        self.tcstrflw_obj.uwnd = varobj.uwnd.assign_attrs(
            diagvars_obj.uwnd)
        self.tcstrflw_obj.uwnd.values = varobj.uwnd
        self.tcstrflw_obj.vwnd = varobj.vwnd.assign_attrs(
            diagvars_obj.vwnd)
        self.tcstrflw_obj.vwnd.values = varobj.vwnd

        # Compute the velocity potential and streamfunction.
        (self.tcstrflw_obj.chi, self.tcstrflw_obj.psi) = [
            varobj.uwnd.assign_attrs(
                parser_interface.object_getattr(
                    object_in=diagvars_obj, key=varname)) for
            varname in ["chi", "psi"]
        ]
        (self.tcstrflw_obj.chi.values, self.tcstrflw_obj.psi.values) = \
            winds.global_psichi(varobj=varobj)

        # Compute the vorticity and divergence.
        (self.tcstrflw_obj.divg, self.tcstrflw_obj.vort) = [
            varobj.uwnd.assign_attrs(
                parser_interface.object_getattr(
                    object_in=diagvars_obj, key=varname)) for
            varname in ["divg", "vort"]
        ]
        self.tcstrflw_obj.divg.values = winds.global_divg(varobj=varobj)
        self.tcstrflw_obj.vort.values = winds.global_vort(varobj=varobj)

        # Compute the components of the total wind field.
        [parser_interface.object_setattr(
            object_in=self.tcstrflw_obj, key=varname,
            value=varobj.uwnd.assign_attrs(parser_interface.object_getattr(
                object_in=diagvars_obj, key=varname)
            )
        ) for varname in ["udiv", "uhrm", "urot", "vdiv", "vhrm", "vrot"]
        ]
        (
            self.tcstrflw_obj.udiv.values,
            self.tcstrflw_obj.vdiv.values,
            self.tcstrflw_obj.uhrm.values,
            self.tcstrflw_obj.vhrm.values,
            self.tcstrflw_obj.urot.values,
            self.tcstrflw_obj.vrot.values,
        ) = winds.global_wind_part(varobj=varobj)

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

            A Python numpy.array variable containing the variable to
            be interpolated to the specified vertical levels.

        Returns
        -------

        varout: numpy.array

            A Python numpy.array variable containing the interpolated
            variable; the output variable is of dimension (nz, ny, nx)
            where `nz` is the number of levels specified by `plevs`
            and `ny` and `nx` are the respective horizontal dimensions
            resolved from `varin`.

        """

        # Interpolate the variable `varin` to the specified vertical
        # levels (`plevs`).
        varout = vertical.interp(
            varin=varin, zarr=self.tcdiags_obj.inputs.pressure.values, levs=self.plevs
        )

        return varout

    @staticmethod
    def filter_var(varin: numpy.array, ncoeffs: int) -> numpy.array:
        """
        Description
        -----------

        This method filters a specified input variable `varin` by
        deconstructing the respective variable using singular value
        decomposition (SVD) methods and subsequently reconstructing
        the variable field using only the specified singular values as
        determined by the value for `ncoeffs` upon entry.

        Parameters
        ----------

        varin: numpy.array

            A Python numpy.array variable containing the input
            variable to be filtered.

        ncoeffs: int

            A Python integer specifying the maximum singular value,
            relative to 0, to set 0.0 prior to reconstrucing the
            respective variable.

        Returns
        -------

        varout: numpy.array

            A Python numpy.array variable containing the deconstucted
            variable `varin` that has been reconstructed using the
            singular value spectrum defined by `noeff` upon entry.

        """

        # Deconstruct the variable using SVD and reconstruct as per
        # the singular value spectrum defined by `ncoeffs`.
        varout = numpy.zeros(numpy.shape(varin))
        varout = svd.rebuild(varin=varin, ncoeffs=ncoeffs)

        return varout

    @privatemethod
    def tc_filter(self: Metrics) -> Tuple[numpy.array, numpy.array]:
        """
        Description
        -----------

        This method defines a relaxation mask with respect to the
        defined TC event locations; the SVD of the respective zonal-
        and meridional-wind components is performed in order to
        minimize the signal of the respective TC events in the wind
        field and the relaxation mask is applied to reduce the signal
        of the respective TC events in the respective wind component
        analyses.

        Returns
        -------

        uwind: numpy.array

            A Python numpy.array variable containing the reconstructed
            zonal wind component.

        vwind: numpy.array

            A Python numpy.array variable containing the reconstructed
            meridional wind component.

        """

        # Filter the TC event signal and reconstruct the respective
        # zonal- and meridional-wind components.
        mask = self.tc_mask()
        uwind = self.tcdiags_obj.inputs.uwind.values._magnitude
        vwind = self.tcdiags_obj.inputs.vwind.values._magnitude
        for level in range(numpy.shape(uwind)[0]):
            ufilt = self.filter_var(
                varin=uwind[level, :, :], ncoeffs=self.options_obj.ncoeffs)
            uwind[level, :, :] = (1.0 - mask)*(uwind[level, :, :] - ufilt) \
                + mask*uwind[level, :, :]
            vfilt = self.filter_var(
                varin=vwind[level, :, :], ncoeffs=self.options_obj.ncoeffs)
            vwind[level, :, :] = (1.0 - mask)*(vwind[level, :, :] - vfilt) \
                + mask*vwind[level, :, :]

        return (uwind, vwind)

    @privatemethod
    def tc_mask(self: Metrics) -> numpy.array:
        """
        Description
        -----------

        This method defines a relaxation mask used to filter the
        respective variables relative to the specified TC locations.

        Returns
        -------

        mask: numpy.array

            A Python numpy.array variable specifying the relaxation
            mask relative to each TC event location.

        """

        # Initialize the relaxation mask.
        latgrid = numpy.array(self.tcdiags_obj.inputs.latitude.values).ravel()
        longrid = numpy.array(self.tcdiags_obj.inputs.longitude.values).ravel()
        mask = numpy.zeros(numpy.shape(
            self.tcdiags_obj.inputs.longitude.values))
        mask[:, :] = 1.0

        # Update the relaxation mask relative to the location of each
        # TC event.
        for tcevent in self.tcdiags_obj.tcinfo:
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

            # Compute the radial distance grid relative to the
            # respective TC event location.
            raddist = numpy.reshape(radial_distance(
                refloc=(tcevent_obj.lat_deg, tcevent_obj.lon_deg),
                latgrid=latgrid, longrid=longrid),
                numpy.shape((self.tcdiags_obj.inputs.latitude.values)))

            # Update the masked region relative to the respective TC
            # event.
            mask = numpy.where(raddist <= self.options_obj.distance, 0.0, mask)
            mask = numpy.where((raddist > self.options_obj.distance) &
                               (raddist < self.options_obj.relax_distance),
                               (raddist - self.options_obj.distance) /
                               (self.options_obj.relax_distance -
                                self.options_obj.distance), mask)

        return mask

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

        # TODO

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

        # Filter the respective vector wind components relative to the
        # TC event locations and interpolate to the specified pressure
        # levels.
        (uwnd, vwnd) = self.tc_filter()

        # Compute the diagnostic variables.
        self.compute_diags(uwnd=uwnd, vwnd=vwnd)

        # Write the results to the specifed netCDF-formatted file
        # path.
        self.write_output()
