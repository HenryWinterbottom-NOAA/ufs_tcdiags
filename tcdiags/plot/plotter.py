"""
Module
------

    plotter.py

Description
-----------

    This module contains functions for plotting (and saving)
    `matplotlib.pyplot` figures.

Functions
---------

    plotter(save_name, dpi=100)

        This function provides a decorator to be used to generate
        `matplotlib.pyplot` figures.

Requirements
------------

- matplotlib; https://github.com/matplotlib/matplotlib

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 22 December 2023

History
-------

    2023-12-22: Henry Winterbottom -- Initial implementation.

"""

# ----

import functools
from typing import Callable, Dict, Tuple

import matplotlib.pyplot as plt
from utils.logger_interface import Logger

# ----

# Define all available module properties.
__all__ = ["plotter"]

# ----

logger = Logger(caller_name=__name__)

# ----


def plotter(save_name: str, dpi: int = 100) -> Callable:
    """
    Description
    -----------

    This function provides a decorator to be used to generate
    matplotlib.pyplot figures.

    Parameters
    ----------

    save_name: ``str``

        A Python string specifying the filename path for the
        respective image/figure.

    Keywords
    --------

    dpi: ``int``

        A Python integer specifying the dots per inch for the output
        image.

    Returns
    -------

    decorator: ``Callable``

        A Python Callable object.

    """

    # Define the decorator.
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapped_function(*args: Tuple, **kwargs: Dict) -> Callable:
            func(*args, **kwargs)
            msg = f"Saving matplotlib.pyplot object to {save_name}."
            logger.info(msg=msg)
            plt.tight_layout()
            plt.savefig(save_name, dpi=dpi)
            plt.clf()
            plt.close("current")

        return wrapped_function

    return decorator
