"""
Module
------

    basemap.py

Description
-----------

    This module contains functions to build and decorate a Basemap
    object in accordance with specified attributes.

Functions
---------

    __bldmap__(basemap_dict)

        This function builds the Basemap object in accordance with the
        specified basemap attributes/configuration.

    __decmap__(basemap_obj)

        This function decorates the basemap configuration; all
        supported basemap decorations are available; see `[here]
        <https://tinyurl.com/basemap-map-background>`_ for all
        supported options.

    basemapper(func)

        This function is a wrapper function for building the Basemap
        object decorated accordingly.

Requirements
------------

- basemap; https://github.com/matplotlib/basemap

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 18 December 2023

History
-------

    2023-12-18: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=eval-used
# pylint: disable=unused-import

# ----

import functools
from types import SimpleNamespace
from typing import Callable, Dict, Tuple

import numpy
from mpl_toolkits.basemap import Basemap
from tools import parser_interface

# ----


def __bldmap__(basemap_dict: Dict) -> Basemap:
    """
    Description
    -----------

    This function builds the Basemap object in accordance with the
    specified basemap attributes/configuration.

    Parameters
    ----------

    basemap_dict: ``Dict``

        A Python dictionary containing the basemap
        attributes/configuration.

    Returns
    -------

    basemap_obj: ``Basemap``

        A Python Basemap object containing the basemap projection.

    """

    # Build the Basemap object.
    params_obj = parser_interface.argspec(func=Basemap)
    kwargs = dict(
        zip(params_obj.args[-len(params_obj.defaults) :], params_obj.defaults)
    )
    kwargs = {
        key: basemap_dict[key] if key in basemap_dict else value
        for (key, value) in kwargs.items()
    }
    basemap = Basemap(**kwargs)

    return basemap


# ----


def __decmap__(basemap_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function decorates the basemap configuration; all supported
    basemap decorations are available; see `[here]
    <https://tinyurl.com/basemap-map-background>`_ for all supported
    options.

    Parameters
    ----------

    basemap_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the basemap
        attributes, including the Basemap object.

    Returns
    -------

    basemap_obj: ``SimpleNamespace``

        A Python SimpleNamespace object updated with the specified
        basemap attributes.

    """

    # Decorate the respective basemap.
    for pltattr in basemap_obj.plotting.keys():
        pltattr_dict = basemap_obj.plotting[pltattr]
        params_obj = parser_interface.argspec(
            func=parser_interface.object_getattr(object_in=Basemap, key=pltattr)
        )
        def_kwargs = dict(
            zip(params_obj.args[-len(params_obj.defaults) :], params_obj.defaults)
        )
        kwargs = {
            key: pltattr_dict[key] if key in pltattr_dict else value
            for (key, value) in def_kwargs.items()
        }
        for item in pltattr_dict:
            try:
                kwargs[item] = eval(pltattr_dict[item])
            except (TypeError, NameError, ValueError):
                pass
        parser_interface.object_getattr(object_in=basemap_obj.Basemap, key=pltattr)(
            **kwargs
        )

    return basemap_obj


# ----


def basemapper(func: Callable) -> Callable:
    """
    Description
    -----------

    This function is a wrapper function for building the Basemap
    object decorated accordingly.

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
    def wrapped_function(self: Callable, *args: Tuple, **kwargs: Dict):
        """
        Description
        -----------

        This method builds the Basemap object including the specified
        basemap decorations.

        Other Parameters
        ----------------

        args: ``Tuple``

            A Python tuple containing additional arguments passed to
            the constructor.

        kwargs: ``Dict``

            A Python dictionary containing additional key and value
            pairs to be passed to the constructor.

        """

        # Build the decorated basemap object.
        basemap_obj = func(self, *args, **kwargs)
        basemap_obj.Basemap = __bldmap__(basemap_dict=basemap_obj.basemap)
        basemap_obj = __decmap__(basemap_obj=basemap_obj)

        return basemap_obj

    return wrapped_function
