Applications Execution
======================

The driver script for the respective diagnostics is ``/path/to/ufs_tcdiags/compute_tcdiags.py``. It can be executed as follows.

.. code-block:: bash

   user@host:$ cd /path/to/ufs_tcdiags/scripts
   user@host:$ ./compute_tcdiags.py --help

   Usage: compute_tcdiags.py [-h] [-plot] [-output] [-tcmsi] [-tcpi] [-tcohc] [-tcstrflw] yaml

   Tropical cyclone diagnostics interface.

   Positional Arguments:
     yaml        YAML-formatted tropical cyclone diagnostics configuration file.

   Optional Arguments:
     -h, --help  show this help message and exit
     -plot       Plot the specified figures for the respective applications.
     -output     Write netCDF-formatted files containing the diagnostic and derived quantities for the respective applications.
     -tcmsi      YAML-formatted file containing the TC multi-scale intensity application configuration.
     -tcpi       YAML-formatted file containing the TC potential intensity application configuration.
     -tcohc      YAML-formatted file containing the TC relative ocean heat-content application configuration.
     -tcstrflw   YAML-formatted file containing the TC steering application configuration.

Note that both atmosphere and ocean diagnostic applications are included. The available atmosphere diagnostics applications can be executed in series as follows.

.. code-block:: bash

   user@host:$ ./compute_tcdiags.py /path/to/ufs_tcdiags/patm/atmos.demo.yaml -tcmsi -tcpi -tcstrflw

If the user wants to write netCDF-formatted output files and plot specified figures, they may append the above command as follows.

.. code-block:: bash

   user@host:$ ./compute_tcdiags.py /path/to/ufs_tcdiags/patm/atmos.demo.yaml -tcmsi -tcpi -tcstrflw -output -plot

Ocean diagnostics can be executed in a similar fashion as follows.

.. code-block:: bash

   user@host:$ ./compute_tcdiags.py /path/to/ufs_tcdiags/patm/ocean.demo.yaml -tcohc -output -plot
