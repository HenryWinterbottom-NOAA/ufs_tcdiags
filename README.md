[![License](https://img.shields.io/badge/License-LGPL_v2.1-black)](https://github.com/HenryWinterbottom-NOAA/ufs_tools/blob/develop/LICENSE)
![Linux](https://img.shields.io/badge/Linux-ubuntu%7Ccentos-lightgrey)
![Python Version](https://img.shields.io/badge/Python-3.5|3.6|3.7-blue)
[![Code style: black](https://img.shields.io/badge/Code%20Style-black-purple.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/ufs-tcdiags/badge/?version=latest)](https://ufs-tcdiags.readthedocs.io/en/latest/?badge=latest)

[![Python Coding Standards](https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/pycodestyle.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags/actions/workflows/pycodestyle.yaml)
[![Container Builds](https://github.com/HenryWinterbottom-NOAA/ufs_diags/actions/workflows/containers.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_diags/actions/workflows/containers.yaml)

# Cloning

This repository utilizes several sub-modules from various sources. To
obtain the entire system, do as follows.

~~~shell
user@host:$ /path/to/git clone --recursive https://github.com/HenryWinterbottom-NOAA/ufs_tcdiags
~~~

# Dependencies

The package dependencies and the respective repository and manual
installation attributes are provided in the table below.

<div align="left">

| Dependency Package | <div align="left">Installation Instructions</div> | 
| :-------------: | :-------------: |
| <div align="left">[`basemap`](https://matplotlib.org/basemap/)</div> | <div align="left">`pip install basemap`</div> |
| <div align="left">[`basemap-data-hires`](https://matplotlib.org/basemap/)</div> | <div align="left">`pip install basemap-data-hires`</div> |
| <div align="left">[`cmocean`](https://github.com/matplotlib/cmocean)</div> | <div align="left">`pip install cmocean`</div> |
| <div align="left">[`jupyterlab`](https://jupyter.org)</div> | <div align="left">`pip install jupyterlab`</div> |
| <div align="left">[`matplotlib`](https://matplotlib.org/)</div> | <div align="left">`pip install matplotlib`</div> | 
| <div align="left">[`mycolorpy`](https://github.com/binodbhttr/mycolorpy)</div> | <div align="left">`pip install mycolorpy`</div> |
| <div align="left">[`notebook`](https://github.com/jupyter/notebook)</div> | <div align="left">`pip install notebook`</div> |
| <div align="left">[`pyahocorasick`](https://github.com/WojciechMula/pyahocorasick) | <div align="left">`pip install pyahocorasick`</div> |
| <div align="left">[`tcmarkers`](https://github.com/abrammer/tc_markers)</div> | <div align="left">`pip install tcmarkers`</div> |
| <div align="left">[`tcpyPI`](https://github.com/dgilford/tcpyPI)</div> | <div align="left">`pip install tcpypi`</div> |
| <div align="left">[`ufs_diags`](https://github.com/HenryWinterbottom-NOAA/ufs_diags)</div> | <div align="left">`pip install git+https://www.github.com/HenryWinterbottom-NOAA/ufs_diags.git`</div> |
| <div align="left">[`ufs_obs`](https://github.com/HenryWinterbottom-NOAA/ufs_obs)</div> | <div align="left">`pip install git+https://www.github.com/HenryWinterbottom-NOAA/ufs_obs.git`</div> |

</div>

# Installing Package Dependencies

In order to install the respective Python packages upon which
`ufs_tcdiags` is dependent, do as follows.

~~~shell
user@host:$ cd /path/to/ufs_tcdiags
user@host:$ /path/to/pip install update
user@host:$ /path/to/pip install -r /path/to/ufs_tcdiags/requirements.txt
~~~

For additional information using `pip` and `requirements.txt` type files, see [here](https://pip.pypa.io/en/stable/reference/requirements-file-format/).

# Docker Containers

A Docker container containing the latest supported image can be
obtained as follows.

~~~shell
user@host:$ /path/to/docker pull ghrc.io/henrywinterbottom-noaa/ubuntu20.04.ufs_tcdiags:latest
~~~

The Docker container may then be used as follows.

~~~shell
user@host:$ /path/to/docker container run -it ghrc.io/henrywinterbottom-noaa/ubuntu20.04.ufs_tcdiags:latest
user@host:$ cd /home/ufs_tcdiags
~~~

# Running Jupyter Notebooks from Docker

The Jupyter notebooks may be launched from within the Docker container as follows.

~~~shell
user@host:$ /path/to/docker container run -it ghrc.io/henrywinterbottom-noaa/ubuntu20.04.ufs_tcdiags:latest
user@host:$ cd /home/ufs_tcdiags/jupyter/notebooks
user@host:$ /path/to/jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root <notebook>
user@host:$ export UFS_TCDIAGS=/home/ufs_tcdiags
~~~

This action will produce a local HTML path and an associated token as
follows.

~~~shell
To access the server, open this file in a browser:
    file:///root/.local/share/jupyter/runtime/jpserver-21362-open.html
Or copy and paste one of these URLs:
    http://5186640b39b0:8889/tree?token=abcdefghijklmnopqrstuvwxwy0123456789ABCDEFGHIJKL
    http://127.0.0.1:8889/tree?token=abcdefghijklmnopqrstuvwxwy0123456789ABCDEFGHIJKL
~~~~

Copy the paste the token attribute beginning with
``http://127.0.0.1:8889`` into a web browser address bar and execute
the respective Jupyter notebook(`<notebook`> above) as usual.

# Forking

If a user wishes to contribute modifications done within their
respective fork(s) to the authoritative repository, we request that
the user first submit an issue and that the fork naming conventions
follow those listed below.

- `docs/user_branch_name`: Documentation additions and/or corrections for the application(s).

- `feature/user_branch_name`: Additions, enhancements, and/or upgrades for the application(s).

- `fix/user_branch_name`: Bug-type fixes for the application(s) that do not require immediate attention.

- `hotfix/user_branch_name`: Bug-type fixes which require immediate attention to fix issues that compromise the integrity of the respective application(s). 

