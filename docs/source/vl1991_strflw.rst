Velden and Leslie (1991)
========================

This application diagnoses the tropical cyclone (TC) relative layer
mean wind attributes using an application based on `Velden and Leslie, (1991) <https://doi.org/10.1175/1520-0434(1991)006<0244:TBRBTC>2.0.CO;2>`_.

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
   * - ``isolevels``
     - A list of isobaric levels at which the TC steering flow
       attributes should be diagnosed.
     - 
   * - ``distance``
     - The distance (meters) relative to a TC position about which to
       filter the respective TC wind field.
     - 1600000.0
   * - ``ncoeffs``
     - The total number of singular values used to reconstruct the
       filtered TC wind field.
     - 10
   * - ``ddist``
     - The radial distance (meters) interval for the radial
       interpolation.
     - 100000.0
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
       netCDF-formatted file path described in the TC steering flow
       configuration file.
     - ``False``
       
The contents of an example YAML-formatted configuration file for the
TC steering flow application follows.

.. code-block:: yaml

   app_module: tcdiags.vl1991_strflw
   app_class: VL1991
   schema: !ENV ${TCDIAGS_ROOT}/parm/schema/tcdiags.vl1991_strflw.yaml
   isolevels:
     - 100000
     - 90000
     - 80000
     - 70000
     - 60000
     - 50000
     - 40000
     - 30000
     - 20000
     - 10000
   distance: 1600000.0
   ddist: 100000.0
   write_output: true
   output_file: ./tcdiags.vl1991_strflw.nc
   output_varlist: !INC /home/ufs_tcdiags/parm/io/tcdiags.vl1991_strflw.yaml

Note that the application assumes that the environment variable
``TCDIAGS_ROOT`` has been defined and points to the top-level
directory of the ``ufs_tcdiags`` repository clone. Further, the
``output_varlist`` points to a YAML-formatted file containing the
variables to be written to ``output_file`` if ``write_output`` is
``True``. A snippet containing some of the contents written to the
netCDF-formatted file path follows.

.. code-block:: bash

   user@host:$ ncdump -h ./tcdiags.vl1991_strflw.nc

   dimensions:
	   plevs = 10 ;
	   lat = 192 ;
	   lon = 384 ;
   variables:
	   int64 plevs(plevs) ;
	   double lat(lat) ;
		   lat:_FillValue = NaN ;
	   double lon(lon) ;
		   lon:_FillValue = NaN ;
	   double chi(plevs, lat, lon) ;
		   chi:_FillValue = 9.96920996838687e+36 ;
		   chi:missing_value = 9.96920996838687e+36 ;
		   chi:description = "\"The velocity potential field.\"\n" ;
		   chi:name = "velocity potential" ;
		   chi:units = "meters^2/second" ;
	   double divg(plevs, lat, lon) ;
	     	   divg:_FillValue = 9.96920996838687e+36 ;
		   divg:missing_value = 9.96920996838687e+36 ;
		   divg:description = "\"The total divergence field.\"\n" ;
		   divg:name = "divergence" ;
		   divg:units = "1/second" ;

^^^^^^^^^^^^^^^^^^^^^^^
Running the Application
^^^^^^^^^^^^^^^^^^^^^^^

The TC steering flow application can be executed using a variety of
methods. Each is described below.

========
Terminal
========

The TC steering flow application may be executed within an supporting
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

   user@host:$ ./compute_tcdiags.py /path/to/ufs_tcdiags/parm/tcdiags.demo.yaml -tcstrflw

================
Jupyter Notebook
================
   
The TC steering flow application can also be executed from within a
Jupyter notebook as follows.

.. code-block:: bash

   user@host:$ export PYTHONPATH="/path/to/ufs_tcdiags/jupyter":"/path/to/ufs_tcdiags/ush":"${PYTHONPATH}"
   user@host:$ cd /path/to/ufs_tcdiags/jupyter/notebooks
   user@host:$ /path/to/jupyter notebook tcdiags.vl1991_strflw.ipynb

This action behaves as the terminal instance for the application
(above) but is executed from within the respective Jupyter notebook.

================
Docker Container
================

The TC steering flow application may be executed within an appropriate
Docker container as follows.

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

   user@host:$ ./compute_tcdiags.py /home/ufs_tcdiags/parm/tcdiags.demo.yaml -tcstrflw

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
   user@host:$ /path/to/jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root tcdiags.vl1991_strflw.ipynb

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

The following example is computed from a nominally 1.0-degree `ERA5 <https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5>`_
analysis valid 0000 UTC 01 October 2016.

.. list-table::
   :widths: auto
   :header-rows: 0   

   * - .. figure:: _static/tcstrflw.shallow.png
          :name: tcstrflw.shallow
	  :align: center
   *  - .. figure:: _static/tcstrflw.medium.png
          :name: tcstrflw.medium
	  :align: center
   *  - .. figure:: _static/tcstrflw.deep.png
          :name: tcstrflw.deep
	  :align: center

The layer-mean winds with respect to the intensity ranges illustrated
by Figure 2 of `Velden and Leslie, (1991) <https://doi.org/10.1175/1520-0434(1991)006<0244:TBRBTC>2.0.CO;2>`_
are shown above for the 850- to 500-hPa (top), 850- to 400-hPa
(center), and 850- to 300-hPa (bottom). The TC locations, valid for
0000 UTC 01 October 2016, are denoted by the respective red symbols.
