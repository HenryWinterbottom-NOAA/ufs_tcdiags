# File: Docker/ufs_containers.ufs_utils.dockerfile
# Author: Henry R. Winterbottom
# Date: 27 August 2023
# Version: 0.0.1
# License: LGPL v2.1

# This Docker recipe file builds a Docker image containing the
# following packages:

# - `ufs_pyutils`;
# - `ufs_diags`; 
# - `ufs_tcdiags`.

# -------------------------
# * * * W A R N I N G * * *
# -------------------------

# It is STRONGLY urged that users do not make modifications below this
# point; changes below are not supported.

# ----

FROM ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_pyutils:latest
ARG DEBIAN_FRONTEND=noninteractive
ENV UFS_DIAGS_GIT_URL="https://www.github.com/HenryWinterbottom-NOAA/ufs_diags.git"
ENV UFS_DIAGS_GIT_BRANCH="develop"
ENV UFS_TCDIAGS_GIT_URL="https://www.github.com/HenryWinterbottom-NOAA/ufs_tcdiags.git"
ENV UFS_TCDIAGS_GIT_BRANCH="develop"

ENV TZ=Etc/UTC

RUN $(which apt-get) update -y && \
    $(which apt-get) install -y --no-install-recommends && \
    $(which apt-get) install -y gfortran && \
    $(which apt-get) install -y git-all && \
    $(which rm) -rf /var/lib/apt/lists/*

RUN $(which pip) install jupyterlab && \
    $(which pip) install notebook && \
    $(which pip) install pyspharm==1.0.9 && \
    $(which pip) install tcpypi && \
    cd /opt && \
    $(which git) clone --recursive ${UFS_DIAGS_GIT_URL} --branch ${UFS_DIAGS_GIT_BRANCH} && \
    cd /opt/ufs_diags && \
    $(which pip) install -r requirements.txt && \
    cd /home && \
    $(which git) clone --recursive ${UFS_TCDIAGS_GIT_URL} --branch ${UFS_TCDIAGS_GIT_BRANCH}

ENV PYTHONPATH=/home/ufs_tcdiags/ush:/opt/ufs_diags/sorc/:${PYTHONPATH}
EXPOSE 8888