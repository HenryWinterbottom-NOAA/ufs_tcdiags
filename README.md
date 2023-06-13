[![License](https://img.shields.io/badge/license-LGPL_v2.1-black)](https://github.com/HenryWinterbottom-NOAA/ufs_tools/blob/develop/LICENSE)
![Linux](https://img.shields.io/badge/linux-ubuntu%7Ccentos-lightgrey)
![Python Version](https://img.shields.io/badge/python-3.5|3.6|3.7-blue)

[![Dependencies](https://img.shields.io/badge/dependencies-ufs__pyutils-orange)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils)

[![Python Coding Standards](https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/pycodestyle.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/pycodestyle.yaml)
[![Container Builds](https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/containers.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/containers.yaml)
[![Python Virtual Environments](https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/venv.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/venv.yaml)

# Cloning

This repository utilizes several sub-modules from various sources. To
obtain the entire system, do as follows.

~~~
user@host:$ git clone https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags
~~~

# Building the Documentation

The documentation, using the
[Sphinx](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html)
documentation generator, can be compiled as follows.

~~~
user@host:$ cd docs
user@host:$ make html
~~~

The documentation will then be available within the local
`docs/build/html` path.

# Forking

If a user wishes to contribute modifications done within their
respective fork(s) to the authoritative repository, we request that
the user first submit an issue and that the fork naming conventions
follow those listed below.

- `docs/user_branch_name`: Documentation additions and/or corrections for the application(s).

- `feature/user_branch_name`: Additions, enhancements, and/or upgrades for the application(s).

- `fix/user_branch_name`: Bug-type fixes for the application(s) that do not require immediate attention.

- `hotfix/user_branch_name`: Bug-type fixes which require immediate attention to fix issues that compromise the integrity of the respective application(s). 

