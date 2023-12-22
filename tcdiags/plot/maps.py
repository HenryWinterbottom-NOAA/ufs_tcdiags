"""
Module
------

    maps.py

Description
-----------

    This module contains the base-class object for all map-projection
    type plots.

Classes
-------

    Maps(tcdiags_obj, *args, **kwargs)

        This is the base-class object for all map-projection type
        plots; it is a sub-class of Plot.

Author(s)
---------

    Henry R. Winterbottom; 22 December 2023

History
-------

    2023-12-22: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=too-few-public-methods

# ----

from types import SimpleNamespace
from typing import Dict, Tuple

from tcdiags.plot.plot import Plot

# ----


class Maps(Plot):
    """
    Description
    -----------

    This is the base-class object for all map-projection type plots;
    it is a sub-class of Plot.

    Parameters
    ----------

    tcdiags_obj: ``SimpleNamespace``

        A Python SimpleNamespace containing the respective application
        attributes.

    Other Parameters
    ----------------

    args: ``Tuple``

        A Python tuple containing additional arguments passed to the
        constructor.

    kwargs: ``Dict``

        A Python dictionary containing additional key and value pairs
        to be passed to the constructor.

    """

    def __init__(
        self: Plot, tcdiags_obj: SimpleNamespace, *args: Tuple, **kwargs: Dict
    ):
        """
        Description
        -----------

        Creates a new Maps object.

        """

        # Define the base-class attributes.
        super().__init__(tcdiags_obj=tcdiags_obj, *args, **kwargs)
