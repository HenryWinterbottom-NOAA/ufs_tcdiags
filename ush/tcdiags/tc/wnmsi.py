# =========================================================================

# Module: ush/tcdiags/tc/wnmsi.py

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

    wnmsi.py

Description
-----------

    This module contains the base-class object for tropical cyclone
    (TC) multi-scale intensity (MSI) application.

Classes
-------

    TCWNMSI(yaml_dict, inputs_obj)

        This is the base-class object for computing the tropical
        cyclone (TC) multi-scale intensity (MSI) attributes described
        in Vukicevic et al., [2014].

Requirements
------------

- tabulate; https://github.com/astanin/python-tabulate

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

References
----------

    Vukicevic, T., E., Uhlhorn, P. Reasor, and B. Klotz, A novel
    multiscale intensity metric for evaluation of tropical cyclone
    intensity forecasts, J. Atmos. Sci., 71 (4), 1292-13-4,
    2014. doi:10.1175/JAS-D-13-0153.1

Author(s)
---------

    Henry R. Winterbottom; 17 March 2023

History
-------

    2023-03-17: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict, List

import numpy
from exceptions import TropCycWNMSIError
from metpy.units import units
from tabulate import tabulate
from tcdiags.analysis.fft import forward_fft2d, inverse_fft2d
from tcdiags.atmos import winds
from tcdiags.geomets import bearing_geoloc
from tcdiags.interp import interp_ll2ra, interp_vertical
from tcdiags.io.inputs import VARRANGE_STRING
from tcdiags.io.outputs import TCDiagsOutputsNetCDFIO
from tools import parser_interface
from utils.logger_interface import Logger

# ----


@dataclass
class WNMSI:
    """
    Description
    -----------

    This is the base-class object for computing the tropical cyclone
    (TC) multi-scale intensity (MSI) attributes described in Vukicevic
    et al., [2014].

    Parameters
    ----------

    yaml_dict: Dict

        A Python dictionary containing the attributes from the
        experiment configuration file; the TC MSI application
        configuration values are contained in the YAML-formatted file
        path denoted by the `tcwnmsi` attribute in the experiment
        configuration.

    inputs_obj: object

        A Python object containing the mandatory input variables.

    Raises
    ------

    TropCycWNMSIError:

        - raised if the TC attributes cannot be determined from the
          `tcvitals` attributes or the attribute has not been
          specified.

    """

    def __init__(self: dataclass, yaml_dict: Dict, inputs_obj: object):
        """
        Description
        -----------

        Creates a new WNMSI object.

        """

        # Define the base-class attributes.
        self.logger = Logger()
        self.inputs_obj = inputs_obj
        self.yaml_dict = dict(yaml_dict)
        self.tcwnmsi_obj = parser_interface.object_define()
        self.tcv_dict = {}

        # Define the experiment configuration variables.
        tcwnmsi_default_var_dict = {
            "dphi": 45.0,
            "drho": 100000.0,
            "max_radius": 1000000.0,
            "max_wn": 3,
            "output_file": "%s.TCMSI.nc",
        }

        tcwnmsi_var_dict = parser_interface.update_dict(
            default_dict=tcwnmsi_default_var_dict, base_dict=self.yaml_dict
        )

        for tcwnmsi_var in tcwnmsi_var_dict:
            value = parser_interface.dict_key_value(
                dict_in=tcwnmsi_var_dict, key=tcwnmsi_var, no_split=True
            )

            self.tcwnmsi_obj = parser_interface.object_setattr(
                object_in=self.tcwnmsi_obj, key=tcwnmsi_var, value=value
            )

        # Collect the TC attributes from the experiment configuration;
        # proceed accordingly.
        tcid_list = [
            key
            for key in self.yaml_dict.keys()
            if key not in tcwnmsi_default_var_dict.keys()
        ]

        msg = (
            "The TC maximum intensity index will be computed for the following "
            f"TC events: {[tcid for tcid in tcid_list]}."
        )
        self.logger.info(msg=msg)

        for tcid in tcid_list:
            self.tcv_dict[tcid] = self.yaml_dict[tcid]

        if len(self.tcv_dict) <= 0:
            msg = (
                "The TC attributes have not been specified within "
                "the experiment configuration file attribute `tcvitals` or could "
                "not be determined. Aborting!!!"
            )
            raise TropCycWNMSIError(msg=msg)

        # Define the array dimension attributes.
        (self.nx, self.ny) = [
            self.inputs_obj.lat.shape[1],
            self.inputs_obj.lat.shape[0],
        ]
        self.ndim = self.nx * self.ny

        # Define the output variables and attributes. list.
        self.output_varlist = [
            "total_wind",
        ]

        self.output_attrslist = [
            "dist_rmw_m",
            "epsi_msi_mps",
            "heading_rmw_deg",
            "lat_0_deg",
            "lon_0_deg",
            "lat_rmw_deg",
            "lon_rmw_deg",
            "vmax_mps",
            "wn0_msi_mps",
            "wn1_msi_mps",
            "wn0p1_msi_mps",
        ]

    def compute_inputs(self: dataclass) -> None:
        """
        Description
        -----------

        This method computes the total wind speed magnitude,
        interpolates it to a geometric height of 10-meters, and
        updates the base-class object `tcwnmsi_obj` accordingly.

        """

        # Compute the vector wind speed magnitude and interpolate to a
        # geometric elevation of 10-meters.
        for wnd in ["uwnd", "vwnd"]:
            self.tcwnmsi_obj = parser_interface.object_setattr(
                object_in=self.tcwnmsi_obj,
                key=wnd,
                value=parser_interface.object_getattr(
                    object_in=self.inputs_obj, key=wnd
                ),
            )

        self.tcwnmsi_obj = winds.wndmag(inputs_obj=self.tcwnmsi_obj)

        wndmag10m = interp_vertical(
            varin=self.tcwnmsi_obj.wndmag,
            zarr=(self.inputs_obj.hght),
            levs=numpy.array(10.0),
        )

        wndmag10m = self.tcwnmsi_obj.wndmag[0, :, :]

        self.tcwnmsi_obj = parser_interface.object_setattr(
            object_in=self.tcwnmsi_obj, key="wndmag10m", value=wndmag10m
        )

        msg = VARRANGE_STRING % (
            "10-meter wind speed",
            numpy.nanmin(numpy.array(self.tcwnmsi_obj.wndmag10m)),
            numpy.nanmax(numpy.array(self.tcwnmsi_obj.wndmag10m)),
            self.tcwnmsi_obj.wndmag.units,
        )
        self.logger.info(msg=msg)

    def compute_tcmsi(self: dataclass) -> None:
        """
        Description
        -----------

        This method computes the TC MSI following Vukicevic et al.,
        [2014] and updates the base-class object accordingly.

        """

        # Define the wave-number components of the total wind field.
        wnd_wavenum = parser_interface.object_getattr(
            object_in=self.tcwnmsi_obj, key="wavenumbers"
        )

        # Define the maximum wind speed from the total wind field.
        total_wind = parser_interface.object_getattr(
            object_in=self.tcwnmsi_obj, key="total_wind"
        )
        vmax = units.Quantity(numpy.nanmax(total_wind), "mps")

        if vmax is None:
            msg = (
                "The maximum wind speed could not be determined from "
                "the total wind field; computing from the sum of the "
                "wavenumber spectra."
            )
            self.logger.warn(msg=msg)

            vmax = sum(
                numpy.nanmax(wnd_wavenum[idx]) for idx in range(0, len(wnd_wavenum))
            )

        # Compute the TC MSI attributes.
        tcmsi_dict = {
            "vmax_mps": vmax,
            "wn0_msi_mps": numpy.nanmax(wnd_wavenum[0]),
            "wn1_msi_mps": numpy.nanmax(wnd_wavenum[1]),
            "wn0p1_msi_mps": (numpy.nanmax(wnd_wavenum[0] + wnd_wavenum[1])),
            "epsi_msi_mps": (vmax - (numpy.nanmax(wnd_wavenum[0] + wnd_wavenum[1]))),
        }

        # Update the base-class object.
        for item in tcmsi_dict:
            value = parser_interface.dict_key_value(
                dict_in=tcmsi_dict, key=item, no_split=True
            )
            self.tcwnmsi_obj = parser_interface.object_setattr(
                object_in=self.tcwnmsi_obj, key=item, value=value
            )

    def compute_tcmsigeo(self: dataclass) -> None:
        """
        Description
        -----------

        This method computes the geographical location of maximum
        winds using the distance and bearing relative to the reference
        geographical location and updates the base-class object
        accordingly.

        """

        # Compute the 10-meter wind speed using the wavenumber 0 and 1
        # components of the total wind field.
        wnd_wavenum = parser_interface.object_getattr(
            object_in=self.tcwnmsi_obj, key="wavenumbers"
        )
        wind = numpy.absolute(wnd_wavenum[0] + wnd_wavenum[1])

        # Compute the geographical location of the 10-meter wind
        # maximum location.
        (didx, hidx) = numpy.where(wind == self.tcwnmsi_obj.wn0p1_msi_mps)
        (heading, dist) = (
            numpy.degrees(self.tcwnmsi_obj.azimuth[hidx]),
            numpy.array(self.tcwnmsi_obj.radial[didx]),
        )

        (lat_rmw, lon_rmw) = bearing_geoloc(
            loc1=(self.tcwnmsi_obj.lat_0_deg, self.tcwnmsi_obj.lon_0_deg),
            heading=heading,
            dist=dist,
        )

        msg = f"Maximum wind location {lat_rmw}N, {lon_rmw}E."
        self.logger.info(msg=msg)

        # Update the base-class object.
        self.tcwnmsi_obj = parser_interface.object_setattr(
            object_in=self.tcwnmsi_obj, key="dist_rmw_m", value=dist[0]
        )
        self.tcwnmsi_obj.dist_rmw_m = units.Quantity(
            self.tcwnmsi_obj.dist_rmw_m, "meters"
        )

        self.tcwnmsi_obj = parser_interface.object_setattr(
            object_in=self.tcwnmsi_obj, key="heading_rmw_deg", value=heading[0]
        )
        self.tcwnmsi_obj.heading_rmw_deg = units.Quantity(
            self.tcwnmsi_obj.heading_rmw_deg, "degrees"
        )

        self.tcwnmsi_obj = parser_interface.object_setattr(
            object_in=self.tcwnmsi_obj, key="lat_rmw_deg", value=lat_rmw
        )
        self.tcwnmsi_obj.lat_rmw_deg = units.Quantity(
            self.tcwnmsi_obj.lat_rmw_deg, "degrees"
        )

        self.tcwnmsi_obj = parser_interface.object_setattr(
            object_in=self.tcwnmsi_obj, key="lon_rmw_deg", value=lon_rmw
        )
        self.tcwnmsi_obj.lon_rmw_deg = units.Quantity(
            self.tcwnmsi_obj.lon_rmw_deg, "degrees"
        )

    def wndcmp(self: dataclass, lat_0: float, lon_0: float) -> None:
        """
        Description
        -----------

        This method computes the respective wavenumber-defined
        10-meter wind field structures in accordance with the
        experiment configuration; the 10-meter total wind field is
        transformed from a Cartesian-type grid projection to a
        polar-coordinate grid-projection; the resulting transform is
        then used to decompose the field into it's corresponding
        Fourier coefficients which are then used to
        compute/reconstruct the respective wavenumber define 10-meter
        total wind field structures.

        Parameters
        ----------

        lat_0: float

            A Python float value defining the reference latitude
            coordinate about which the Cartesian-type grid is to be
            transformed to a polar-coordinate grid-projection; units
            are degrees north.

        lon_0: float

            A Python float value defining the reference longitude
            coordinate about which the Cartesian-type grid is to be
            transformed to a polar-coordinate grid-projection; units
            are degrees east.

        """

        # Interpolate the 10-meter wind field to polar coordinates.
        msg = "Transforming the 10-meter wind field to polar coordinates."
        self.logger.info(msg=msg)

        wnd10mpolar_obj = interp_ll2ra(
            varin=self.tcwnmsi_obj.wndmag10m.magnitude,
            lats=numpy.array(self.inputs_obj.lat),
            lons=numpy.array(self.inputs_obj.lon),
            lon_0=lon_0,
            lat_0=lat_0,
            max_radius=self.tcwnmsi_obj.max_radius,
            drho=self.tcwnmsi_obj.drho,
            dphi=self.tcwnmsi_obj.dphi,
        )

        # Define the relevant attributes for TC MSI computations and
        # diagnostics and update the base-class object.
        self.tcwnmsi_obj = parser_interface.object_setattr(
            object_in=self.tcwnmsi_obj, key="azimuth", value=wnd10mpolar_obj.azimuth
        )
        self.tcwnmsi_obj.azimuth = units.Quantity(
            self.tcwnmsi_obj.azimuth, "degrees")

        self.tcwnmsi_obj = parser_interface.object_setattr(
            object_in=self.tcwnmsi_obj, key="lat_0_deg", value=lat_0
        )
        self.tcwnmsi_obj.lat_0_deg = units.Quantity(
            self.tcwnmsi_obj.lat_0_deg, "degrees"
        )
        self.tcwnmsi_obj = parser_interface.object_setattr(
            object_in=self.tcwnmsi_obj, key="lon_0_deg", value=lon_0
        )
        self.tcwnmsi_obj.lon_0_deg = units.Quantity(
            self.tcwnmsi_obj.lon_0_deg, "degrees"
        )

        self.tcwnmsi_obj = parser_interface.object_setattr(
            object_in=self.tcwnmsi_obj, key="radial", value=wnd10mpolar_obj.radial
        )
        self.tcwnmsi_obj.radial = units.Quantity(
            self.tcwnmsi_obj.radial, "meters")

        self.tcwnmsi_obj = parser_interface.object_setattr(
            object_in=self.tcwnmsi_obj, key="total_wind", value=wnd10mpolar_obj.varout
        )
        self.tcwnmsi_obj.total_wind = units.Quantity(
            self.tcwnmsi_obj.total_wind, "mps")

        # Compute the forward fast-Fourier transform of the 10-meter
        # wind field.
        varin = wnd10mpolar_obj.varout
        varout = forward_fft2d(varin=varin)

        # Deconstruct the Fourier transformed 10-meter wind field
        # accordingly and reconstruct the allowable wave numbers for
        # the 10-meter wind field.
        nallow = int(wnd10mpolar_obj.varout.shape[1] / 2)
        ncoeffs = min(self.tcwnmsi_obj.max_wn, nallow)

        if self.tcwnmsi_obj.max_wn > nallow:
            msg = f"Resetting the total number of Fourier coefficients to {ncoeffs}."
            self.logger.warn(msg=msg)

        msg = (
            f"Decomposing the 10-meter wind field using {ncoeffs} Fourier coefficients."
        )
        self.logger.info(msg=msg)
        self.wndrstrct(varin=varout, ncoeffs=ncoeffs)

    def wndrstrct(self: dataclass, varin: numpy.complex_, ncoeffs: int) -> None:
        """
        Description
        -----------

        This method deconstructs the 10-meter wind-field into the
        respective (allowable) wave-number components and updates the
        base-class object accordingly.

        Parameters
        ----------

        varin: numpy.complex_

            A Python array-type complex variable; this is typically
            the Fourier transformed 10-meter total wind-field.

        ncoeffs: int

            A Python integer specifying the number of wave-numbers
            about which to reconstruct the 10-meter total wind field.

        """

        # Save the input variable.
        fftsave = parser_interface.object_deepcopy(object_in=varin)

        # For each (allowable) wavenumber (e.g., spectral
        # coefficient), reconstruct the respective variable from using
        # the input variable field..
        wndrstrct_dict = {}

        for coeff in range(ncoeffs):
            # Define the Fourier coefficients for the respective
            # wavenumber.
            msg = f"Computing the total wind-field components for wave-number {coeff}."
            self.logger.info(msg=msg)

            fftr = numpy.zeros(fftsave.shape, dtype=numpy.complex_)
            fftr[:, coeff] = fftsave[:, coeff]

            # Compute the inverse Fourier transform.
            ifftr = inverse_fft2d(varin=fftr)

            wndrstrct_dict[coeff] = units.Quantity(numpy.real(ifftr), "mps")

        # Update the base-class object accordingly.
        self.tcwnmsi_obj = parser_interface.object_setattr(
            object_in=self.tcwnmsi_obj, key="wavenumbers", value=wndrstrct_dict
        )

    def write_output(self: dataclass, tcid: str) -> None:
        """
        Description
        -----------

        TODO

        Parameters
        ----------

        tcid: str

            A Python string defining the TC event; this is used within
            the base-class object to denote different TC events (when
            applicable).

        """

        # Build the output variable list and object.
        ncoeffs = len(self.tcwnmsi_obj.wavenumbers)
        var_list = self.output_varlist + \
            [f"wn{idx}" for idx in range(0, ncoeffs)]

        # Update the output variable object.
        wns_dict = parser_interface.object_getattr(
            object_in=self.tcwnmsi_obj, key="wavenumbers"
        )

        for idx in wns_dict:
            value = parser_interface.dict_key_value(
                dict_in=wns_dict, key=idx, no_split=True
            )
            self.tcwnmsi_obj = parser_interface.object_setattr(
                object_in=self.tcwnmsi_obj, key=f"wn{idx}", value=value
            )

        # Build the dimensional and CF compliant dimensions.
        coords_2d = OrderedDict(
            {
                "radial": (["radial"], self.tcwnmsi_obj.radial),
                "azimuth": (["azimuth"], self.tcwnmsi_obj.azimuth),
            }
        )

        coords_3d = OrderedDict(
            {
                "radial": (["radial"], self.tcwnmsi_obj.radial),
                "azimuth": (["azimuth"], self.tcwnmsi_obj.azimuth),
                "wavenumbers": (["wavenumbers"], numpy.arange(0, ncoeffs)),
            }
        )

        # Define the global attributes accordingly.
        global_attrs_dict = {}

        for global_attr in self.output_attrslist:
            attr = parser_interface.object_getattr(
                object_in=self.tcwnmsi_obj, key=global_attr, force=True
            )

            if attr is not None:
                value = numpy.array(attr)
                try:
                    units = attr.units
                    global_attrs_dict[global_attr] = f"{value} {units}"

                except AttributeError:
                    global_attrs_dict[global_attr] = value

        # Write the netCDF-formatted file path containing the TC MPI
        # attributes.
        tcdiags_out = TCDiagsOutputsNetCDFIO(
            output_file=self.tcwnmsi_obj.output_file % tcid
        )

        tcdiags_out.write(
            var_obj=self.tcwnmsi_obj,
            var_list=var_list,
            coords_2d=coords_2d,
            coords_3d=coords_3d,
            attrs_list=["units"],
            global_attrs_dict=global_attrs_dict,
        )

    def write_table(self: dataclass, tcid: str) -> None:
        """
        Description
        -----------

        This method writes the TC MSI attributes to formatted tables
        accordingly.

        Parameters
        ----------

        tcid: str

            A Python string defining the TC event; this is used within
            the base-class object to denote different TC events (when
            applicable).

        """

        def __buildtbl__(header: List, table: List) -> None:
            """
            Description
            -----------

            This function builds a table and writes it via the
            base-class logging object.

            Parameters
            ----------

            header: list

                A Python list containing the table header string(s).

            table: list

                A Python list containing the table row(s).

            """

            msg = "\n" + tabulate(
                table,
                header,
                tablefmt="fancy_grid",
                numalign=("center", "center"),
                colalign=("center", "center"),
            )
            self.logger.info(msg=msg)

        # Build and write the table for the wavenumber spectra maximum
        # wind speed values.
        header = [
            f"TC {tcid} Wave number",
            f"Maximum Wind Speed ({self.tcwnmsi_obj.uwnd.units})",
        ]

        table = []

        for idx in range(len(self.tcwnmsi_obj.wavenumbers)):
            msg = [
                f"{idx}", f"{numpy.nanmax(self.tcwnmsi_obj.wavenumbers[idx])}"]
            table.append(msg)

        __buildtbl__(header=header, table=table)

        # Build and write the table for the TC MSI attributes.
        header = [f"TC {tcid} MSI Attribute", f"Value"]

        table = []

        for item in self.output_attrslist:
            value = parser_interface.object_getattr(
                object_in=self.tcwnmsi_obj, key=item
            )

            msg = [item, value]
            table.append(msg)

        __buildtbl__(header=header, table=table)

    def run(self: dataclass):
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Computes the input fields required to compute the TC MSI.

        (2) Decomposes the total-wind field into it's respective
            wavenumber components as a function of TC event.

        (3) Computes the TC MSI attributes, including the geographical
            location for the radius of maximum winds as a function of
            TC event.

        (4) Writes a table of the respective TC MSI attributes and
            writes a netCDF-formatted file containing each of the
            (allowable) wavenumber components of the respective TC
            wind field and the attributes written to the
            aforementioned table are written as global attributes
            within the respective netCDF-formatted file.

        """

        # Compute the input variables.
        self.compute_inputs()

        # Compute the TC MSI components for each respective TC event.
        for tcid in self.tcv_dict:
            # Define the geographical location about which the
            # 10-meter wind field for the respective TC event will be
            # analyzed.
            (lat_0, lon_0) = [
                self.tcv_dict[tcid][key] for key in ["lat_deg", "lon_deg"]
            ]

            # Decompose the 10-meter wind field into the respective
            # (allowable) wave-number structures.
            self.wndcmp(lat_0=lat_0, lon_0=lon_0)

            # Compute the TC maximum potential intensity attributes.
            self.compute_tcmsi()
            self.compute_tcmsigeo()

            # Write the diagnostics accordingly.
            self.write_table(tcid=tcid)
            self.write_output(tcid=tcid)

        del self.tcwnmsi_obj
