#!/usr/bin/env bash

# File: install.sh
# Author: Henry R. Winterbottom
# Date: 23 December 2023

# Description: This script installs the dependencies for the
#   `ufs_diags` package and establishes the run-time environment
#   configuration.

# Usage: ./install.sh

# Imported Environment Variables:

#   - INSTALL_PATH: The installation path for the `ufs_tcdiags` GitHub
#       clone; defaults to `${PWD}`.

#   - FC: The FORTRAN compiler to be used for building the dependency
#       packages; defaults to `gfortran`.

# ----

# Configure the run-time environment.
set -x -e
export INSTALL_PATH=${INSTALL_PATH:-"${PWD}/../"}
export FC=${FC:-$(command -v which) gfortran}
export VENV_PATH="${INSTALL_PATH}/venv"
export F77="${FC}"

# Build the virtual environment.
echo "Installing in path ${INSTALL_PATH}"
$(command -v python3) -m venv .
# shellcheck disable=SC1091
source "${VENV_PATH}/bin/activate"
$(command -v pip) install --upgrade pip
$(command -v mkdir) -p "${VENV_PATH}/dependencies"
$(command -v git) clone --recursive http://www.github.com/henrywinterbottom-noaa/ufs_pyutils --branch develop "${VENV_PATH}/dependencies/ufs_pyutils"
$(command -v pip) install -r "${VENV_PATH}/dependencies/ufs_pyutils/requirements.txt"
$(command -v pip) install -r "${INSTALL_PATH}/requirements.txt"
$(command -v git) clone --recursive http://www.github.com/henrywinterbottom-noaa/ufs_diags --branch develop "${VENV_PATH}/dependencies/ufs_diags"
$(command -v pip) install -r "${VENV_PATH}/dependencies/ufs_diags/requirements.txt"
$(command -v pip) install -r "${INSTALL_PATH}/requirements.txt"

# Build the wrapper script for the virtual environment.
echo "Building script ${VENV_PATH}/setup.sh"
cat >> "${VENV_PATH}/setup.sh" <<EOF
#!/usr/bin/env bash
source "${VENV_PATH}/bin/activate"
export TCDIAGS_ROOT="${INSTALL_PATH}"
export PYTHONPATH="${VENV_PATH}/dependencies/ufs_pyutils:${VENV_PATH}/dependencies/ufs_diags:${INSTALL_PATH}:${INSTALL_PATH}/tcdiags/plot"
EOF
$(command -v chmod) +x "${VENV_PATH}/setup.sh"
