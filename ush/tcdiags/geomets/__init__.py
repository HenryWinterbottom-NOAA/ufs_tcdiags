# =========================================================================

# Module: ush/tcdiags/geomets/__init__.py

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

    __init__.py

Description
-----------

    This module contains various method to compute attributes/values
    on a sphere.

Functions
---------

    bearing_geoloc(loc1, dist, heading)

        This function returns the geographical coordinate location
        compute from a reference geographical location and the
        distance and bearing for the destination location.

    haversine(loc1, loc2, radius=R_earth.value)

        This function computes and returns the great-circle (i.e.,
        haversine) between two locations.

    radial_distance(refloc, latgrid, longrid, radius=R_earth.value)

        This function computes the radial distance for all
        geographical locations relative to a fixed (e.g., reference)
        location using the Haversine formulation.

Requirements
------------

- astropy; https://github.com/astropy/astropy

- metpy; https://unidata.github.io/MetPy/latest/index.html

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 13 March 2023

History
-------

    2023-03-13: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=no-name-in-module

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from math import asin, atan2, cos, radians, sin, sqrt
from typing import Tuple

import numpy
from astropy.constants import R_earth
from metpy.units import units
from tcdiags.exceptions import GeoMetsError
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["bearing_geoloc", "haversine", "radial_distance"]

# ----

logger = Logger(caller_name=__name__)

# ----


def bearing_geoloc(
    loc1: Tuple, dist: float, heading: float, radius: float = R_earth.value
) -> Tuple[float, float]:
    """
    Description
    -----------

    This function returns the geographical coordinate location compute
    from a reference geographical location and the distance and
    bearing for the destination location.

    Parameters
    ----------

    loc1: Tuple

        A Python tuple containing the geographical coordinates of
        location 1; format is (lat, lon); units are degrees.

    dist: float

        A Python float value specifying the distance from the
        reference geographical location to the destination location;
        units are meters.

    heading: float

        A Python float value specifying the heading from the reference
        geographical location to the destination location; units are
        degrees.

    Returns
    -------

    loc2: Tuple

        A Python tuple containing the geographical coordinates of
        destination location; format is (lat, lon); units are degrees.

    """

    # Compute the new latitude and longitude geographical location.
    (lat1, lon1, heading) = [
        numpy.radians(loc1[0]),
        numpy.radians(loc1[1]),
        numpy.radians(heading),
    ]
    lat2 = numpy.degrees(
        asin(
            sin(lat1) * cos(dist / radius)
            + cos(lat1) * sin(dist / radius) * cos(heading)
        )
    )
    lon2 = numpy.degrees(
        lon1
        + atan2(
            sin(heading) * sin(dist / radius) * cos(lat1),
            cos(dist / radius) - sin(lat1) * sin(lat2),
        )
    )

    return (lat2, lon2)


# ----


def haversine(loc1: Tuple, loc2: Tuple, radius: float = R_earth.value) -> float:
    """
    Description
    -----------

    This function computes and returns the great-circle (i.e.,
    haversine) between two locations.

    Parameters
    ----------

    loc1: Tuple

        A Python tuple containing the geographical coordinates of
        location 1; format is (lat, lon); units are degrees.

    loc2: Tuple

        A Python tuple containing the geographical coordinates of
        location 2; format is (lat, lon); units are degrees.

    Keywords
    --------

    radius: float, optional

        A Python float value defining the radial distance to be used
        when computing the haversine; units are meters.

    Returns
    -------

    hvsine: float

        A Python float value containing the great-circle distance
        (e.g., haversine) between the two locations defined upon
        entry; units are meters.

    """

    # Define the source and destination geographical locations.
    (lat1, lon1) = loc1
    (lat2, lon2) = loc2
    (lat1, lon1, lat2, lon2) = list(map(radians, [lat1, lon1, lat2, lon2]))

    # Compute the great-circle distance (e.g., haversine).
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    dist = sin(dlat / 2.0) ** 2.0 + cos(lat1) * cos(lat2) * sin(dlon / 2.0) ** 2.0
    hvsine = 2.0 * radius * asin(sqrt(dist))

    return hvsine


# ----


def radial_distance(
    refloc: Tuple,
    latgrid: numpy.array,
    longrid: numpy.array,
    radius: float = R_earth.value,
) -> numpy.array:
    """
    Description
    -----------

    This function computes the radial distance for all geographical
    locations relative to a fixed (e.g., reference) location using the
    Haversine formulation.

    Parameters
    ----------

    refloc: Tuple

        A Python tuple containing the geographical coordinates for the
        reference location; format is (lat, lon); units are degrees.

    latgrid: numpy.array

        A Python numpy.array 1-dimensional variable containing the
        latitude coordinate values; units are degrees.

    longrid: numpy.array

        A Python numpy.array 1-dimensional variable containing the
        longitude coordinate values; units are degrees.

    Keywords
    --------

    radius: float, optional

        A Python float value defining the radial distance to be used
        when computing the haversine; units are meters.

    Returns
    -------

    raddist: numpy.array

        A Python numpy.array 1-dimensional variable containing the
        radial distances relative to the reference geographical
        location; units are meters.

    Raises
    ------

    GeoMetsError:

        - raised if the either or both the latitude and longitude
          arrays are not 1-dimensional upon entry.

    """

    # Check that the input arrays are a single dimension; proceed
    # accordingly.
    if len(latgrid.shape) > 1 or len(longrid.shape) > 1:
        msg = (
            "The input latitude and longitude arrays must be of 1-dimension; "
            f"received latitude dimension {latgrid.shape} and longitude "
            f"dimension {longrid.shape} upon entry. Aborting!!!"
        )
        raise GeoMetsError(msg=msg)

    # Compute the radial distance array relative to the reference
    # location.
    raddist = numpy.zeros(numpy.shape(latgrid))
    raddist = [
        haversine(refloc, (latgrid[idx], longrid[idx]), radius=radius)
        for idx in range(len(raddist))
    ]

    return raddist
