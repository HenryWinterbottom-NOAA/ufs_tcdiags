"""
Module
------

    ncwrite.py

Description
-----------

    This module contains functions to build and write netCDF-formatted
    file paths.

Functions
---------

    __getcoords__(ncio_obj)

        This function defines the Climate and Forecast (CF) Metadata
        Convention compliant grid-coordinates.

    __getvarobj__(ncio_obj)

        This function builds a Python SimpleNamespace object
        containing the output variable attributes.

    __write__(xarrlist, ncoutput)

        This function writes the netCDF-formatted file path.

    __xarraylist__(varobj, coords_dict)

        This method builds a Python list of DataArray objects to be
        used to build and write the netCDF-formatted file path.

    ncwrite(func)

        This function is a wrapper function for building and writing
        netCDF-formatted files.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

- xarray; https://github.com/pydata/xarray

Author(s)
---------

    Henry R. Winterbottom; 13 March 2023

History
-------

    2023-03-13: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=fixme

# ----

import functools
from collections import OrderedDict
from types import SimpleNamespace
from typing import Callable, Dict, List, Tuple

import numpy
from tools import parser_interface
from utils.logger_interface import Logger
from xarray import DataArray, merge

# ----

# Define all available module properties
__all__ = ["ncwrite"]

# ----

logger = Logger(caller_name=__name__)

# ----


def __getcoords__(ncio_obj: SimpleNamespace) -> Dict:
    """
    Description
    -----------

    This function defines the Climate and Forecast (CF) Metadata
    Convention compliant grid-coordinates.

    Parameters
    ----------

    ncio_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the
        netCDF-formatted output file attributes.

    Returns
    -------

    coords_dict: ``Dict``

        A Python dictionary containing the CF-compliant grid
        coordinate attributes.

    """

    # TODO: This function lacks a means to handle unstructured-type
    # grids; this includes tripolar projections.

    # Build the Python dictionary containing the CF-compliant grid
    # coordinate attributes.
    coords_dict = OrderedDict()
    grid_coords = ncio_obj.grid_coords
    for var in vars(ncio_obj):
        varinfo = parser_interface.object_getattr(object_in=ncio_obj, key=var)
        try:
            grid_coord_idx = varinfo.grid_coord_idx
            if grid_coord_idx is not None:
                values = numpy.array(varinfo.values)
                if not varinfo.unstructured:
                    if grid_coord_idx == 1:
                        values = values[:, 0]
                    if grid_coord_idx == 2:
                        values = values[0, :]
                coords_dict[f"{grid_coords[grid_coord_idx]}"] = values
        except AttributeError:
            pass

    return coords_dict


# ----


def __getvarobj__(ncio_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function builds a Python SimpleNamespace object containing
    the output variable attributes.

    Parameters
    ----------

    ncio_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the
        netCDF-formatted output file attributes.

    Returns
    -------

    varobj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the output
        variable attributes.

    """

    # Build the Python SimpleNamespace object containing the output
    # variable attributes.
    varobj = parser_interface.object_define()
    varlist = parser_interface.object_getattr(
        object_in=ncio_obj, key="ncvarlist", force=True
    )
    if varlist is None:
        msg = "No variables have been defined for output; no output will be written."
        logger.warn(msg=msg)
        varobj = None
    else:
        for var in varlist:
            varinfo = parser_interface.object_getattr(
                object_in=ncio_obj, key=var, force=True
            )
            varobj = parser_interface.object_setattr(
                object_in=varobj, key=var, value=varinfo
            )

    return varobj


# ----


def __write__(xarrlist: List[DataArray], ncoutput: str) -> None:
    """
    Description
    -----------

    This function writes the netCDF-formatted file path.

    Parameters
    ----------

    xarrlist: ``List[DataArray]``

        A Python list of DataArray objects from which to build the
        netCDF-formatted file path.

    ncoutput: ``str``

        A Python string specifying the netCDF-formatted file path to
        be written.

    """

    # Build and write the netCDF-formatted file path.
    dsout = merge(xarrlist)
    dsout.to_netcdf(ncoutput)


# ----


def __xarraylist__(varobj: SimpleNamespace, coords_dict: Dict) -> List[DataArray]:
    """
    Description
    -----------

    This method builds a Python list of DataArray objects to be used
    to build and write the netCDF-formatted file path.

    Parameters
    ----------

    varobj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the output
        variable attributes.

    coords_dict: ``Dict``

        A Python dictionary containing the coordinate axis/axes
        attributees.

    Returns
    -------

    xarrlist: ``List[DataArray]``

        A Python list of DataArray objects from which to build the
        netCDF-formatted file path.

    """

    # Build the respective output variable DataArray objects.
    xarrdslist = []
    varlist = list(vars(varobj).keys())
    for var in varlist:
        varinfo = parser_interface.object_getattr(object_in=varobj, key=var)
        coords = OrderedDict({key: coords_dict[key] for key in varinfo.coords})
        msg = f"Building DataArray object for variable {var}."
        logger.info(msg=msg)
        attributes = parser_interface.object_getattr(
            object_in=varinfo, key="attributes", force=True
        )
        if attributes is None:
            attributes = {}
        xarrdsobj = DataArray(
            name=var,
            dims=varinfo.coords,
            coords=coords,
            data=numpy.array(varinfo.values),
        ).assign_attrs(attributes)
        xarrdslist.append(xarrdsobj.to_dataset(name=var))

    return xarrdslist


# ----


def ncwrite(func: Callable) -> Callable:
    """
    Description
    -----------

    This function is a wrapper function for building and writing
    netCDF-formatted files.

    Parameters
    ----------

    func: ``Callable``

        A Python Callable object containing the function to be
        wrapped.

    Returns
    -------

    wrapped_function: ``Callable``

        A Python Callable object containing the wrapped function.

    """

    @functools.wraps(func)
    async def wrapped_function(*args: Tuple, **kwargs: Dict) -> Callable:
        """
        Description
        -----------

        This method builds and writes a specified netCDF-formatted
        file path.

        Other Parameters
        ----------------

        args: ``Tuple``

            A Python tuple containing additional arguments passed to
            the constructor.

        kwargs: ``Dict``

            A Python dictionary containing additional key and value
            pairs to be passed to the constructor.

        """

        # Build and write the netCDF-formatted file path.
        ncio_obj = await func(*args, **kwargs)
        if ncio_obj is not None:
            coords_dict = __getcoords__(ncio_obj=ncio_obj)
            varobj = __getvarobj__(ncio_obj=ncio_obj)
            xarrlist = __xarraylist__(varobj=varobj, coords_dict=coords_dict)
            msg = f"Writing netCDF-formatted file {ncio_obj.ncoutput}."
            logger.info(msg=msg)
            __write__(xarrlist=xarrlist, ncoutput=ncio_obj.ncoutput)
        else:
            msg = (
                "No outputs have been specified; a netCDF-formatted file "
                "will not be written."
            )
            logger.warn(msg=msg)

    return wrapped_function
