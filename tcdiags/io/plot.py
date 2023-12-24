"""
Module
------

    plot.py

Description
-----------

    This module contains functions to build, create, and publish
    figures as defined by the respective caller configurations.

Functions
---------

    plot(func)

        This function is a wrapper function for building, creating,
        and publishing figures define by the respective caller
        configuration.

Requirements
------------

- ufs_pyutils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 24 December 2023

History
-------

    2023-12-24: Henry Winterbottom - - Initial implementation.

"""

# ----

import functools
from importlib import import_module
from typing import Callable, Dict, Tuple, Type

from tools import parser_interface

# ----

# Define all available module properties
__all__ = ["plot"]

# ----


def plot(func: Callable) -> Callable:
    """
    Description
    -----------

    This function is a wrapper function for building, creating, and
    publishing figures define by the respective caller configuration.

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
    async def wrapped_function(
        self: Type["MyClass"], *args: Tuple, **kwargs: Dict
    ) -> Callable:
        """
        Description
        -----------

        This method builds, creates, and publishes figures as defined
        by the respective caller configuration.

        Other Parameters
        ----------------

        args: ``Tuple``

            A Python tuple containing additional arguments passed to
            the constructor.

        kwargs: ``Dict``

            A Python dictionary containing additional key and value
            pairs to be passed to the constructor.

        """

        # Build, create, and publish the respective figures.
        app_obj = await func(self, *args, **kwargs)
        plot_module = parser_interface.dict_key_value(
            dict_in=app_obj.plot_dict, key="plot_module", force=True, no_split=True
        )
        plot_class = parser_interface.dict_key_value(
            dict_in=app_obj.plot_dict, key="plot_class", force=True, no_split=True
        )
        plot_obj = parser_interface.object_getattr(
            import_module(plot_module), key=plot_class, force=True
        )
        plot_obj(tcdiags_obj=app_obj.tcdiags_obj).run(app_obj=app_obj.varobj)

    return wrapped_function
