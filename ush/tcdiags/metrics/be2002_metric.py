# =========================================================================

# Module: ush/tcdiags/metrics/be2002_metric.py

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

    be2002_metric.py

Description
-----------

    This module contains the base-class object for tropical cyclone
    (TC) potential intensity application.

Classes
-------

    TropCycMPI(yaml_dict, inputs_obj)

        This is the base-class object for all tropical cyclone (TC)
        potential intensity (PI) computations following Bister and
        Emanuel [2002] and via the software provided by Gifford,
        D. M., [2020]; it is a sub-class of Metrics.

Requirements
------------

- tcpyPI; https://github.com/dgilford/tcpyPI

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

References
----------

    Bister, M., and K. A. Emanuel. "Low frequency variability of
    tropical cyclone potential intensity, 1, Interannual to
    interdecadal variability". Journal of Geophysical Research 107
    (2002): 4801.

    Gifford, D. M., "pyPI(v1.3): Tropical cyclone potential intensity
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

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from types import SimpleNamespace

import numpy
from metpy.units import units
from tcdiags.io.nc_write import NCWrite
from tcdiags.metrics.metrics import Metrics
from tcpyPI import pi
from tools import parser_interface
from utils.decorator_interface import privatemethod

# ----


class BE2002(Metrics):
    """ "
    Description
    -----------

    This is the base-class object for all tropical cyclone(TC)
    potential intensity(PI) computations following Bister and Emanuel
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

    def __init__(self: Metrics, tcdiags_obj: SimpleNamespace):
        """
        Description
        -----------

        Creates a new TropCycMPI object.

        """

        # Define the base-class attributes.
        super().__init__(tcdiags_obj=tcdiags_obj)

        self.tcpi_obj = parser_interface.object_define()

        # TODO: /begin

        # The following should be evaluated via the schema interface
        # and updated accordingly.

        # Define the experiment configuration variables.
        self.tcmpi_var_dict = {
            "mslp_max": 2000.0,
            "output_file": "tcmpi.nc",
            "zmax": 10.0,
        }  # NEED TO UPDAT THIS USING DEFAULT DICTIONARY

        # Define the local variables.
        self.tcpi_obj.zmax = 10.0

        # TODO: /end

        # Define the array dimension attributes.
        (self.nx, self.ny) = [
            self.tcdiags_obj.inputs.latitude.values.shape[1],
            self.tcdiags_obj.inputs.latitude.values.shape[0],
        ]
        self.ndim = self.nx * self.ny
        self.nlevs = self.tcdiags_obj.inputs.temperature.values.shape[0]

        lat = numpy.array(self.tcdiags_obj.inputs.latitude.values)[:, 0]
        level = numpy.arange(0.0, self.nlevs)
        lon = (
            numpy.array(self.tcdiags_obj.inputs.longitude.values)[0, :]
            - self.tcdiags_obj.inputs.longitude.scale_add
        )

        # Build and define the CF compliant dimensions.
        self.tcpi_obj.dims2d = {"lat": (["lat"], lat), "lon": (["lon"], lon)}
        self.tcpi_obj.dims3d = {
            "lev": (["lev"], level),
            "lat": (["lat"], lat),
            "lon": (["lon"], lon),
        }

        # Define the output variables list.
        self.output_varlist = [
            "mxrt",
            "pmin",
            "pout",
            "pres",
            "pslp",
            "temp",
            "tout",
            "vmax",
            "zsfc",
        ]

    @privatemethod
    def compute(self: Metrics) -> None:
        """
        Description
        -----------

        This method computes the TC potential intensity metrics.

        """

        # Initialize the TC potential intensity metric arrays.
        msg = "Computing the tropical cyclone maximum potential intensity metrics."
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
    def get_inputs(self: Metrics) -> None:
        """
        Description
        -----------

        This method computes, updates the units in accordance with the
        TC MPI application, and updates the base-class object
        `tcpi_obj` accordingly.

        """

        # Compute/define the input variables.
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
            self.tcdiags_obj.inputs.pslp.values.ravel(), "hectopascal"
        )
        self.tcpi_obj.temp = units.Quantity(
            numpy.reshape(
                self.tcdiags_obj.inputs.temperature.values, (self.nlevs, self.ndim)
            ),
            "celsius",
        )
        self.tcpi_obj.sstc = units.Quantity(
            self.tcdiags_obj.inputs.temperature.values[0, ...].ravel(), "celsius"
        )
        self.tcpi_obj.zsfc = units.Quantity(
            self.tcdiags_obj.inputs.surface_height.values.ravel(), "meters"
        )

    def tcpi(self: Metrics, idx: int) -> None:
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
        if zsfc <= self.tcpi_obj.zmax:

            msl = self.tcpi_obj.pslp.magnitude[idx]
            mxrt = self.tcpi_obj.mxrt.magnitude[:, idx]
            pres = self.tcpi_obj.pres.magnitude[:, idx]
            sstc = self.tcpi_obj.temp.magnitude[0, idx]
            tempc = self.tcpi_obj.temp.magnitude[:, idx]

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
    def update_units(self: Metrics) -> None:
        """
        Description
        -----------

        This method updates the respective TC potential intensity
        input and output variable array units within the base-class
        attribute `tcpi_obj`.

        """

        # Update the respective TC potential intensity input and
        # output array units for output.
        self.tcpi_obj.pmin.values = units.Quantity(
            numpy.reshape(self.tcpi_obj.pmin.values, (self.ny, self.nx)), "pascal"
        )
        self.tcpi_obj.pmin.attrs = {
            "units": "pascal",
            "name": "potential intensity sea-level pressure",
        }

        self.tcpi_obj.pout.values = units.Quantity(
            numpy.reshape(self.tcpi_obj.pout.values, (self.ny, self.nx)), "pascal"
        )
        self.tcpi_obj.pout.attrs = {
            "units": "pascal",
            "name": "potential intensity outflow pressure level",
        }

        self.tcpi_obj.tout.values = units.Quantity(
            numpy.reshape(self.tcpi_obj.tout.values, (self.ny, self.nx)), "kelvin"
        )
        self.tcpi_obj.tout.attrs = {
            "units": "kelvin",
            "name": "potential intensity outflow temperature",
        }

        self.tcpi_obj.vmax.values = units.Quantity(
            numpy.reshape(self.tcpi_obj.vmax.values, (self.ny, self.nx)), "mps"
        )
        self.tcpi_obj.vmax.attrs = {
            "units": "meter_per_second",
            "name": "potential intensity surface wind speed",
        }

        self.tcpi_obj.mxrt = self.tcdiags_obj.inputs.mixing_ratio
        self.tcpi_obj.mxrt.attrs = {"units": "kg/kg", "name": "mixing ratio"}

        self.tcpi_obj.pres = self.tcdiags_obj.inputs.pressure
        self.tcpi_obj.pres.attrs = {"units": "pascal", "name": "pressure"}

        self.tcpi_obj.pslp = self.tcdiags_obj.inputs.pslp
        self.tcpi_obj.pslp.attrs = {"units": "pascal", "name": "sea-level pressure"}

        self.tcpi_obj.temp = self.tcdiags_obj.inputs.temperature
        self.tcpi_obj.temp.attrs = {"units": "kelvin", "name": "temperature"}

        self.tcpi_obj.zsfc = self.tcdiags_obj.inputs.surface_height
        self.tcpi_obj.zsfc.attrs = {"units": "meter", "name": "surface height"}

    @privatemethod
    def write_output(self: Metrics) -> None:
        """
        Description
        -----------

        This method writes a netCDF-formatted file containing the TC
        MPI computed values as well as the diagostics/inputs
        quantities for the TC MPI application.

        """

        # Define the netCDF output object and write the respective
        # variables to the external netCDF-formatted file path.
        ncwrite = NCWrite(output_file=self.tcdiags_obj.tcmpi.output_file)

        ncwrite.write(
            var_obj=self.tcpi_obj,
            var_list=self.output_varlist,
            coords_3d=self.tcpi_obj.dims3d,
            coords_2d=self.tcpi_obj.dims2d,
        )

    def run(self: Metrics) -> None:
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

        """

        # Collect and define/compute the TC potential intensity input
        # fields.
        self.get_inputs()

        # Compute the TC MPI following Bister and Emanuel [2002].
        self.compute()

        # Update the units for the respective TC potential intensity
        # metrics.
        self.update_units()

        # Write the computed values and diagnostics/inputs quantities
        # to the specified netCDF-formatted output file.
        self.write_output()
