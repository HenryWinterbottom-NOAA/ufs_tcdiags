################################
UFS Tropical Cyclone Diagnostics
################################

The Unified Forecast System (UFS) Tropical Cyclone Diagnostics
package, henceforth ``ufs_tcdiags``, provides applications to compute
and/or perform analytic and diagnostic evaluations of tropical cyclone
related attributes.

Status: |pycs| |docker| |venv|

Links: `Code Repository <https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags>`_ | `Issues <https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/issues>`_

==========
Developers
==========

* Henry R. Winterbottom - henry.winterbottom@noaa.gov

=======
Cloning
=======

The ``ufs_tcdiags`` applications require the ``ufs_pyutils``
<https://github.com/HenryWinterbottom-NOAA/ufs_pyutils>`_ and ``ufs_diags`` <https://github.com/HenryWinterbottom-NOAA/ufs_diags>`_ packages. The
``ufs_tcdiags`` can be cloned as follows.

.. code-block:: console

   user@host:$ git clone https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags

====================
Package Dependencies
====================

* `UFS Python Utilities <https://github.com/HenryWinterbottom-NOAA/ufs_pyutils>`_
* `UFS Diagnostics <https://github.com/HenryWinterbottom-NOAA/ufs_diags>`_

==============================
Installing Python Dependencies
==============================

.. code-block:: console

   user@host:$ /path/to/pip install -r /path/to/ufs_tcdiags/requirements.txt

======================
Container Environments
======================

.. code-block:: console

   user@host:$ cd Docker
   user@host:$ /path/to/singularity build ufs_tcdiags.sif ./ubuntu20.04-miniconda_ufs_pyutils.ufs_tcdiags.def
   
============
Applications
============

.. toctree:: 
   :numbered:
   :maxdepth: 1

   tcpi.rst

.. |pycs| image:: https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/pycodestyle.yaml/badge.svg
    :alt: Python Coding Standards
    :scale: 100%
    :target: https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/pycodestyle.yaml

.. |docker| image:: https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/containers.yaml/badge.svg
    :alt: Docker Images
    :scale: 100%
    :target: https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/containers.yaml

.. |venv| image:: https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/venv.yaml/badge.svg
    :alt: Python Virtual Environment
    :scale: 100%
    :target: https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/venv.yaml
