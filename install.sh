#!/usr/bin/env bash

# File: install.sh
# Author: Henry R. Winterbottom
# Date: 08 December 2023

# Description: This script installs the dependencies for the
#   `ufs_tcdiags` package and establishes the run-time environment
#   configuration.

# Usage: ./install [--install_path]

# ----

# Configure the run-time environment.
set -x -e

export INSTALL_PATH=${INSTALL_PATH:-"${HOME}"}
export BUILD_PATH=${BUILD_PATH:-"${PWD}"}

echo "Installing in path ${INSTALL_PATH}"
$(command -v pip) install --upgrade pip
$(command -v pip) install git+https://www.github.com/HenryWinterbottom-NOAA/ufs_pyutils.git --target "${INSTALL_PATH}/ufs_pyutils"
$(command -v pip) install git+https://www.github.com/HenryWinterbottom-NOAA/ufs_diags.git --target "${INSTALL_PATH}/ufs_diags"
$(command -v pip) install git+https://www.github.com/HenryWinterbottom-NOAA/ufs_obs.git --target "${INSTALL_PATH}/ufs_obs"
$(command -v pip) install -r "${BUILD_PATH}/requirements.txt"

export PYTHONPATH="${INSTALL_PATH}/ufs_pyutils/sorc:${INSTALL_PATH}/ufs_diags/sorc:${INSTALL_PATH}/ufs_obs/sorc:${PYTHONPATH}"
echo "PYTHONPATH=${PYTHONPATH}" >> "${HOME}/.bashrc"
