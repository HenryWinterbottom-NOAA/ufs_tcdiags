"""
Module
------

    vurk2014_msi.py

Description
-----------

    This module contains the base-class object for tropical cyclone
    (TC) multi-scale intensity (MSI) application.

Classes
-------

    VURK2014(tcdiags_obj)

        This is the base-class object for computing the tropical
        cyclone (TC) multi-scale intensity (MSI) attributes described
        in Vukicevic et al., [2014]; it is a sub-class of Diagnostics.

Requirements
------------

- ufs_diags; https://github.com/HenryWinterbottom-NOAA/ufs_diags

- ufs_pyutils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

References
----------

    Vukicevic, T., E., Uhlhorn, P. Reasor, and B. Klotz, A novel
    multiscale intensity metric for evaluation of tropical cyclone
    intensity forecasts, J. Atmos. Sci., 71 (4), 1292-13-4,
    2014. doi:10.1175/JAS-D-13-0153.1

Author(s)
---------

    Henry R. Winterbottom; 15 June 2023

History
-------

    2023-06-15: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=protected-access

# ----

import asyncio
from collections import OrderedDict
from types import SimpleNamespace
from typing import Dict, Tuple

import numpy
import xarray
from derived.atmos import winds
from grids.bearing_geoloc import bearing_geoloc
from interp.ll2ra import ll2ra
from interp.vertical import interp
from metpy.units import units
from pint import UnitRegistry
from tools import parser_interface
from transforms.fft import forward_fft2d, inverse_fft2d
from utils import table_interface
from utils.decorator_interface import privatemethod

from tcdiags.diagnostics import Diagnostics

# ----


class VURK2014(Diagnostics):
    """
    Description
    -----------

    This is the base-class object for computing the tropical cyclone
    (TC) multi-scale intensity (MSI) attributes described in Vukicevic
    et al., [2014]; it is a sub-class of Diagnostics.

    Parameters
    ----------

    tcdiags_obj: SimpleNamespace

        A Python SimpleNamespace object containing all configuration
        attributes for the respective application including inputs
        (i.e., `inputs` and `tcinfo`) as well as the remaining
        (supported) applications.

    """

    # Define the table variable attributes.
    TBL_ATTR_DICT = OrderedDict(
        {
            "vmax": "Maximum wind speed",
            "rmw": "Radius of maximum wind",
            "lat_rmw": "Maximum wind latitude",
            "lon_rmw": "Maximum wind longitude",
            "head_rmw": "Azimuth of radius of maximum wind",
            "wn0_msi": "Wavenumber 0 Maximum Wind Speed",
            "wn1_msi": "Wavenumber 1 Maximum Wind Speed",
            "wn0p1_msi": "Wavenumber (0 + 1) Maximum Wind Speed",
            "epsi_msi": "Residual wind speed",
        },
    )
    NCOUT_ATTRS = {
        "name": "wavenumber spectra for the 10-meter wind field",
        "description": "Polar projection for the near surface total wind "
        "field wave number spectra.",
    }

    def __init__(self: Diagnostics, tcdiags_obj: SimpleNamespace):
        """
        Description
        -----------

        Creates a new VURK2014 object.

        """

        # Define the base-class attributes.
        super().__init__(tcdiags_obj=tcdiags_obj, app="tcmsi")
        self.output_varlist = list(self.options_obj.output_varlist.keys())
        self.tcmsi_obj = parser_interface.object_define()
        self.diagsvar_obj = parser_interface.dict_toobject(
            in_dict=self.options_obj.output_varlist
        )
        self.wnd_units = "meter_per_second"

    @privatemethod
    def build_cfmeta(
        self: Diagnostics, tcinfo_obj: SimpleNamespace
    ) -> Tuple[Dict, Dict]:
        """
        Description
        -----------

        This method defines the Climate and Forecast (CF) COORDS
        compliant dimension attributes metadata.

        Parameters
        ----------

        tcinfo_obj: SimpleNamespace

            A Python SimpleNamespace object containing the attributes
            and diagnostics for the respective TC event.

        Returns
        -------

        coords_2d: Dict

            A Python dictionary containing the 2-dimensional variable
            CF COORDS complinant dimension attribute metadata.

        coords_3d: Dict

            A Python dictionary containing the 3-dimensional variable
            CF COORDS complinant dimension attribute metadata.

        """

        # Define the netCDF-formatted output file attributes.
        coords_2d = OrderedDict(
            {
                "radial": (["radial"], tcinfo_obj.wnds10m.radial),
                "azimuth": (["azimuth"], tcinfo_obj.wnds10m.azimuth),
            }
        )
        coords_3d = OrderedDict(
            {
                "wavenumber": (["wavenumber"], numpy.arange(0, tcinfo_obj.ncoeffs)),
                **coords_2d,
            }
        )

        return (coords_2d, coords_3d)

    @privatemethod
    def build_tables(self: Diagnostics, tcinfo_obj: SimpleNamespace, tcid: str) -> None:
        """
        Description
        -----------

        This method composes and writes formatted tables to standard
        output corresponding to the MSI attributes computed for the
        respective TC event.

        Parameters
        ----------

        tcinfo_obj: SimpleNamespace

            A Python SimpleNamespace object containing the attributes
            and diagnostics for the respective TC event.

        tcid: str

            A Python string specifying the identifier (i.e., name) for
            the respective TC event.

        """

        # Build and write table containing wind speed values for each
        # wavenumber component.
        table_obj = parser_interface.object_define()
        var_units = UnitRegistry().get_symbol(str(tcinfo_obj.wndspec.wn0.u))
        table_obj.header = [
            f"TC {tcid} Wave Number",
            f"Maximum Wind Speed ({var_units})",
        ]
        table_obj.table = []
        for coeff in range(tcinfo_obj.ncoeffs):
            value = numpy.nanmax(
                parser_interface.object_getattr(
                    object_in=tcinfo_obj.wndspec, key=f"wn{coeff}"
                )
            )
            table_obj.table.append([f"{coeff}", value._magnitude])
        table = table_interface.compose(table_obj=table_obj)
        self.logger.info(msg="\n\n" + table + "\n\n")

        # Build and write table containing the MSI attributes.
        table_obj.header = [
            f"TC {tcid} MSI Attribute",
            "Value",
            "Units",
        ]
        table_obj.table = []
        for item in self.TBL_ATTR_DICT:
            value = parser_interface.object_getattr(object_in=tcinfo_obj, key=item)
            table_obj.table.append(
                [
                    f"{self.TBL_ATTR_DICT[item]}",
                    f"{value._magnitude}",
                    format(value.units, "~"),
                ]
            )
        table = table_interface.compose(table_obj=table_obj)
        self.logger.info(msg="\n\n" + table + "\n\n")

    @privatemethod
    async def compute_inputs(self: Diagnostics) -> None:
        """
        Description
        -----------

        This method computes the inputs for the TC MSI application;
        the total wind speed magnitude is computed and subsequently
        interpolated to height of 10-meters; the attribute `wnds10m`
        is written to the base-class attribute `tcmsi_obj`.

        """

        # Compute the magnitude of the total wind field.
        msg = "Computing the wind field magnitude."
        self.logger.info(msg=msg)
        varobj = parser_interface.object_define()
        varobj.uwnd = self.tcdiags_obj.inputs.uwind.values._magnitude
        varobj.vwnd = self.tcdiags_obj.inputs.vwind.values._magnitude
        wndmag = await winds.wndmag(varobj=varobj)

        # Interpolate to estimate the 10-meter wind field.
        msg = "Interpolating the wind field magnitude to a 10-meter elevation."
        self.logger.info(msg=msg)
        self.tcmsi_obj.wnds10m = interp(
            varin=wndmag,
            zarr=self.tcdiags_obj.inputs.height.values,
            levs=[10.0],
        )
        self.tcmsi_obj.wnds10m.values = numpy.where(
            numpy.nan, wndmag[0, :, :], self.tcmsi_obj.wnds10m.values
        )

    @privatemethod
    def compute_msi(self: Diagnostics, tcinfo_obj: SimpleNamespace) -> SimpleNamespace:
        """
        Description
        -----------

        This method computes the MSI attributes for the respective TC
        event; in addition to the MSI attributes described in
        Vukicevic et al., [2014], estimates for the location of the
        MSI defined maximum wind speed and the radius of maximum winds
        are appended to the parameter `tcinfo_obj`.

        Parameters
        ----------

        tcinfo_obj: SimpleNamespace

            A Python SimpleNamespace object containing the attributes
            and diagnostics for the respective TC event.

        Returns
        -------

        tcinfo_obj: SimpleNamespace

            A Python SimpleNamespace object containing the attributes
            contained upon entry and appended with the MSI attributes
            for the respective TC event.

        """

        # Compute the 10-meter wind speed MSI attributes.
        vmax = units.Quantity(numpy.nanmax(tcinfo_obj.wnds10m.varout), self.wnd_units)
        if vmax is None:
            vmax = sum(
                numpy.nanmax(
                    parser_interface.object_getattr(
                        object_in=tcinfo_obj.wndspec, key=f"wn{coeff}"
                    )
                )
                for coeff in range(0, tcinfo_obj.ncoeffs)
            )
        tcinfo_obj.vmax = vmax
        wn0p1 = tcinfo_obj.wndspec.wn0 + tcinfo_obj.wndspec.wn1
        tcinfo_obj.wn0p1_msi = units.Quantity(numpy.nanmax(wn0p1), self.wnd_units)
        tcinfo_obj.wn0_msi = units.Quantity(
            numpy.nanmax(tcinfo_obj.wndspec.wn0), self.wnd_units
        )
        tcinfo_obj.wn1_msi = units.Quantity(
            numpy.nanmax(tcinfo_obj.wndspec.wn1), self.wnd_units
        )
        tcinfo_obj.epsi_msi = units.Quantity(
            (tcinfo_obj.vmax - tcinfo_obj.wn0p1_msi), self.wnd_units
        )

        # Compute the 10-meter wind speed MSI location attributes.
        wn0p1 = numpy.absolute(tcinfo_obj.wndspec.wn0 + tcinfo_obj.wndspec.wn1)
        (ridx, aidx) = numpy.where(
            wn0p1._magnitude
            == numpy.max(numpy.absolute(tcinfo_obj.wn0p1_msi._magnitude))
        )
        tcinfo_obj.rmw_azimuth = numpy.degrees(tcinfo_obj.wnds10m.azimuth[aidx])[0]
        tcinfo_obj.rmw_radius = (tcinfo_obj.wnds10m.radial[ridx])[0]
        tcinfo_obj.rmw = units.Quantity(tcinfo_obj.rmw_radius, "meters")
        tcinfo_obj.head_rmw = numpy.degrees(tcinfo_obj.rmw_azimuth)
        (tcinfo_obj.lat_rmw, tcinfo_obj.lon_rmw) = bearing_geoloc(
            loc1=(tcinfo_obj.lat_deg, tcinfo_obj.lon_deg),
            heading=tcinfo_obj.head_rmw,
            dist=tcinfo_obj.rmw_radius,
        )
        tcinfo_obj.head_rmw = units.Quantity(tcinfo_obj.rmw_azimuth, "degree")
        (tcinfo_obj.lat_rmw, tcinfo_obj.lon_rmw) = (
            units.Quantity(tcinfo_obj.lat_rmw, "degree"),
            units.Quantity(tcinfo_obj.lon_rmw, "degree"),
        )
        (_, tcinfo_obj.lon_llcrnr) = bearing_geoloc(
            loc1=(tcinfo_obj.lat_deg, tcinfo_obj.lon_deg),
            heading=270.0,
            dist=self.options_obj.max_radius,
        )
        (_, tcinfo_obj.lon_urcrnr) = bearing_geoloc(
            loc1=(tcinfo_obj.lat_deg, tcinfo_obj.lon_deg),
            heading=90.0,
            dist=self.options_obj.max_radius,
        )
        (tcinfo_obj.lat_urcrnr, _) = bearing_geoloc(
            loc1=(tcinfo_obj.lat_deg, tcinfo_obj.lon_deg),
            heading=0.0,
            dist=self.options_obj.max_radius,
        )
        (tcinfo_obj.lat_llcrnr, _) = bearing_geoloc(
            loc1=(tcinfo_obj.lat_deg, tcinfo_obj.lon_deg),
            heading=180.0,
            dist=self.options_obj.max_radius,
        )

        return tcinfo_obj

    @privatemethod
    def decmpwnd(
        self: Diagnostics, varin: numpy.complex_, ncoeffs: int
    ) -> SimpleNamespace:
        """
        Description
        -----------

        This method decomposes the spectra into the corresponding
        wavenumber components and reconstructs the corresponding
        real-space field.

        Parameters
        ----------

        varin: numpy.complex_

            A Python numpy.complex_ variable containing a Fourier
            transformed variable field.

        ncoeffs: int

            A Python integer specifying the total number of wavenumber
            coefficients to use for the decomposition.

        Returns
        -------

        fft_obj: SimpleNamespace

            A Python SimpleNamespace object containing the real-space
            field reconstructed using the allowable wavenumbers.

        """

        # Reconstuct the Fourier transformed field using the allowable
        # wavenumbers.
        fft_obj = parser_interface.object_define()
        varin_save = parser_interface.object_deepcopy(object_in=varin)
        for coeff in range(ncoeffs):
            fftr = numpy.zeros(varin_save.shape, dtype=numpy.complex_)
            fftr[:, coeff] = varin_save[:, coeff]
            ifftr = inverse_fft2d(varin=fftr)
            fft_obj = parser_interface.object_setattr(
                object_in=fft_obj,
                key=f"wn{coeff}",
                value=units.Quantity(numpy.real(ifftr), self.wnd_units),
            )

        return fft_obj

    @privatemethod
    def interp_ll2ra(self: Diagnostics, tcinfo_obj: SimpleNamespace) -> SimpleNamespace:
        """
        Description
        -----------

        This method projects the 10-meter wind field analysis into a
        radial and azimuthal coordinate system centered at the
        location (e.g., latitude and longitude) for the respective TC
        event.

        Parameters
        ----------

        tcinfo_obj: SimpleNamespace

            A Python SimpleNamespace object containing the attributes
            and diagnostics for the respective TC event.

        Returns
        -------

        tcinfo_obj: SimpleNamespace

            A Python SimpleNamespace object containing the attributes
            contained upon entry and appended with the coordinate
            system attributes for the respective TC event.

        """

        # Interpolate the 10-meter wind speed magnitude to a radius
        # and azimuthal projection.
        tcinfo_obj.wnds10m = ll2ra(
            varin=numpy.array(self.tcmsi_obj.wnds10m.values),
            lats=numpy.array(self.tcdiags_obj.inputs.latitude.values),
            lons=numpy.array(self.tcdiags_obj.inputs.longitude.values),
            lat_0=tcinfo_obj.lat_deg,
            lon_0=tcinfo_obj.lon_deg,
            max_radius=self.options_obj.max_radius,
            dphi=self.options_obj.dphi,
            drho=self.options_obj.drho,
        )

        return tcinfo_obj

    @privatemethod
    def specanly(self: Diagnostics, tcinfo_obj: SimpleNamespace) -> None:
        """
        Description
        -----------

        This method performs the spectral analysis of the 10-meter
        wind field defined within the radial and azimuthal coordinate
        system for the respective TC event.

        Parameters
        ----------

        tcinfo_obj: SimpleNamespace

            A Python SimpleNamespace object containing the attributes
            and diagnostics for the respective TC event.

        Returns
        -------

        tcinfo_obj: SimpleNamespace

            A Python SimpleNamespace object containing the attributes
            contained upon entry and appended with the spectral
            analysis attributes for the respective TC event.

        """

        # Compute the FFT.
        fft_varin = forward_fft2d(varin=tcinfo_obj.wnds10m.varout)

        # Update the spectral analysis attributes accordingly.
        ncoeffs = min(
            self.options_obj.max_wn, int(tcinfo_obj.wnds10m.varout.shape[1] / 2)
        )
        if ncoeffs != self.options_obj.max_wn:
            msg = (
                "Resetting the total number of Fourier coefficients "
                f"from {self.options_obj.max_wn} to {ncoeffs}."
            )
            self.logger.warn(msg=msg)
        tcinfo_obj.ncoeffs = ncoeffs

        # Reconstruct the 10-meter wind field using the specified
        # number of allowable Fourier coefficients.
        tcinfo_obj.wndspec = self.decmpwnd(varin=fft_varin, ncoeffs=ncoeffs)

        return tcinfo_obj

    @privatemethod
    def write_polar_output(
        self: Diagnostics, tcinfo_obj: SimpleNamespace, tcid: str
    ) -> None:
        """
        Description
        -----------

        This method compiles the netCDF-formatted output file CF
        compliant metadata and write the MSI attributes to the
        specified netCDF-formatted output file.

        Parameters
        ----------

        tcid: str

            A Python string specifying the identifier (i.e., name) for
            the respective TC event.

        """

        # Build the netCDF-formatted file metadata.
        (coords_2d, coords_3d) = self.build_cfmeta(tcinfo_obj=tcinfo_obj)
        output_file = self.options_obj.output_file % tcid
        msg = (
            f"Writing netCDF-formatted output file {output_file} for TC "
            f"event {tcid}."
        )
        self.logger.info(msg=msg)

        # Build the netCDF-formatted file output fields.
        ncvarlist = []
        ncvarlist.append(
            xarray.DataArray(
                tcinfo_obj.wnds10m.varout,
                coords=coords_2d,
                dims=coords_2d.keys(),
                attrs=self.diagsvar_obj.wnds10m,
            ).to_dataset(name="wnds10m")
        )
        varout = numpy.zeros(
            (tcinfo_obj.ncoeffs, tcinfo_obj.wnds10m.nrho, tcinfo_obj.wnds10m.nphi)
        )
        for coeff in range(tcinfo_obj.ncoeffs):
            varout[coeff, :, :] = parser_interface.object_getattr(
                object_in=tcinfo_obj.wndspec, key=f"wn{coeff}"
            ).magnitude
        ncvarlist.append(
            xarray.DataArray(
                varout,
                coords=coords_3d,
                dims=coords_3d.keys(),
                attrs=self.NCOUT_ATTRS,
            ).to_dataset(name="wnds10m_spec")
        )

        # Update the netCDF-formatted file global-attributes.
        attrs_dict = {}
        for ncvar in vars(tcinfo_obj).keys():
            attr_info = parser_interface.object_getattr(object_in=tcinfo_obj, key=ncvar)
            if not isinstance(attr_info, SimpleNamespace):
                try:
                    attrs_dict[f"{ncvar}"] = attr_info._magnitude
                except AttributeError:
                    attrs_dict[f"{ncvar}"] = attr_info

        # Write the netCDF-formatted file.
        ncfile = xarray.merge(ncvarlist).assign_attrs(attrs_dict)
        ncfile.to_netcdf(output_file)

    def run(self: Diagnostics) -> SimpleNamespace:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Defines the respective TC-centric polar projection for the
        10-meter total wind field magnitudes.

        (2) Computes the wavenumber spectrum for the respective TC
        event.

        (3) Computes the TC event MSI and writes the results to a
        corresponding file path.

        Returns
        -------

        tcmsi_obj: SimpleNamespace

            A Python SimpleNamespace object containing the relevant TC
            event MSI attributes.

        """

        # Compute the 10-meter wind field.
        self.tcmsi_obj.lats = self.tcdiags_obj.inputs.latitude.values._magnitude
        self.tcmsi_obj.lons = self.tcdiags_obj.inputs.longitude.values._magnitude
        asyncio.run(self.compute_inputs())
        self.tcmsi_obj.wnds = self.tcmsi_obj.wnds10m.values
        self.tcmsi_obj = parser_interface.object_setattr(
            object_in=self.tcmsi_obj,
            key="tcids",
            value=list(self.tcdiags_obj.tcinfo.keys()),
        )

        # Compute the multi-scale intensity index attributes for each
        # TC event.
        for tcid in self.tcdiags_obj.tcinfo:
            tcinfo_obj = parser_interface.dict_toobject(
                in_dict=parser_interface.dict_key_value(
                    dict_in=self.tcdiags_obj.tcinfo, key=tcid, no_split=True
                )
            )
            tcinfo_obj = self.interp_ll2ra(tcinfo_obj=tcinfo_obj)
            tcinfo_obj = self.specanly(tcinfo_obj=tcinfo_obj)
            tcinfo_obj = self.compute_msi(tcinfo_obj=tcinfo_obj)

            # Write the tables containing the MSI attributes and the
            # netCDF-formatted output file for the respective TC
            # event.
            self.build_tables(tcinfo_obj=tcinfo_obj, tcid=tcid)
            if self.options_obj.write_output:
                self.write_polar_output(tcinfo_obj=tcinfo_obj, tcid=tcid)
            self.tcmsi_obj = parser_interface.object_setattr(
                object_in=self.tcmsi_obj, key=tcid, value=tcinfo_obj
            )

        return self.tcmsi_obj
