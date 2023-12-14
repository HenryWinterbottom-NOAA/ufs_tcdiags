Tropical Cyclone Input Files
============================

For the respective tropical cyclone (TC) relative and related
applications, the respective TC attributes must be specified and
written to a YAML-formatted file so that the diagnostic packages can
utilize the information. A script to generate this file from the
relevant TC information/observation files is provided and may be
executed as follows.

.. code-block:: bash

   user@host:$ cd /path/to/ufs_tcdiags/scripts
   user@host:$ ./tcinfo_yaml.py --help

   Usage: tcinfo_yaml.py [-h] [-atcf] input yaml

   Tropical cyclone information input files interface.

   Positional Arguments:
     input       An input file, of a supported type, containing the TC information to be formatted.
     yaml        Path to the YAML-formatted TC information attributes file.

   Optional Arguments:
     -h, --help  Show this help message and exit.
     -atcf       TC information collected from an ATCF (e.g., TC-vitals) formatted file.

The following TC observation data-formats are supported.

.. list-table::
   :widths: auto
   :header-rows: 1

   * - **Data Format**
     - **Description/Reference**
   * - `ATCF <https://www.nrlmry.navy.mil/atcf_web/docs/database/new/abdeck.txt>`_
     - `Automated Tropical Cyclone Forecast <https://journals.ametsoc.org/view/journals/wefo/5/4/1520-0434_1990_005_0653_tatcfs_2_0_co_2.xml>`_

TC attributes may be collected from multiple sources, and the resulting
YAML-formatted files may be concatenated together so that TC
diagnostics may be computed using TC attributes collected from the
different supported sources.

Generating the YAML-formatted files from the supported data sources
is described in the remainder of this section.

^^^^^^^^^^^^^^^^^
ATCF Applications
^^^^^^^^^^^^^^^^^

An example using ATCF-formatted input files is as follows.

.. code-block:: bash

   user@host:$ cd /path/to/ufs_tcdiags/scripts
   user@host:$ ./tcinfo_yaml.py --help

   Usage: tcinfo_yaml.py [-h] [-atcf] input yaml

   Tropical cyclone information input files interface.

   Positional Arguments:
     input       An input file, of a supported type, containing the TC information to be formatted.
     yaml        Path to the YAML-formatted TC information attributes file.

   Optional Arguments:
     -h, --help  Show this help message and exit.
     -atcf       TC information collected from an ATCF (e.g., TC-vitals) formatted file.

   user@host:$ ./tcinfo_yaml.py /path/to/atcf_input_file /path/to/output/tcinfo_yaml_file -atcf

Consider the following ATCF record, e.g., ``/path/to/atcf_input_file``.

.. code-block:: bash

   JTWC 06P ULA       20160101 0000 167S 1704W 230 032 0956 1003 0333 46 018 0148 0195 0185 0130 
   NHC  09C NINE      20160101 0000 027N 1781W 280 036 1001 1007 0389 15 083 -999 -999 -999 -999

The resulting YAML-formatted file, i.e.,
``/path/to/output/tcinfo_yaml_file``, is as follows.

.. code-block:: yaml

  06P:
    lat_deg: -16.7
    lon_deg: 170.4
  09C:
    lat_deg: 2.7
    lon_deg: 178.1
