=================================
UFS Tropical Cyclone Diagnostics
=================================

Description
===========

The Unified Forecast System (UFS) Tropical Cyclone Diagnostics
package, henceforth ``ufs_tcdiags``, provides applications to compute
and/or perform analytic and diagnostic evaluations of tropical cyclone
(TC) related attributes.

Developers
==========

- Henry R. Winterbottom - henry.winterbottom@noaa.gov

Cloning
=======

The ``ufs_tcdiags`` repository may be obtained as follows.

.. code-block:: bash

   user@host:$ /path/to/git clone --recursive https://www.github.com/HenryWinterbottom-NOAA/ufs_tcdiags ./ufs_tcdiags

Installing Python Dependencies
==============================

Install the necessary Python dependencies as follows.

.. code-block:: bash

   user@host:$ /path/to/pip install -r /path/to/ufs_tcdiags/requirements.txt

Virtual Environments
====================

To configure the virtual environment for the ``ufs_tcdiags`` applications, do as follows.

.. code-block:: bash

   user@host:$ cd /path/to/ufs_tcdiags/venv
   user@host:$ ./install.sh

The above step will build the Python virtual environment. To execute
within the Python virtual environment, do as follows.

.. code-block:: bash

   user@host:$ source setup.sh
   (venv) user@host:$
  
The above step establishes the Python virtual environment and all
dependent module paths.

Container Environments
======================

A Docker container environment, supporting and within which the
``ufs_tcdiags`` applications can be executed, may be obtained and
executed as follows.

.. code-block:: bash

   user@host:$ /path/to/docker ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_tcdiags:latest
   user@host:$ /path/to/docker container run -it ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_tcdiags:latest
     
.. toctree::
   :hidden:
   :maxdepth: 1

   apps.rst
   tcinfo.rst
   ohc.rst
   tc.rst
   tcpi.rst
   metrics.rst
   references.rst

