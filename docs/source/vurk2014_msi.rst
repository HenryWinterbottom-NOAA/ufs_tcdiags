Vukicevic et al., (2014)
========================

This application computes the tropical cyclone (TC) multi-scale
intensity (MSI) in accordance with that described by `Vukicevic et
al., (2014) <https://doi.org/10.1175/JAS-D-13-0153.1>`_.

^^^^^^^^^^^^^
Configuration
^^^^^^^^^^^^^

The following table provides and describes the configurable variables
for the application. Note that if a **Default Value** is missing, the
respective variable is mandatory.

.. list-table::
   :widths: auto
   :header-rows: 1

   * - **Variable**
     - **Description**
     - **Default**
   * - ``drho``
     - Incremental radial distance (meters) for polar coordinate grid
       computations.
     - 40000
   * - ``dphi``
     - Incremental azimuthal angle (degrees) for the polar coordinate
       grid computations.
     - 45
   * - ``max_radius``
     - The maximum radial distance (meters) for the polar coordinate
       grid.
     - 200000
   * - ``max_wn``
     - The total number of wave-numbers for the spectral
       decomposition.
     - 3
   * - ``output_file``
     - The netCDF-formatted file path to contain the variables
       specified in ``output_varlist``; only written if
       ``write_output`` (below) is ``True``.
     -
   * - ``output_varlist``
     - The file path for the YAML-formatted file containing the list
       of output variables.
     -        
   * - ``write_output``
     - Write the variables specified in ``output_varlist`` to the
       netCDF-formatted file path described in the TC MSI
       configuration file.
     - ``False``
       
The contents of an example TC MSI YAML-formatted configuration file
follows.

.. code-block:: yaml

   app_module: tcdiags.vurk2014_msi
   app_class: VURK2014
   schema: !ENV ${TCDIAGS_ROOT}/parm/schema/tcdiags.vurk2014_msi.yaml
   drho: 50000.
   dphi: 1
   max_radius: 1200000.
   max_wn: 3
   write_output: true
   output_file: ./tcdiags.vurk2014_msi.%s.nc
   output_varlist: !INC /home/ufs_tcdiags/parm/io/tcdiags.vurk2014_msi.yaml

Note that the application assumes that the environment variable
``TCDIAGS_ROOT`` has been defined and points to the top-level
directory of the ``ufs_tcdiags`` repository clone. Further, the
``output_varlist`` points to a YAML-formatted file containing the
variables to be written to ``output_file`` if ``write_output`` is
``True``. The default file for the application appears as follows.

.. code-block:: yaml

  wnds10m:
    name: |
         magnitude of the total 10-meter (near-surface) wind field
    units: meter_per_second
    description: |
         Polar projection for the 10-meter total wind field.

Also included automatically within the netCDF-formatted output file
are the wave-number decompositions for the 10-meter wind field. The
total number of wave-numbers in the spectra are defined the ``max_wn``
in the table above. An example snippet from the netCDF-formatted file
follows.

.. code-block:: bash

   user@host:$ ncdump -h ./tcdiags.vurk2014_msi.21L.nc

   dimensions:
	   radial = 25 ;
	   azimuth = 362 ;
	   wavenumber = 3 ;
   variables:
    	   double radial(radial) ;
	   	   radial:_FillValue = NaN ;
	   double azimuth(azimuth) ;
	    	   azimuth:_FillValue = NaN ;
	   double wnds10m(radial, azimuth) ;
		   wnds10m:_FillValue = NaN ;
		   wnds10m:description = "Polar projection for the near surface total wind field magnitude.\n" ;
		   wnds10m:name = "magnitude of the total 10-meter (near-surface) wind field\n" ;
		   wnds10m:units = "meter_per_second" ;
	   int64 wavenumber(wavenumber) ;
	   double wnds10m_spec(wavenumber, radial, azimuth) ;
		   wnds10m_spec:_FillValue = NaN ;
		   wnds10m_spec:name = "wavenumber spectra for the 10-meter wind field" ;
		   wnds10m_spec:description = "Polar projection for the near surface total wind field wave number spectra." ;

^^^^^^^^^^^^^^^^^^^^^^^
Running the Application
^^^^^^^^^^^^^^^^^^^^^^^

The TC MSI application can be executed using a variety of
methods. Each is described below.

========
Terminal
========

The TC MSI application may be executed within an supporting
environment as follows.

.. code-block:: bash

   user@host:$ export PYTHONPATH="/path/to/ufs_tcdiags/ush":"${PYTHONPATH}"
   user@host:$ cd /path/to/ufs_tcdiags/scripts
   user@host:$ ./compute_tcdiags.py --help

   Usage: compute_tcdiags.py [-h] [-tcmsi] [-tcpi] [-tcstrflw] yaml

   Tropical cyclone diagnostics computation(s) application interface.

   Positional Arguments:
     yaml        YAML-formatted tropical cyclone diagnostics configuration file.

   Optional Arguments:
     -h, --help  show this help message and exit
     -tcmsi      YAML-formatted file containing the TC multi-scale intensity application configuration.
     -tcpi       YAML-formatted file containing the TC potential intensity application configuration.
     -tcstrflw   YAML-formatted file containing the TC steering application configuration.

   user@host:$ ./compute_tcdiags.py /path/to/ufs_tcdiags/parm/tcdiags.demo.yaml -tcmsi

================
Jupyter Notebook
================
   
The TC MSI application can also be executed from within a Jupyter
notebook as follows.

.. code-block:: bash

   user@host:$ export PYTHONPATH="/path/to/ufs_tcdiags/jupyter":"/path/to/ufs_tcdiags/ush":"${PYTHONPATH}"
   user@host:$ cd /path/to/ufs_tcdiags/jupyter/notebooks
   user@host:$ /path/to/jupyter notebook tcdiags.vurk2014_msi.ipynb

This action behaves as the terminal instance for the application
(above) but is executed from within the respective Jupyter notebook.

================
Docker Container
================

The TC MSI application may be executed within a supporting Docker
container as follows.

.. code-block:: bash

   user@host:$ /path/to/docker run -v /path/to/ufs_tcdiags:/home/ufs_tcdiags -it ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_tcdiags:latest
   user@host:$ export PYTHONPATH="/home/ufs_tcdiags/ush":"${PYTHONPATH}"
   user@host:$ cd /home/ufs_tcdiags/scripts
   user@host:$ ./compute_tcdiags.py --help

   Usage: compute_tcdiags.py [-h] [-tcmsi] [-tcpi] [-tcstrflw] yaml

   Tropical cyclone diagnostics computation(s) application interface.

   Positional Arguments:
     yaml        YAML-formatted tropical cyclone diagnostics configuration file.

   Optional Arguments:
     -h, --help  show this help message and exit
     -tcmsi      YAML-formatted file containing the TC multi-scale intensity application configuration.
     -tcpi       YAML-formatted file containing the TC potential intensity application configuration.
     -tcstrflw   YAML-formatted file containing the TC steering application configuration.

   user@host:$ ./compute_tcdiags.py /home/ufs_tcdiags/parm/tcdiags.demo.yaml -tcmsi

==========================================
Jupyter Notebook Within a Docker Container
==========================================

Similar to the Jupyter notebook and Docker container examples above,
the Jupyter notebook can also be launched from within the Docker
container. This can be accomplished as follows.

.. code-block:: bash

   user@host:$ /path/to/docker run -v /path/to/ufs_tcdiags:/home/ufs_tcdiags -p 8888:8888 -it ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_tcdiags:latest
   user@host:$ export PYTHONPATH="/home/ufs_tcdiags/ush":"/home/ufs_tcdiags/jupyter":"${PYTHONPATH}"
   user@host:$ cd /path/to/ufs_tcdiags/jupyter/notebooks
   user@host:$ /path/to/jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root tcdiags.vurk2014_msi.ipynb

The above action will provide the user a local HTML path and an
associated token as follows.

.. code-block:: bash

    To access the server, open this file in a browser:
        file:///root/.local/share/jupyter/runtime/jpserver-21362-open.html
    Or copy and paste one of these URLs:
	http://5186640b39b0:8889/tree?token=abcdefghijklmnopqrstuvwxwy0123456789ABCDEFGHIJKL
        http://127.0.0.1:8889/tree?token=abcdefghijklmnopqrstuvwxwy0123456789ABCDEFGHIJKL

Copy the paste the token attribute that begins with
``http://127.0.0.1:8889`` into a web browser address bar and execute
the respective Jupyter notebook as described above.

^^^^^^^^^^^^^^^
Example Results
^^^^^^^^^^^^^^^

The following example for TC `AL14
<https://www.nhc.noaa.gov/archive/2016/al14/al142016.fstadv.012.shtml?>`_
is computed from a nominally 1.0-degree `ERA5
<https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5>`_
analysis valid 0000 UTC 01 October 2016.

.. list-table::
   :widths: auto
   :header-rows: 1

   * - **TC 14L MSI Attributes**
     - **Value (Units)**
   * - Center Latitude
     - 13.4 (degrees)
   * - Center Longitude
     - -72 (degrees) 
   * - Maximum 10-meter Wind Speed
     - 22.09724998474121 (m/s)
   * - Azimuth of Maximum 10-meter Wind Speed
     - 60.000000000000135 (degrees)
   * - Radius of Maximum 10-meter Wind Speed
     - 120000.0 (m)
   * - Wavenumber-0 Maximum Wind Speed
     - 18.144823659624375 (m/s)
   * - Wavenumber-1 Maximum Wind Speed
     - 3.1016818996685966 (m/s)
   * - Wavenumbers (0+1) Maximum Wind Speed
     - 19.831703222806482 (m/s)
   * - Residual Wavenumber Maximum Wind Speed
     - 2.265546761934729 (m/s)
   * - Radius of Maximum Wind Latitude
     - 12.373095556722303 (degrees)
   * - Radius of Maximum Wind Longitude
     - -72.30604517770875 (degrees)

.. list-table::
   :widths: auto
   :header-rows: 0   

   * - .. figure:: _static/tcwnmsi.10m_wind.14L.png
          :name: tcwnmsi.10m_wind.14L
          :align: center
     - .. figure:: _static/tcwnmsi.wn0_wind.14L.png
          :name: tcwnmsi.wn0_wind.14L
          :align: center
   * - .. figure:: _static/tcwnmsi.wn1_wind.14L.png
          :name: tcwnmsi.wn1_wind.14L
          :align: center
     - .. figure:: _static/tcwnmsi.wn0p1_wind.14L.png
          :name: tcwnmsi.wn0p1_wind.14L
          :align: center
   * - .. figure:: _static/tcwnmsi.wn2_wind.14L.png
          :name: tcwnmsi.wn2_wind.14L
          :align: center
     - .. figure:: _static/tcwnmsi.wnres_wind.14L.png
          :name: tcwnmsi.wnres_wind.14L
          :align: center		  

Tropical cyclone multi-scale intensity attributes for TC AL14 as
follows: 10-meter wind-speed (top-left); 10-meter wind-speed
wave-number 0 component (top-right); 10-meter wind-speed wave-number 1
component (middle-left); 10-meter wind-speed wave-numbers (0 + 1)
component (middle-right); 10-meter wind-speed wave-number 2 component
(bottom-left); and 10-meter wind-speed residual wave-numbers
(bottom-right). The Jupyter notebook to generate the above can be
found `here <jupyter/notebooks/tcdiags.vurk2014_msi.ipynb>`_.
