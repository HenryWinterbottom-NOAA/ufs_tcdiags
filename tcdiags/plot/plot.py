"""
Module
------

    plot.py

Description
-----------

    This module contains the base-class object for all plotting
    applications.

Classes
-------

    Plot(tcdiags_obj, *args, **kwargs)

        This is the base-class object for all plotting applications;
        it is a sub-class of ABC.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 22 December 2023

History
-------

    2023-12-22: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=too-few-public-methods
# pylint: disable=unused-argument

# ----

from abc import ABC, abstractmethod
from types import SimpleNamespace
from typing import Dict, Tuple

from utils.logger_interface import Logger

# ----

# Define all available module properties.
__all__ = ["Plot"]

# ----


class Plot(ABC):
    """
    Description
    -----------

    This is the base-class object for all plotting applications; it is
    a sub-class of ABC.

    Parameters
    ----------

    tcdiags_obj: ``SimpleNamespace``

        A Python SimpleNamespace containing the respective application
        attributes.

    Other Parameters
    ----------------

    args: Tuple

        A Python tuple containing additional arguments passed to the
        constructor.

    kwargs: Dict

        A Python dictionary containing additional key and value pairs
        to be passed to the constructor.

    """

    def __init__(self: ABC, tcdiags_obj: SimpleNamespace, *args: Tuple, **kwargs: Dict):
        """
        Description
        -----------

        Creates a new Plot object.

        """

        # Define the base-class attributes.
        self.logger = Logger(caller_name=f"{__name__}.{self.__class__.__name__}")
        self.tcdiags_obj = tcdiags_obj

    @abstractmethod
    def plot(self: ABC, plt_obj: SimpleNamespace) -> SimpleNamespace:
        """
        Description
        -----------

        This method provides a plotting layer for the respective
        sub-class task.

        Parameters
        ----------

        plt_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the plotting
            attributes for the respective application.

        """
