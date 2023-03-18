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

    This module contains various method for compute attributes on a
    sphere.

Functions
---------

    bearing_geoloc(loc1, dist, heading)

        This function returns the geographical coordinate location
        compute from a reference geographical location and the
        distance and bearing for the destination location.

    haversine(loc1, loc2, radius=R_earth.value)

        This function computes and returns the great-circle (i.e.,
        haversine) between two locations.

Requirements
------------

- geopy; https://github.com/geopy/geopy

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 13March 2023

History
-------

    2023-03-13: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=no-name-in-module

# ----

from math import asin, cos, radians, sin, sqrt
from typing import Tuple

from astropy.constants import R_earth
from exceptions import GeoMetsError
from utils.logger_interface import Logger

import geopy
from geopy.distance import geodesic

# ----

# Define all available functions.
__all__ = ["bearing_geoloc", "haversine"]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


def bearing_geoloc(loc1: Tuple, dist: float, heading: float) -> Tuple[float, float]:
    """
    Description
    -----------

    This function returns the geographical coordinate location compute
    from a reference geographical location and the distance and
    bearing for the destination location.

    Parameters
    ----------

    loc1: tuple

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

    loc2: tuple

        A Python tuple containing the geographical coordinates of
        destination location; format is (lat, lon); units are degrees.

    """

    # Define the origin location attributes.
    origin = geopy.Point(loc1)

    # Compute the destination location.
    dest = geodesic(meters=dist).destination(origin, heading)
    loc2 = [dest.latitude, dest.longitude]

    return loc2

# ----


def haversine(loc1: Tuple, loc2: Tuple, radius: float = R_earth.value) -> float:
    """
    Description
    -----------

    This function computes and returns the great-circle (i.e.,
    haversine) between two locations.

    Parameters
    ----------

    loc1: tuple

        A Python tuple containing the geographical coordinates of
        location 1; format is (lat, lon); units are degrees.

    loc2: tuple

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

    # Convert from degrees to radians.
    (lat1, lon1, lat2, lon2) = list(map(radians, [lat1, lon1, lat2, lon2]))

    # Compute the great-circle distance (e.g., haversine).
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    dist = sin(dlat / 2.0) ** 2.0 + cos(lat1) * \
        cos(lat2) * sin(dlon / 2.0) ** 2.0
    hvsine = 2.0 * radius * asin(sqrt(dist))

    return hvsine
