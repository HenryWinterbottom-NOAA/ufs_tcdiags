[![License](https://img.shields.io/badge/License-LGPL_v2.1-black)](https://github.com/HenryWinterbottom-NOAA/ufs_tools/blob/develop/LICENSE)
![Linux](https://img.shields.io/badge/Linux-ubuntu%7Ccentos-lightgrey)
![Python Version](https://img.shields.io/badge/Python-3.5|3.6|3.7-blue)
[![Code style: black](https://img.shields.io/badge/Code%20Style-black-purple.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/ufs-tcdiags/badge/?version=latest)](https://ufs-tcdiags.readthedocs.io/en/latest/?badge=latest)

[![Dependencies](https://img.shields.io/badge/Dependencies-geopy-orange)](https://github.com/geopy/geopy)
[![](https://img.shields.io/badge/jupyterlab-orange)](https://jupyter.org/)
[![](https://img.shields.io/badge/metpy-orange)](https://github.com/Unidata/MetPy)
[![](https://img.shields.io/badge/notebook-orange)](https://github.com/jupyter/notebook)
[![](https://img.shields.io/badge/pyspharm-orange)](https://pypi.org/project/pyspharm/)
[![](https://img.shields.io/badge/tcpypi-orange)](https://github.com/dgilford/tcpyPI)
[![](https://img.shields.io/badge/ufs__diags-orange)](https://github.com/HenryWinterbottom-NOAA/ufs_diags)
[![](https://img.shields.io/badge/ufs__pyutils-orange)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils)
[![](https://img.shields.io/badge/wrf--python-orange)](https://github.com/NCAR/wrf-python)

[![Python Coding Standards](https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/pycodestyle.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/pycodestyle.yaml)
[![Virtual Environment](https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/venv.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/venv.yaml)
[![Container Builds](https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/containers.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/containers.yaml)

# Cloning

This repository utilizes several sub-modules from various sources. To
obtain the entire system, do as follows.

```shell
user@host:$ /path/to/git clone --recursive https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags
```

# Docker Containers

A Docker container containing the latest supported image can be
obtained as follows.

```bash
user@host:$ /path/to/docker pull ghrc.io/henrywinterbottom-noaa/ubuntu20.04.ufs_tcdiags:latest
```

The Docker container may then be used as follows.

```bash
user@host:$ /path/to/docker container run -v /path/to/work:/work -it ghrc.io/henrywinterbottom-noaa/ubuntu20.04.ufs_tcdiags:latest
user@host:$ cd /home/ufs_tcdiags
```

In the above example, the `/path/to/work:/work` is the local directory
path (`/path/to/work`) to be bound to the Docker container directory
`/work`.

# Virtual Environments

A virtual environment supporting the respective applications can be
defined as follows.

```bash
user@host:$ cd /path/to/ufs_tcdiags/venv
user@host:$ /path/to/python -m venv /path/to/virtual_environment
user@host:$ cd /path/to/virtual_environment
user@host:$ 
```

# Forking

If a user wishes to contribute modifications done within their
respective fork(s) to the authoritative repository, we request that
the user first submit an issue and that the fork naming conventions
follow those listed below.

- `docs/user_branch_name`: Documentation additions and/or corrections for the application(s).

- `feature/user_branch_name`: Additions, enhancements, and/or upgrades for the application(s).

- `fix/user_branch_name`: Bug-type fixes for the application(s) that do not require immediate attention.

- `hotfix/user_branch_name`: Bug-type fixes which require immediate attention to fix issues that compromise the integrity of the respective application(s). 

