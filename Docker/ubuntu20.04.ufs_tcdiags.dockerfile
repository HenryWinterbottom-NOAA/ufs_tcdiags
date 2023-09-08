# File: Docker/ufs_containers.ufs_utils.dockerfile
# Author: Henry R. Winterbottom
# Date: 27 August 2023
# License: LGPL v2.1

# -------------------------
# * * * W A R N I N G * * *
# -------------------------

# It is STRONGLY urged that users do not make modifications below this
# point; changes below are not supported.

# -------------------------
# * * * W A R N I N G * * *
# -------------------------

FROM ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_diags:latest
ARG DEBIAN_FRONTEND=noninteractive
ENV UFS_TCDIAGS_GIT_URL="https://www.github.com/HenryWinterbottom-NOAA/ufs_tcdiags.git"
ENV UFS_TCDIAGS_GIT_BRANCH="develop"
ENV TCDIAGS_ROOT="/home/ufs_tcdiags"

ENV TZ=Etc/UTC

RUN $(which apt-get) update -y && \
    $(which apt-get) install -y --no-install-recommends && \
    $(which apt-get) install -y git-all && \
    $(which rm) -rf /var/lib/apt/lists/*

RUN $(which git) clone --recursive ${UFS_TCDIAGS_GIT_URL} --branch ${UFS_TCDIAGS_GIT_BRANCH} ${TCDIAGS_ROOT} && \
    $(which pip) install -r ${TCDIAGS_ROOT}/requirements.txt

ENV PYTHONPATH=${TCDIAGS_ROOT}/ush:${TCDIAGS_ROOT}/jupyter/ush:/opt/ufs_diags/:${PYTHONPATH}
EXPOSE 8888