# =========================================================================

# Module: ush/tcdiags/metrics/tropcycmpi.py

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

    tropcycmpi.py

Description
-----------

    This module contains the base-class object for tropical cyclone
    (TC) (maximum) potential intensity application.

Classes
-------

    TropCycMPI(yaml_dict, inputs_obj)

        This is the base-class object for all tropical cyclone (TC)
        (maximum) potential intensity (MPI) computations following
        Bister and Emanuel [2002].

Requirements
------------

- tcpyPI; https://github.com/dgilford/tcpyPI

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

References
----------

    Bister, M., and Emanuel, K. A., Low frequency variability of
    tropical cyclone potential intensity, 1, Interannual to
    interdecadal variability, J. Geophys. Res., 107( D24), 4801,
    doi:10.1029/2001JD000776, 2002.

Author(s)
---------

    Henry R. Winterbottom; 13 March 2023

History
-------

    2023-03-13: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=expression-not-assigned
# pylint: disable=too-many-instance-attributes
# pylint: disable=invalid-name
# pylint: disable=no-member

# ----

from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict

import numpy
from metpy.units import units
from tcdiags.atmos import moisture, pressures
from tcdiags.io.outputs import TCDiagsOutputsNetCDFIO
from tcpyPI import pi
from tools import parser_interface
from utils.logger_interface import Logger

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


@dataclass
class TropCycMPI:
    """
    Description
    -----------

    This is the base-class object for all tropical cyclone (TC)
    (maximum) potential intensity (MPI) computations following Bister
    and Emanuel [2002].

    Parameters
    ----------

    yaml_dict: dict

        A Python dictionary containing the attributes from the
        experiment configuration file; the TC MPI application
        configuration values are contained in the YAML-formatted file
        path denoted by the `tcmpi` attribute in the experiment
        configuration.

    inputs_obj: object

        A Python object containing the mandatory input variables.

    """

    def __init__(self, yaml_dict: Dict, inputs_obj: object):
        """
        Description
        -----------

        Creates a new TropCycMPI object.

        """

        # Define the base-class attributes.
        self.logger = Logger()
        self.inputs_obj = inputs_obj
        self.yaml_dict = yaml_dict

        self.tcmpi_obj = parser_interface.object_define()
        self.tcmpi_var_list = ["mslp", "pout", "tout", "vmax"]

        # Define the experiment configuration variables.
        self.tcmpi_var_dict = {
            "mslp_max": 2000.0,
            "output_file": "tcmpi.nc",
            "zmax": 10.0
        }

        # Define the array dimension attributes.
        (self.nx, self.ny) = [
            self.inputs_obj.lat.shape[1],
            self.inputs_obj.lat.shape[0],
        ]
        self.ndim = self.nx * self.ny

        self.nlevs = self.inputs_obj.temp.shape[0]

        # Initialize the local variables.
        (self.mslp, self.vmax, self.tout, self.pout) = [
            numpy.empty(self.ndim) for idx in range(4)
        ]

        # Compute the input variables.
        self.compute_inputs()

        # Define the local variables.
        self.define_locals()

        # Define the configuration variables.
        self.init_config()

        # Build the dimensional and CF compliant dimensions.
        self.coords_2d = OrderedDict(
            {
                "lat": (["lat"], numpy.array(self.inputs_obj.lat)[:, 0]),
                "lon": (["lon"], numpy.array(self.inputs_obj.lon)[0, :]),
            }
        )

        self.coords_3d = OrderedDict(
            {
                "level": (["level"], numpy.arange(0, self.nlevs)),
                "lat": (["lat"], numpy.array(self.inputs_obj.lat)[:, 0]),
                "lon": (["lon"], numpy.array(self.inputs_obj.lon)[0, :]),
            }
        )

        # Define the output variables list.
        self.output_varlist = [
            "mslp",
            "mxrt",
            "pout",
            "pres",
            "pslp",
            "temp",
            "tout",
            "vmax",
            "zsfc",
        ]

    def define_locals(self) -> None:
        """
        Description
        -----------

        This method defines the input variables for the tropical
        cyclone maximum potential intensity calculations.

        """

        # Initialize the input variable arrays for the tropical
        # cyclone maximum potential intensity calculation.
        self.sstc = numpy.array(self.inputs_obj.temp)[0, :, :].ravel()
        self.slp = numpy.array(self.tcmpi_obj.pslp).ravel()
        self.mxrt = numpy.reshape(
            numpy.array(
                self.tcmpi_obj.mxrt), (self.tcmpi_obj.mxrt.shape[0], self.ndim)
        )
        self.pres = numpy.reshape(
            numpy.array(
                self.tcmpi_obj.pres), (self.tcmpi_obj.pres.shape[0], self.ndim)
        )
        self.temp = numpy.reshape(
            numpy.array(
                self.tcmpi_obj.temp), (self.tcmpi_obj.temp.shape[0], self.ndim)
        )
        self.zsfc = numpy.array(self.inputs_obj.zsfc).ravel()

    def init_config(self) -> None:
        """
        Description
        -----------

        This method defines the base-class attribute values collected
        from the experiment configuration variables.

        """

        # Check the configuration file for the respective
        # configuration variables; proceed accordingly.
        for tcmpi_var in self.tcmpi_var_dict:

            value = parser_interface.dict_key_value(
                dict_in=self.yaml_dict, key=tcmpi_var, force=True, no_split=True
            )

            # Use the default value assigned in the constructor.
            if value is None:
                value = parser_interface.dict_key_value(
                    dict_in=self.tcmpi_var_dict,
                    key=tcmpi_var,
                    force=True,
                    no_split=None,
                )

                msg = (
                    f"Setting configuration variable {tcmpi_var} to default value "
                    f"{value}."
                )
                self.logger.warn(msg=msg)

            # Update the base-class object.
            self.tcmpi_obj = parser_interface.object_setattr(
                object_in=self.tcmpi_obj, key=tcmpi_var, value=value
            )

    def compute_inputs(self) -> None:
        """
        Description
        -----------

        This method computes, updates the units in accordance with the
        TC MPI application, and updates the base-class object
        `tcmpi_obj` accordingly.

        """

        # Compute the input variables.
        self.tcmpi_obj = moisture.spfh_to_mxrt(inputs_obj=self.inputs_obj)
        self.tcmpi_obj = pressures.pressure_to_sealevel(
            inputs_obj=self.inputs_obj)

        # Update the input variable units accordingly.
        self.tcmpi_obj.pslp = units.Quantity(
            self.inputs_obj.pslp, "hectopascal")
        self.tcmpi_obj.pres = units.Quantity(
            self.inputs_obj.pres, "hectopascal")
        self.tcmpi_obj.temp = units.Quantity(self.inputs_obj.temp, "celsius")

    def compute_tcmpi(self) -> None:
        """
        Description
        -----------

        This function computes the TC MPI in accordance with Bister
        and Emanuel [2002] and the Python package described in
        Gifford, D. M., [2020]; the TC MPI variables are scaled
        accordingly and the base-class object attributes are updated
        and assigned the appropriate units accordingly.

        """

        # Compute the tropical cyclone maximum potential intensity
        # attributes.
        msg = ("Computing the tropical cyclone maximum potential intensity "
               "metrics."
               )
        self.logger.info(msg=msg)
        [self.tcpi(idx=idx) for idx in range(self.ndim)]

        # Define the units for the respective varaiables.
        self.mslp = units.Quantity(self.mslp, "hectopascal")
        self.pout = units.Quantity(self.pout, "hectopascal")
        self.tout = units.Quantity(self.tout, "celsius")
        self.vmax = units.Quantity(self.vmax, "mps")

        # Define the base-class attribute values.
        self.tcmpi_obj = parser_interface.object_setattr(
            object_in=self.tcmpi_obj, key="mslp", value=self.mslp
        )
        self.tcmpi_obj.mslp = numpy.reshape(
            self.tcmpi_obj.mslp, (self.ny, self.nx))
        self.tcmpi_obj.mslp = units.Quantity(self.tcmpi_obj.mslp, "pascal")

        self.tcmpi_obj = parser_interface.object_setattr(
            object_in=self.tcmpi_obj, key="pout", value=self.pout
        )
        self.tcmpi_obj.pout = numpy.reshape(
            self.tcmpi_obj.pout, (self.ny, self.nx))
        self.tcmpi_obj.pout = units.Quantity(self.tcmpi_obj.pout, "pascal")

        self.tcmpi_obj = parser_interface.object_setattr(
            object_in=self.tcmpi_obj, key="tout", value=self.tout
        )
        self.tcmpi_obj.tout = numpy.reshape(
            self.tcmpi_obj.tout, (self.ny, self.nx))
        self.tcmpi_obj.tout = units.Quantity(self.tcmpi_obj.tout, "kelvin")

        self.tcmpi_obj = parser_interface.object_setattr(
            object_in=self.tcmpi_obj, key="vmax", value=self.vmax
        )
        self.tcmpi_obj.vmax = numpy.reshape(
            self.tcmpi_obj.vmax, (self.ny, self.nx))

        # Correct the units for output.
        self.tcmpi_obj.pres = units.Quantity(self.tcmpi_obj.pres, "pascal")
        self.tcmpi_obj.temp = units.Quantity(self.tcmpi_obj.temp, "kelvin")

        for tcmpi_var in self.tcmpi_var_list:
            value = parser_interface.object_getattr(
                object_in=self.tcmpi_obj, key=tcmpi_var)

            msg = (f"The tropical cyclone metric {tcmpi_var} range values: "
                   f"({numpy.nanmin(numpy.array(value))}, {numpy.nanmax(numpy.array(value))}) "
                   f"{value.units}."
                   )
            self.logger.debug(msg=msg)

    def tcpi(self, idx: int) -> None:
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

        # Compute the TC MPI only for near-ocean locations; assign NaN
        # otherwise.
        if self.zsfc[idx] <= self.tcmpi_obj.zmax:

            (self.vmax[idx], self.mslp[idx], _, self.tout[idx], self.pout[idx]) = pi(
                SSTC=self.sstc[idx],
                MSL=self.slp[idx],
                P=self.pres[:, idx],
                TC=self.temp[:, idx],
                R=self.mxrt[:, idx],
            )

        else:

            (self.vmax[idx], self.mslp[idx], self.tout[idx], self.pout[idx]) = [
                numpy.nan for count in range(4)
            ]

    def write_output(self) -> None:
        """
        Description
        -----------

        This method writes a netCDF-formatted file containing the TC
        MPI computed values as well as the diagostics/inputs
        quantities for the TC MPI application.

        """

        # Write the netCDF-formatted file path containing the TC MPI
        # attributes.
        tcdiags_out = TCDiagsOutputsNetCDFIO(
            output_file=self.tcmpi_obj.output_file)

        tcdiags_out.write(
            var_obj=self.tcmpi_obj,
            var_list=self.output_varlist,
            coords_3d=self.coords_3d,
            coords_2d=self.coords_2d,
            attrs_list=["units"],
        )

    def run(self) -> None:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Computes the TC MPI in accordance with experiment
            configuration.

        (2) Writes the TC MPI attributes to the specified output
            netCDF-formatted file path.

        """

        # Compute the TC MPI following Bister and Emanuel [2002].
        self.compute_tcmpi()

        # Write the computed values and diagnostics/inputs quantities
        # to the specified netCDF-formatted output file.
        self.write_output()
