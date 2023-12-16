"""
Module
------

    be2002_pi.py

Description
-----------

    This module contains the base-class object for tropical cyclone
    (TC) potential intensity application.

Classes
-------

    BE2002(tcdiags_obj)

        This is the base-class object for all tropical cyclone (TC)
        potential intensity (PI) computations following Bister and
        Emanuel [2002] and via the software provided by Gifford,
        D. M., [2020]; it is a sub-class of Metrics.

Requirements
------------

- tcpyPI; https://github.com/dgilford/tcpyPI

- ufs_pyutils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

References
----------

    Bister, M., and K. A. Emanuel. "Low frequency variability of
    tropical cyclone potential intensity, 1, Interannual to
    interdecadal variability". Journal of Geophysical Research 107
    (2002): 4801.

    Gifford, D. M., "pyPI (v1.3): Tropical cyclone potential intensity
    calculations in Python". Geoscientific Model Development 14
    (2020): 2351-2369.

Author(s)
---------

    Henry R. Winterbottom; 13 March 2023

History
-------

    2023-03-13: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=expression-not-assigned
# pylint: disable=fixme
# pylint: disable=invalid-name
# pylint: disable=too-many-instance-attributes

# ----

import asyncio

from types import SimpleNamespace

import numpy
from metpy.units import units
from tcpyPI import pi
from tools import parser_interface
from utils.decorator_interface import privatemethod

from tcdiags.diagnostics import Diagnostics

# ----


class BE2002(Diagnostics):
    """
    Description
    -----------

    This is the base-class object for all tropical cyclone (TC)
    potential intensity (PI) computations following Bister and Emanuel
    [2002] and via the software provided by Gifford, D. M., [2020]; it
    is a sub-class of Metrics.

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

    Bister, M., and K. A. Emanuel. "Low frequency variability of
    tropical cyclone potential intensity, 1, Interannual to
    interdecadal variability". Journal of Geophysical Research 107
    (2002): 4801.

    DOI: https://doi.org/10.1029/2001JD000776

    Gifford, D. M., "pyPI(v1.3): Tropical cyclone potential intensity
    calculations in Python". Geoscientific Model Development 14
    (2020): 2351-2369.

    DOI: https://doi.org/10.5194/gmd-14-2351-2021

    """

    def __init__(self: Diagnostics, tcdiags_obj: SimpleNamespace):
        """
        Description
        -----------

        Creates a new TropCycMPI object.

        """

        # Define the base-class attributes.
        super().__init__(tcdiags_obj=tcdiags_obj, app="tcpi")
        self.output_varlist = list(self.options_obj.output_varlist.keys())
        self.tcpi_obj = parser_interface.object_define()
        (self.nx, self.ny) = [
            self.tcdiags_obj.inputs.latitude.values.shape[1],
            self.tcdiags_obj.inputs.latitude.values.shape[0],
        ]
        self.ndim = self.nx * self.ny
        self.nlevs = self.tcdiags_obj.inputs.temperature.values.shape[0]
        self.tcpi_obj.dims = {
            "lev": (["lev"], numpy.arange(0.0, float(self.nlevs))),
            "lat": (
                ["lat"],
                numpy.array(self.tcdiags_obj.inputs.latitude.values)[:, 0],
            ),
            "lon": (
                ["lon"],
                numpy.array(self.tcdiags_obj.inputs.longitude.values)[0, :]
                - self.tcdiags_obj.inputs.longitude.scale_add,
            ),
        }
        self.ncio = self.write_output

    @privatemethod
    async def compute(self: Diagnostics) -> None:
        """
        Description
        -----------

        This method computes the TC potential intensity metrics.

        """

        # Initialize the TC potential intensity metric arrays.
        msg = "Computing the tropical cyclone potential intensity metrics."
        self.logger.info(msg=msg)
        (
            self.tcpi_obj.vmax,
            self.tcpi_obj.pmin,
            self.tcpi_obj.tout,
            self.tcpi_obj.pout,
        ) = [parser_interface.object_define() for idx in range(4)]
        (
            self.tcpi_obj.vmax.values,
            self.tcpi_obj.pmin.values,
            self.tcpi_obj.tout.values,
            self.tcpi_obj.pout.values,
        ) = [numpy.empty(self.ndim) for idx in range(4)]

        # Compute the TC potential intensity metrics; proceed
        # accordingly.
        [self.tcpi(idx=idx) for idx in range(self.ndim)]

    @privatemethod
    def get_inputs(self: Diagnostics) -> None:
        """
        Description
        -----------

        This method computes, updates the units in accordance with the
        TC MPI application, and updates the base-class object
        `tcpi_obj` accordingly.

        """

        # Define the input variables.
        self.tcpi_obj.mxrt = units.Quantity(
            numpy.reshape(
                self.tcdiags_obj.inputs.mixing_ratio.values, (self.nlevs, self.ndim)
            ),
            "gram/gram",
        )
        self.tcpi_obj.pres = units.Quantity(
            numpy.reshape(
                self.tcdiags_obj.inputs.pressure.values, (self.nlevs, self.ndim)
            ),
            "hectopascal",
        )
        self.tcpi_obj.pslp = units.Quantity(
            self.tcdiags_obj.inputs.sea_level_pressure.values.ravel(), "hectopascal"
        )
        self.tcpi_obj.temp = units.Quantity(
            numpy.reshape(
                self.tcdiags_obj.inputs.temperature.values, (self.nlevs, self.ndim)
            ),
            "celsius",
        )
        # TODO: Define the SST at the I/O level;
        self.tcpi_obj.sstc = units.Quantity(
            self.tcdiags_obj.inputs.temperature.values[0, ...].ravel(), "celsius"
        )
        self.tcpi_obj.zsfc = units.Quantity(
            self.tcdiags_obj.inputs.surface_height.values.ravel(), "meters"
        )
        self.tcpi_obj.lats = units.Quantity(
            self.tcdiags_obj.inputs.latitude.values, "degrees"
        )
        self.tcpi_obj.lons = units.Quantity(
            self.tcdiags_obj.inputs.longitude.values, "degrees"
        )

    def tcpi(self: Diagnostics, idx: int) -> None:
        """
        Description
        -----------

        This method computes the tropical cyclone (TC) (maximum)
        potential intensity (MPI) assuming the methodology of Bister
        and Emanuel [1997] and the application described within
        Gifford, D. M., [2020]; the base-class variables are used and
        updated accordingly.

        Parameters
        ----------

        idx: int

            A Python integer defining the grid index for which to
            compute the TC MPI.

        """

        # Compute the TC potential intensity; the base-class object
        # `tcpi` contains the respective TC potential intensity
        # indices; proceed accordingly.
        zsfc = self.tcpi_obj.zsfc.magnitude[idx]
        if zsfc <= self.options_obj.zmax:
            msl = float(self.tcpi_obj.pslp.magnitude[idx])
            mxrt = numpy.array(self.tcpi_obj.mxrt.magnitude[:, idx])
            pres = numpy.array(self.tcpi_obj.pres.magnitude[:, idx])
            sstc = numpy.array(self.tcpi_obj.temp.magnitude[0, idx])
            tempc = numpy.array(self.tcpi_obj.temp.magnitude[:, idx])
            (
                self.tcpi_obj.vmax.values[idx],
                self.tcpi_obj.pmin.values[idx],
                _,
                self.tcpi_obj.tout.values[idx],
                self.tcpi_obj.pout.values[idx],
            ) = pi(SSTC=sstc, MSL=msl, P=pres, TC=tempc, R=mxrt)
        else:
            (
                self.tcpi_obj.vmax.values[idx],
                self.tcpi_obj.pmin.values[idx],
                self.tcpi_obj.tout.values[idx],
                self.tcpi_obj.pout.values[idx],
            ) = [numpy.nan for idx in range(4)]

    @privatemethod
    def update_units(self: Diagnostics) -> None:
        """
        Description
        -----------

        This method updates the respective TC potential intensity
        input and output variable array units within the base-class
        attribute `tcpi_obj`.

        """

        # Update the respective TC potential intensity input and
        # output array units for output.
        diagvars_obj = parser_interface.dict_toobject(
            in_dict=self.options_obj.output_varlist
        )

        self.tcpi_obj.pmin.values = units.Quantity(
            numpy.reshape(self.tcpi_obj.pmin.values, (self.ny, self.nx)), "pascal"
        )
        self.tcpi_obj.pmin.attrs = diagvars_obj.pmin
        self.tcpi_obj.pout.values = units.Quantity(
            numpy.reshape(self.tcpi_obj.pout.values, (self.ny, self.nx)), "pascal"
        )
        self.tcpi_obj.pout.attrs = diagvars_obj.pout
        self.tcpi_obj.tout.values = units.Quantity(
            numpy.reshape(self.tcpi_obj.tout.values, (self.ny, self.nx)), "kelvin"
        )
        self.tcpi_obj.tout.attrs = diagvars_obj.tout
        self.tcpi_obj.vmax.values = units.Quantity(
            numpy.reshape(self.tcpi_obj.vmax.values, (self.ny, self.nx)), "mps"
        )
        self.tcpi_obj.vmax.attrs = diagvars_obj.vmax
        self.tcpi_obj.mxrt.values = self.tcdiags_obj.inputs.mixing_ratio.values
        self.tcpi_obj.mxrt.attrs = diagvars_obj.mxrt
        self.tcpi_obj.pres.values = self.tcdiags_obj.inputs.pressure.values
        self.tcpi_obj.pres.attrs = diagvars_obj.pres
        self.tcpi_obj.pslp.values = self.tcdiags_obj.inputs.sea_level_pressure.values
        self.tcpi_obj.pslp.attrs = diagvars_obj.pslp
        self.tcpi_obj.temp.values = self.tcdiags_obj.inputs.temperature.values
        self.tcpi_obj.temp.attrs = diagvars_obj.temp
        self.tcpi_obj.zsfc.values = self.tcdiags_obj.inputs.surface_height.values
        self.tcpi_obj.zsfc.attrs = diagvars_obj.zsfc
        self.tcpi_obj.lats = self.tcpi_obj.dims["lat"][1]
        self.tcpi_obj.lons = self.tcpi_obj.dims["lon"][1]

    def run(self: Diagnostics) -> SimpleNamespace:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Collects and defines/computes the inputs for the TC
            potential intensity metrics.

        (2) Computes the TC potential intensity in accordance with the
            formulation of Gifford, D. M., [2002].

        (3) Updates the units for the respective inputs and TC
            potential intensity metrics prior to netCDF-formatted file
            path creation.

        (4) Writes the TC MPI attributes to the specified output
            netCDF-formatted file path.

        Keywords
        --------

        write_output: bool, optional

            A Python boolean valued variable specifying whether to
            write the output from the computed metric(s) to the
            specified external netCDF-formatted file path.

        Returns
        -------

        tcpi_obj: SimpleNamespace

            A Python SimpleNamespace object containing the relevant TC
            potential intensity attributes.

        """

        # Collect and define/compute the TC potential intensity input
        # fields.
        self.get_inputs()

        # Compute the TC MPI following Bister and Emanuel [2002].
        asyncio.run(self.compute())

        # Update the units for the respective TC potential intensity
        # metrics.
        self.update_units()

        # Write the computed values and diagnostics/inputs quantities
        # to the specified netCDF-formatted output file.
        if self.options_obj.write_output:
            self.ncio(
                output_file=self.options_obj.output_file,
                var_obj=self.tcpi_obj,
                var_list=self.output_varlist,
                coords_2d={
                    "lat": self.tcpi_obj.lats,
                    "lon": self.tcpi_obj.lons,
                },
                coords_3d=self.tcpi_obj.dims,
            )

        return self.tcpi_obj
