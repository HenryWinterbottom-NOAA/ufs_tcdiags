"""
Module
------

    lv1972_ohc.py

Description
-----------

    This module contains the base-class object for tropical cyclone
    heat potential (TCHP) computation following the application
    described in Liepper and Volgenau [1972].

Classes
-------

    LV1972(tcdiags_obj)

        This is the base-class object for all tropical cyclone (TC)
        heat-potential computations following Liepper and Volgenau
        [1972]; it is a sub-class of ``Diagnostics``.

Requirements
------------

- ufs_pyutils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

References
----------

    Leipper, D. F., and D. Volgenau. "Hurricane heat potential of the
    Gulf of Mexico". J. Phys. Oceanpgr. 2, 218–224.

Author(s)
---------

    Henry R. Winterbottom; 07 December 2023

History
-------

    2023-12-07: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=fixme
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=unused-argument

# ----

import asyncio
from types import SimpleNamespace
from typing import Dict, Tuple

import numpy
from diags.derived.ocean.depths import isodepth
from diags.derived.ocean.heatcontent import total_heat_content
from diags.derived.ocean.salinity import absolute_from_practical
from diags.derived.ocean.temperatures import conservative_from_potential
from metpy.units import units
from scipy.interpolate import interp1d
from tools import parser_interface
from utils.decorator_interface import privatemethod

from tcdiags.diagnostics import Diagnostics
from tcdiags.io.ncwrite import ncwrite

# ----

# Define all available module properties.
__all__ = ["LV1972"]

# ----


class LV1972(Diagnostics):
    """
    Description
    -----------

    This is the base-class object for all tropical cyclone (TC)
    heat-potential computations following Liepper and Volgenau [1972];
    it is a sub-class of ``Diagnostics``.

    Parameters
    ----------

    tcdiags_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing all configuration
        attributes for the respective application including inputs
        (i.e., `inputs` and `tcinfo`) as well as the remaining
        (supported) applications (see base-class attribute
        `apps_list`).

    Other Parameters
    ----------------

    args: ``Tuple``

        A Python tuple containing additional arguments passed to the
        constructor.

    kwargs: ``Dict``

        A Python dictionary containing additional key and value pairs
        to be passed to the constructor.

    References
    ----------

    Leipper, D. F., and D. Volgenau. "Hurricane heat potential of the
    Gulf of Mexico". J. Phys. Oceanpgr. 2, 218–224.

    DOI: https://doi.org/10.1175/1520-0485(1972)002<0218:HHPOTG>2.0.CO;2

    """

    def __init__(
        self: Diagnostics, tcdiags_obj: SimpleNamespace, *args: Tuple, **kwargs: Dict
    ):
        """
        Description
        -----------

        Creates a new LV1972 object.

        """

        # Define the base-class attributes.
        super().__init__(tcdiags_obj=tcdiags_obj, app="tcohc")

    @privatemethod
    async def compute(self: Diagnostics, tchp_obj: SimpleNamespace) -> SimpleNamespace:
        """
        Description
        -----------

        This method computes the gridded tropical cyclone heat
        potential relative to the specified isotherm depth and the
        ocean heat content.

        Parameters
        ----------

        tchp_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the attributes
            required of the TCHP computation.

        Returns
        -------

        tchp_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the TCHP and
            isotherm depth array values.

        """

        # Compute the depth of the specified isotherm.
        (tchp_obj.isotherm, _) = await isodepth(
            varobj=self.tcdiags_obj.inputs,
            varin=tchp_obj.ctemp.magnitude,
            isolev=self.tcdiags_obj.tcohc.isotherm,
        )
        tchp_obj.isotherm = numpy.ma.where(
            tchp_obj.isotherm <= numpy.nanmax(tchp_obj.isotherm), tchp_obj.isotherm, 0.0
        )
        tchp_obj.isotherm = units.Quantity(tchp_obj.isotherm, "m")
        isotherm = numpy.array(tchp_obj.isotherm).ravel()
        depths = numpy.reshape(
            numpy.array(tchp_obj.depths), (tchp_obj.nz, tchp_obj.nx * tchp_obj.ny)
        )
        ohc = numpy.reshape(
            numpy.array(tchp_obj.ohc), (tchp_obj.nz, tchp_obj.nx * tchp_obj.ny)
        )

        # Compute the TCHP.
        tchp = numpy.empty(numpy.shape(isotherm))
        msg = (
            "Computing the tropical cyclone heat potential relative to the "
            f"{self.tcdiags_obj.tcohc.isotherm}C isotherm."
        )
        self.logger.info(msg=msg)
        tchp = [
            await self.tchp(
                ohc[:, idx],
                isotherm[idx],
                depths[:, idx],
                interp_type=self.tcdiags_obj.tcohc.interp_type,
                fill_value=self.tcdiags_obj.tcohc.fill_value,
                deltaz=self.tcdiags_obj.tcohc.deltaz,
            )
            for idx in range(tchp_obj.nx * tchp_obj.ny)
        ]
        tchp_obj.tchp = units.Quantity(
            numpy.reshape(tchp, numpy.shape(tchp_obj.isotherm)), tchp_obj.ohc.units
        )

        return tchp_obj

    @privatemethod
    async def initialize(self: Diagnostics) -> SimpleNamespace:
        """
        Description
        -----------

        This method initialized the Python SimpleNamespace object
        containing the attributes required to compute the TCHP.

        Returns
        -------

        tchp_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the attributes
            required of the TCHP computation.

        """

        # Initialize the TCHP computation.
        tchp_obj = parser_interface.object_define()
        tchp_obj.lats = units.Quantity(
            self.tcdiags_obj.inputs.latitude.values, "degree"
        )
        tchp_obj.lons = units.Quantity(
            self.tcdiags_obj.inputs.longitude.values, "degree"
        )
        tchp_obj.depths = units.Quantity(self.tcdiags_obj.inputs.depth.values, "m")
        tchp_obj.ohc = await total_heat_content(varobj=self.tcdiags_obj.inputs)
        tchp_obj.ctemp = units.Quantity(
            await conservative_from_potential(varobj=self.tcdiags_obj.inputs), "degC"
        )
        tchp_obj.asaln = units.Quantity(
            await absolute_from_practical(varobj=self.tcdiags_obj.inputs), "g/kg"
        )

        return tchp_obj

    @ncwrite
    async def output(self: Diagnostics, varobj: SimpleNamespace) -> SimpleNamespace:
        """
        Description
        -----------

        This method defines the attributes for the netCDF-formatted
        output file and subsequently writes the specified
        netCDF-formatted output file path.

        Parameters
        ----------

        varobj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the
            netCDF-formatted output file attributes and the respective
            output variable attributes.

        """

        # Define the netCDF-formatted output file attributes and write
        # the netCDF-formatted file path.
        ncout_obj = parser_interface.object_deepcopy(object_in=self.tcdiags_obj.inputs)
        ncout_obj.ncvarlist = list(self.tcdiags_obj.tcohc.output_vars.keys())
        for var in ncout_obj.ncvarlist:
            ncvar = parser_interface.dict_toobject(
                in_dict=parser_interface.dict_key_value(
                    dict_in=self.tcdiags_obj.tcohc.output_vars,
                    key=var,
                    force=True,
                    no_split=True,
                )
            )
            if (
                parser_interface.object_getattr(
                    object_in=ncvar, key="attributes", force=True
                )
                is None
            ):
                ncvar.attributes = {}
            ncvar.values = parser_interface.object_getattr(object_in=varobj, key=var)
            ncvar.attributes["units"] = f"{ncvar.values.units}"
            ncout_obj = parser_interface.object_setattr(
                object_in=ncout_obj, key=var, value=ncvar
            )
        ncout_obj.grid_coords = ["level", "lat", "lon"]
        ncout_obj.ncoutput = self.tcdiags_obj.tcohc.output_file

        return ncout_obj

    async def setup(self: Diagnostics, tchp_obj: SimpleNamespace) -> SimpleNamespace:
        """
        Description
        -----------

        This method defines the netCDF-formatted output file
        attributes.

        Parameters
        ----------

        tchp_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the attributes
            required of the TCHP computation.

        Returns
        -------

        tchp_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the
            netCDF-formatted output file attributes.

        """

        # Define the netCDF-formatted output file attributes.
        tchp_obj.ncoutput = self.tcdiags_obj.tcohc.output_file
        (tchp_obj.nz, tchp_obj.ny, tchp_obj.nx) = numpy.shape(
            numpy.array(tchp_obj.depths)
        )
        tchp_obj.coords_dict = {}
        tchp_obj.coords_dict["level"] = {
            "coord": "z",
            "values": numpy.linspace(
                0, len(numpy.array(self.tcdiags_obj.inputs.depth_profile.values)), 1
            ),
        }
        tchp_obj.coords_dict["lat"] = {
            "coord": "y",
            "values": numpy.array(tchp_obj.lats),
        }
        tchp_obj.coords_dict["lon"] = {
            "coord": "x",
            "values": numpy.array(tchp_obj.lons),
        }

        return tchp_obj

    @staticmethod
    async def tchp(ohc, isodepth, depths, interp_type, fill_value, deltaz) -> float:
        """
        Description
        -----------

        This method computes the tropical cyclone heat potential
        (TCHP) assuming the algorithm described by Liepper and
        Volgenau [1972].

        Parameters
        ----------

        ohc: ``numpy.array``

            A 2-dimensional variable array, ordered as (nz, nx*ny),
            containing the ocean heat content.

        isodepth: ``float``

            A Python float value defining the depth of the isothermal
            level from which to compute the TCHP.

        depths: ``numpy.array``

            A Python 1-dimensional variable array containing the
            vertical levels, increasing with depth.

        Returns
        -------

        tchp: ``float``

            A Python float value containing the integrated TCHP.

        """

        # TODO: Add a minimal depth for which to compute TCHP; i.e.,
        # if anything shallower than `N`, do not compute.

        # Compute the integrated ocean heat content relative to the
        # respective isotherm depth.
        tchp = 0.0
        if isodepth <= numpy.max(depths):
            ohcintrp = interp1d(
                ohc[:], depths[:], kind=interp_type, fill_value=fill_value
            )
            depth = numpy.min(depths[:])
            while depth <= isodepth:
                try:
                    tchp = tchp + ohcintrp(depth)
                except ValueError:
                    break
                depth = depth + deltaz

        return tchp

    def run(self: Diagnostics) -> SimpleNamespace:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Computes the TCHP.

        (2) Optionally writes the specified output variables to the
            specified netCDF-formatted file path.

        """

        # Compute the TCHP and write the specified netCDF-formatted
        # file path.
        tchp_obj = asyncio.run(self.initialize())
        tchp_obj = asyncio.run(self.setup(tchp_obj=tchp_obj))
        tchp_obj = asyncio.run(self.compute(tchp_obj=tchp_obj))
        if self.tcdiags_obj.tcohc.write_output:
            asyncio.run(self.output(varobj=tchp_obj))

        return tchp_obj
