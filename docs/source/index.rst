################################
UFS Tropical Cyclone Diagnostics
################################

^^^^^^^^^^^
Description
^^^^^^^^^^^

The Unified Forecast System (UFS) Tropical Cyclone Diagnostics
package, henceforth ``ufs_tcdiags``, provides applications to compute
and/or perform analytic and diagnostic evaluations of tropical cyclone
(TC) related attributes.

^^^^^^^^^^
Developers
^^^^^^^^^^

* Henry R. Winterbottom - henry.winterbottom@noaa.gov

^^^^^^^
Cloning
^^^^^^^

The ``ufs_tcdiags`` repository may be obtained as follows.

.. code-block:: bash

   user@host:$ /path/to/git clone --recursive https://www.github.com/HenryWinterbottom-NOAA/ufs_tcdiags ./ufs_tcdiags

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Installing Python Dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install the necessary Python dependencies as follows.

.. code-block:: bash

   user@host:$ /path/to/pip install -r /path/to/ufs_tcdiags/requirements.txt

^^^^^^^^^^^^^^^^^^^^^^
Container Environments
^^^^^^^^^^^^^^^^^^^^^^

A Docker container environment, supporting and within which the
``ufs_tcdiags`` applications can be executed, may be obtained and
executed as follows.

.. code-block:: bash

   user@host:$ /path/to/docker ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_tcdiags:latest
   user@host:$ /path/to/docker container run -it ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_tcdiags:latest
   
^^^^^^^^^^^^
Applications
^^^^^^^^^^^^

.. toctree:: 
   :maxdepth: 1

   tc.rst
   tcpi.rst
   metrics.rst

