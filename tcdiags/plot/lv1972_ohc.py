"""
Module
------

    lv1972_ohc.py

Description
-----------

    This module contains the base-class for plotting ocean heat
    content (OHC) and tropical cyclone heat potential (TCHP)
    attributes following Leipper and Volgenau (1972).

Classes
-------

    LV1972(tcdiags_obj)

        This is the base-class object for plotting ocean heat content
        (OHC) and tropical cyclone heat potential (TCHP) attributes
        following Leipper and Volgenau (1972); it is a sub-class of
        Maps.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

References
----------

    Leipper, D. F., and D. Volgenau. "Hurricane heat potential of the
    Gulf of Mexico". J. Phys. Oceanpgr. 2, 218–224.

Author(s)
---------

    Henry R. Winterbottom; 22 December 2023

History
-------

    2023-12-22: Henry Winterbottom -- Initial implementation.

"""

# ----


from types import SimpleNamespace

from tcdiags.plot.basemapper import basemapper
from tcdiags.plot.maps import Maps
from tools import parser_interface
from utils.decorator_interface import privatemethod

# ----


class LV1972(Maps):
    """
    Description
    -----------

    This is the base-class object for plotting ocean heat content
    (OHC) and tropical cyclone heat potential (TCHP) attributes
    following Leipper and Volgenau (1972); it is a sub-class of Maps.

    Parameters
    ----------

    tcdiags_obj: ``SimpleNamespace``

        A Python SimpleNamespace containing the OHC and TCHP
        attributes.

    """

    def __init__(self: Maps, tcdiags_obj: SimpleNamespace):
        """
        Description
        -----------

        Creates a new LV1972 object.

        """

        # Define the base-class attributes.
        super().__init__(tcdiags_obj=tcdiags_obj)

    @basemapper
    def basemap(self: Maps) -> SimpleNamespace:
        """
        Description
        -----------

        This method builds a Python SimpleNamespace object containing
        the basemap attributes for the respective map-type plots.

        Returns
        -------

        basemap_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the basemap
            attributes for the respective map-type plots.

        """

        # Define the basemap attributes for the respective map-type
        # plots.
        super().basemap()
        basemap_obj = parser_interface.dict_toobject(
            in_dict=parser_interface.object_getattr(
                object_in=self.tcdiags_obj.tcohc, key="plot", force=None
            )
        )

        return basemap_obj

    @privatemethod
    def plot(self: Maps, plt_obj: SimpleNamespace) -> None:
        """
        Description
        -----------

        This method plots the configuration specified figures.

        Parameters
        ----------

        plt_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the respective
            figure plotting attributes.

        """

        # Plot the configuration specified figures.
        figures = parser_interface.dict_key_value(
            dict_in=self.tcdiags_obj.tcohc.plot,
            key="figures",
            force=True,
            no_split=True,
        )
        if figures is None:
            msg = (
                "No figure functions have been specified; no figures will be generated."
            )
            self.logger.warn(msg=msg)
            return
        for figure in figures:
            basemap_obj = self.basemap()
            msg = f"Plotting figure {figure}."
            self.logger.info(msg=msg)
            app_obj = parser_interface.object_define()
            for key, value in parser_interface.dict_key_value(
                dict_in=figures, key=figure
            ).items():
                app_obj = parser_interface.object_setattr(
                    object_in=app_obj, key=key, value=str(value)
                )
            func = parser_interface.import_func(app_obj=app_obj)
            kwargs = {"ohc_obj": plt_obj, "basemap_obj": basemap_obj}
            func(**kwargs)

    def run(self: Maps, ohc_obj: SimpleNamespace) -> None:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Plots the configuration specified figures.

        Parameters
        ----------

        ohc_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the OHC
            attributes.

        """

        self.plot(plt_obj=ohc_obj)
