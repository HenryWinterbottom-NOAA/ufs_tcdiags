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


"""

# ----


# ----

import copy
import numpy
from exceptions import TropCycWNMSIError

import gc
from tcdiags.io.inputs import VARRANGE_STRING
from tcdiags.analysis.fft import forward_fft2d, inverse_fft2d
from tcdiags.atmos import winds
from tcdiags.interp import interp_ll2ra, interp_vertical

from dataclasses import dataclass
from typing import Dict, List, Union

from tools import parser_interface

from utils.logger_interface import Logger

from tabulate import tabulate

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


@dataclass
class WNMSI:
    """
    Description
    -----------

    Parameters
    ----------

    Raises
    ------


    """

    def __init__(self, yaml_dict: Dict, inputs_obj: object):
        """
        Descriptions
        ------------

        Creates a new WNMSI object.

        """

        # Define the base-class attributes.
        self.logger = Logger()
        self.inputs_obj = inputs_obj
        self.yaml_dict = dict(yaml_dict)
        self.tcwnmsi_obj = parser_interface.object_define()
        self.tcv_dict = {}

        # Define the experiment configuration variables.
        tcwnmsi_default_var_dict = {"dphi": 45.0, "drho": 100000.0,
                                    "max_radius": 1000000.0, "max_wn": 3
                                    }
        tcwnmsi_var_dict = parser_interface.update_dict(
            default_dict=tcwnmsi_default_var_dict, base_dict=self.yaml_dict)

        for tcwnmsi_var in tcwnmsi_var_dict:
            value = parser_interface.dict_key_value(
                dict_in=tcwnmsi_var_dict, key=tcwnmsi_var, no_split=True)

            self.tcwnmsi_obj = parser_interface.object_setattr(
                object_in=self.tcwnmsi_obj, key=tcwnmsi_var, value=value)

        # Collect the TC attributes from the experiment configuration;
        # proceed accordingly.
        tcid_list = [key for key in self.yaml_dict.keys()
                     if key not in tcwnmsi_default_var_dict.keys()]

        msg = ("The TC maximum intensity index will be computed for the following "
               f"TC events: {[tcid for tcid in tcid_list]}.")
        self.logger.info(msg=msg)

        for tcid in tcid_list:
            self.tcv_dict[tcid] = self.yaml_dict[tcid]

        if len(self.tcv_dict) <= 0:
            msg = ("The TC attributes have not been specified within "
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

        # Compute the input variables.
        self.compute_inputs()

    def _build_table(self, header: List, table: List) -> None:
        """ """

        msg = "\n" + tabulate(table, header,
                              tablefmt="fancy_grid", numalign=("center", "center"),
                              colalign=("center", "center"))
        self.logger.info(msg=msg)

    def compute_inputs(self) -> None:
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
                object_in=self.tcwnmsi_obj, key=wnd,
                value=parser_interface.object_getattr(
                    object_in=self.inputs_obj, key=wnd)
            )

        self.tcwnmsi_obj = winds.wndmag(inputs_obj=self.tcwnmsi_obj)

        wndmag10m = interp_vertical(varin=self.tcwnmsi_obj.wndmag,
                                    zarr=(self.inputs_obj.hght),
                                    levs=numpy.array(10.0))

        wndmag10m = self.tcwnmsi_obj.wndmag[0, :, :]

        self.tcwnmsi_obj = parser_interface.object_setattr(
            object_in=self.tcwnmsi_obj, key="wndmag10m",
            value=wndmag10m)

        msg = VARRANGE_STRING % ("10-meter wind speed",
                                 numpy.nanmin(numpy.array(
                                     self.tcwnmsi_obj.wndmag10m)),
                                 numpy.nanmax(numpy.array(
                                     self.tcwnmsi_obj.wndmag10m)),
                                 self.tcwnmsi_obj.wndmag.units
                                 )
        self.logger.info(msg=msg)

    def compute_tcmsi(self, tcid: str) -> object:
        """ """

        # Define the wave-number components of the total wind field.
        wnd_wavenum = parser_interface.object_getattr(
            object_in=self.tcwnmsi_obj, key="wavenumbers")

        # Build the table for the wavenumber spectra maximum wind
        # speed values.
        header = [f"TC {tcid} Wave number",
                  f"Maximum Wind Speed ({self.tcwnmsi_obj.uwnd.units})"]

        table = []

        for idx in range(len(wnd_wavenum)):
            msg = [f"{idx}", f"{numpy.nanmax(wnd_wavenum[idx])}"]
            table.append(msg)

        self._build_table(header=header, table=table)

        # Define the maximum wind speed from the total wind field.
        total_wind = parser_interface.object_getattr(
            object_in=self.tcwnmsi_obj, key="total_wind")
        vmax = numpy.nanmax(total_wind)

        if vmax is None:
            msg = ("The maximum wind speed could not be determined from "
                   "the total wind field; computing from the sum of the "
                   "wavenumber spectra."
                   )
            self.logger.warn(msg=msg)

            vmax = sum(numpy.nanmax(wnd_wavenum[idx]) for idx in
                       range(0, len(wnd_wavenum)))

        # Compute the TC MSI attributes.
        tcmsi_dict = {"vmax": vmax, "wn0": numpy.nanmax(wnd_wavenum[0]),
                      "wn1": numpy.nanmax(wnd_wavenum[1]),
                      "wn0p1": (numpy.nanmax(wnd_wavenum[0] + wnd_wavenum[1])),
                      "epsi": (vmax - (numpy.nanmax(wnd_wavenum[0] + wnd_wavenum[1])))
                      }

        # Build the table for the TC MSI attributes.
        header = [f"TC {tcid} MSI Attribute",
                  f"Value ({self.tcwnmsi_obj.uwnd.units})"]

        table = []

        for item in tcmsi_dict:
            value = parser_interface.dict_key_value(
                dict_in=tcmsi_dict, key=item, no_split=True)
            self.tcwnmsi_obj = parser_interface.object_setattr(
                object_in=self.tcwnmsi_obj, key=item, value=value)

            msg = [item, value]
            table.append(msg)

        self._build_table(header=header, table=table)

    def wndcmp(self, lat_0: float, lon_0: float):
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

        tcid: str

            A Python string defining the TC event; this is used within
            the base-class object to denote different TC events (when
            applicable).

        """

        # Interpolate the 10-meter wind field to polar coordinates.
        msg = "Transforming the 10-meter wind field to polar coordinates."
        self.logger.info(msg=msg)

        wnd10mpolar_obj = interp_ll2ra(varin=self.tcwnmsi_obj.wndmag10m.magnitude,
                                       lats=numpy.array(self.inputs_obj.lat),
                                       lons=numpy.array(self.inputs_obj.lon),
                                       lon_0=lon_0, lat_0=lat_0,
                                       max_radius=self.tcwnmsi_obj.max_radius,
                                       drho=self.tcwnmsi_obj.drho,
                                       dphi=self.tcwnmsi_obj.dphi)

        self.tcwnmsi_obj = parser_interface.object_setattr(
            object_in=self.tcwnmsi_obj, key="total_wind",
            value=wnd10mpolar_obj.varout)

        # Compute the forward fast-Fourier transform of the 10-meter
        # wind field.
        varin=wnd10mpolar_obj.varout
        varout=forward_fft2d(varin=varin)

        # Deconstruct the Fourier transformed 10-meter wind field
        # accordingly and reconstruct the allowable wave numbers for
        # the 10-meter wind field.
        nallow=int(wnd10mpolar_obj.varout.shape[1]/2)
        ncoeffs=min(self.tcwnmsi_obj.max_wn, nallow)

        if self.tcwnmsi_obj.max_wn > nallow:
            msg=f"Resetting the total number of Fourier coefficients to {ncoeffs}."
            self.logger.warn(msg=msg)

        msg=f"Decomposing the 10-meter wind field using {ncoeffs} Fourier coefficients."
        self.logger.info(msg=msg)
        self.wndrstrct(varin=varout, ncoeffs=ncoeffs)

    def wndrstrct(self, varin: numpy.complex_, ncoeffs: int) -> numpy.complex_:
        """
        Description
        -----------

        This method deconstructs the 10-meter wind-field into the
        respective (allowable) wave-number components and updates the
        base-class object accordingly.

        Parameters
        ----------

        varin: array-type

            A Python array-type complex variable; this is typically
            the Fourier transformed 10-meter total wind-field.

        ncoeffs: int

            A Python integer specifying the number of wave-numbers
            about which to reconstruct the 10-meter total wind field.

        """

        # Save the input variable.
        fftsave=parser_interface.object_deepcopy(
            object_in=varin)

        # For each (allowable) wavenumber (e.g., spectral
        # coefficient), reconstruct the respective variable from using
        # the input variable field..
        wndrstrct_dict={}

        for coeff in range(ncoeffs):

            # Define the Fourier coefficients for the respective
            # wavenumber.
            msg=f"Computing the total wind-field components for wave-number {coeff}."
            self.logger.info(msg=msg)

            fftr=numpy.zeros(fftsave.shape, dtype=numpy.complex_)
            fftr[:, coeff]=fftsave[:, coeff]

            # Compute the inverse Fourier transform.
            ifftr=inverse_fft2d(varin=fftr)

            wndrstrct_dict[coeff] = numpy.real(ifftr)

        # Update the base-class object accordingly.
        self.tcwnmsi_obj = parser_interface.object_setattr(
            object_in=self.tcwnmsi_obj, key="wavenumbers",
            value=wndrstrct_dict)

    def run(self) -> None:
        """
        Description
        -----------


        """

        # Compute the TC MSI components for each respective TC event.
        for tcid in self.tcv_dict:

            # Define the geographical location about which the
            # 10-meter wind field for the respective TC event will be
            # analyzed.
            (lat_0, lon_0) = [self.tcv_dict[tcid][key]
                              for key in ["lat_deg", "lon_deg"]]

            # Decompose the 10-meter wind field into the respective
            # (allowable) wave-number structures.
            self.wndcmp(lat_0=lat_0, lon_0=lon_0)

            # Compute the TC maximum potential intensity attributes.
            self.compute_tcmsi(tcid=tcid)
