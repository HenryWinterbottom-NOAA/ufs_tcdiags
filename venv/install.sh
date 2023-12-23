#!/usr/bin/env bash

# File: install.sh
# Author: Henry R. Winterbottom
# Date: 12 December 2023

# Description: This script installs the dependencies for the
#   `ufs_diags` package and establishes the run-time environment
#   configuration.

# Usage: ./install

# Imported Environment Variables

# INSTALL_PATH: The directory tree path to the `ufs_diags` GitHub
#   clone; if not specified this defaults to `${PWD}`.

# ----

# Configure the run-time environment.
set -x -e

export INSTALL_PATH=${INSTALL_PATH:-"${PWD}/../"}
export VENV_PATH="${INSTALL_PATH}/venv"

echo "Installing in path ${INSTALL_PATH}"
$(command -v python3) -m venv .
export F77=/usr/local/opt/gfortran/bin/gfortran
export FC="${F77}"
$(command -v mkdir) -p "${VENV_PATH}/dependencies"
$(command -v pip) install --upgrade pip
$(command -v git) clone --recursive http://www.github.com/henrywinterbottom-noaa/ufs_pyutils --branch develop "${VENV_PATH}/dependencies/ufs_pyutils"
$(command -v pip) install -r "${VENV_PATH}/dependencies/ufs_pyutils/requirements.txt"
$(command -v pip) install -r "${INSTALL_PATH}/requirements.txt"
$(command -v git) clone --recursive http://www.github.com/henrywinterbottom-noaa/ufs_diags --branch develop "${VENV_PATH}/dependencies/ufs_diags"
$(command -v pip) install -r "${VENV_PATH}/dependencies/ufs_diags/requirements.txt"
$(command -v pip) install -r "${INSTALL_PATH}/requirements.txt"

