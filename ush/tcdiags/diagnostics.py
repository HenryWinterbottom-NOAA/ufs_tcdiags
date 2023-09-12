"""
Module
------

    diagnostics.py

Description
-----------

    This module contains the base-class object for all tropical
    cyclone (TC) diagnostics/analysis applications.

Classes
-------

    Diagnostics(tcdiags_obj, apps_obj, *args, **kwargs)

        This is the base-class object for all tropical cyclone (TC)
        diagnostics/analysis applications.

    Metrics(tcdiags_obj, apps_obj, *args, **kwargs)

        This is the base-class object for all Metrics sub-classes; it
        is a sub-class of diagnostics.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 18 June 2023

History
-------

    2023-06-18: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=unused-argument

# ----

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Dict, Generic, List, Tuple

from confs.yaml_interface import YAML
from tools import parser_interface
from utils import schema_interface
from utils.decorator_interface import privatemethod
from utils.logger_interface import Logger

from tcdiags.io.nc_write import NCWrite

# ----

# Define all available module properties.
__all__ = ["Diagnostics"]

# ----


class Diagnostics:
    """
    Description
    -----------

    This is the base-class object for all tropical cyclone (TC)
    diagnostics/analysis applications.

    Parameters
    ----------

    tcdiags_obj: SimpleNamespace

        A Python SimpleNamespace object containing all configuration
        attributes for the respective application including inputs
        (i.e., `inputs` and `tcinfo`) as well as the remaining
        (supported) applications.

    app: str

        A Python string specifying the respective sub-class
        application; see `TCDiags` class attribute `app_list`.

    Other Parameters
    ----------------

    args: Tuple

        A Python tuple containing additional arguments passed to the
        constructor.

    kwargs: Dict

        A Python dictionary containing additional key and value pairs
        to be passed to the constructor.

    """

    def __init__(
        self: Generic,
        tcdiags_obj: SimpleNamespace,
        app: str,
        *args: Tuple,
        **kwargs: Dict,
    ):
        """
        Description
        -----------

        Creates a new Diagnostics object.

        """

        # Define the base-class attributes.
        self.logger = Logger(
            caller_name=f"{__name__}.{self.__class__.__name__}")
        self.tcdiags_obj = tcdiags_obj
        cls_schema_file = parser_interface.object_getattr(
            object_in=self.tcdiags_obj, key=app, force=True).schema
        cls_opts = parser_interface.object_todict(
            object_in=parser_interface.object_getattr(
                object_in=self.tcdiags_obj, key=app, force=True))
        self.options_obj = self.schema(cls_schema_file=cls_schema_file,
                                       cls_opts=cls_opts)

    @privatemethod
    def schema(
        self: Generic, cls_schema_file: str, cls_opts: Dict
    ) -> SimpleNamespace:
        """
        Description
        -----------

        This method evaluates the schema corresponding to the
        respective application.

        cls_schema_file: str

            A Python string specifying the file path for the
            YAML-formatted file containing the schema attributes for
            the respective application (base-class attribute
            `app_obj`).

        cls_opts: Dict

            A Python dictionary containing the configuration defined
            options for the respective application (base-class
            attribute `app_obj`).

        Returns
        -------

        options_obj: SimpleNamespace

            A Python SimpleNamespace containing the respective
            application configuration.

        """

        # Evaluate the schema and define the configuration for the
        # respective application.
        schema_def_dict = YAML().read_yaml(yaml_file=cls_schema_file)
        cls_schema = schema_interface.build_schema(
            schema_def_dict=schema_def_dict)
        options_obj = parser_interface.dict_toobject(
            in_dict=schema_interface.validate_schema(
                cls_schema=cls_schema, cls_opts=cls_opts, write_table=True
            )
        )

        return options_obj

    def write_output(
            self: Generic,
            output_file: str,
            var_obj: SimpleNamespace,
            var_list: List,
            coords_2d: Dict = None,
            coords_3d: Dict = None,
    ) -> None:
        """
        Description
        -----------

        This method writes the quantities within the calling class
        SimpleNamespace (`var_obj`) to the specified external
        netCDF-formatted file path.

        Parameters
        ----------

        output_file: str

            A Python string defining the path to the output
            netCDF-formatted file.

        var_obj: SimpleNamespace

            A Python SimpleNamespace object containing the quantities
            to be written to the output netCDF-formatted file.

        var_list: List

            A Python list of output variables.

        Keywords
        --------

        coords_2d: Dict, optional

            A Python dictionary containing the 2-dimensional
            coordinate and dimension attributes; this is assumes CF
            compliance.

        coords_3d: Dict, optional

            A Python dictionary containing the 3-dimensional
            coordinate and dimension attributes; this is assumes CF
            compliance.

        """

        # Write the netCDF-formatted output file acccordingly.
        msg = f"Writing netCDF-formatted file path {output_file}."
        self.logger.info(msg=msg)
        ncwrite = NCWrite(output_file=output_file)
        ncwrite.write(
            var_obj=var_obj, var_list=var_list, coords_2d=coords_2d, coords_3d=coords_3d
        )

# ----


class Metrics(Diagnostics):
    """
    Description
    -----------

    This is the base-class object for all Metrics sub-classes; it is a
    sub-class of diagnostics.

    Parameters
    ----------

    tcdiags_obj: SimpleNamespace

        A Python SimpleNamespace object containing all configuration
        attributes for the respective application including inputs
        (i.e., `inputs` and `tcinfo`) as well as the remaining
        (supported) applications.

    app_obj: SimpleNamespace

        A Python SimpleNamespace object containing the attributes for
        the respective sub-class application.

    Other Parameters
    ----------------

    args: Tuple

        A Python tuple containing additional arguments passed to the
        constructor.

    kwargs: Dict

        A Python dictionary containing additional key and value pairs
        to be passed to the constructor.

    """

    def __init__(
        self: Diagnostics,
        tcdiags_obj: SimpleNamespace,
        *args: Tuple,
        **kwargs: Dict,
    ):
        """
        Description
        -----------

        Creates a new Metrics object.

        """

        # Define the base-class attributes.
        super().__init__(tcdiags_obj=tcdiags_obj)


# ----
