Application Inputs
==================

Atmosphere Applications
-----------------------

The atmosphere applications are defined within a YAML-formatted
configuration file. The following variables are required for each
atmosphere analysis.

.. list-table::
   :align: left
   :widths: auto
   :header-rows: 1

   * - **Variable**
     - **Description**
   * - ``height``
     - Geometric height profiles
   * - ``latitude``
     - Latitude geographical coordinate
   * - ``longitude``
     - Longitude geographical coordinate
   * - ``pressure``
     - Pressure profiles
   * - ``sea_level_pressure``
     - Sea-level pressure
   * - ``specific_humidity``
     - Specific humidity
   * - ``surface_height``
     - Topography/surface elevation
   * - ``surface_pressure``
     - Surface pressure
   * - ``temperature``
     - Temperature profiles
   * - ``uwind``
     - Zonal wind profiles
   * - ``vwind``
     - Meridional wind profiles

An example of a configuration for reading the prognostic variables for
a GFS analysis is as follows.

.. code-block:: yaml

   io_class: ReadAnalysis
   io_module: tcdiags.io.read_analysis
   ncfile: &gfs_ncfile !ENV ${TCDIAGS_ROOT}/C96_era5anl_2016100100.nc
   schema: !ENV ${TCDIAGS_ROOT}/parm/schema/tcdiags.read_analysis.gfs.yaml

   height:
     derived: true
     method: height_from_pressure
     module: diags.derived.atmos.heights
     units: m
   latitude:
     flip_lat: &flip_lat true
     ncfile: *gfs_ncfile
     ncvarname: lat
     units: degree
   longitude:
     flip_lat: *flip_lat
     ncfile: *gfs_ncfile
     ncvarname: lon
     scale_add: -360.0
     units: degree
   pressure:
     derived: true
     flip_lat: *flip_lat
     flip_z: &flip_z true
     method: pressure_from_thickness
     module: diags.derived.atmos.pressures
     ncfile: *gfs_ncfile
     ncvarname: dpres
     squeeze: &squeeze true
     squeeze_axis: &squeeze_axis 0
     units: pascals
   sea_level_pressure:
     derived: true
     method: pressure_to_sealevel
     module: diags.derived.atmos.pressures
     units: pascal
   specific_humidity:
     flip_lat: *flip_lat
     flip_z: *flip_z
     ncfile: *gfs_ncfile
     ncvarname: spfh
     squeeze: *squeeze
     squeeze_axis: *squeeze_axis
     units: kg/kg
   surface_height:
     flip_lat: *flip_lat
     ncfile: *gfs_ncfile
     ncvarname: hgtsfc
     scale_mult: 0.98
     squeeze: *squeeze
     squeeze_axis: *squeeze_axis
     units: gpm
   surface_pressure:
     flip_lat: *flip_lat
     ncfile: *gfs_ncfile
     ncvarname: pressfc
     squeeze: *squeeze
     squeeze_axis: *squeeze_axis
     units: pascals
   temperature:
     flip_lat: *flip_lat
     flip_z: *flip_z
     ncfile: *gfs_ncfile
     ncvarname: tmp
     squeeze: *squeeze
     squeeze_axis: *squeeze_axis
     units: K
   uwind:
     flip_lat: *flip_lat
     flip_z: *flip_z
     ncfile: *gfs_ncfile
     ncvarname: ugrd
     squeeze: *squeeze
     squeeze_axis: *squeeze_axis
     units: mps
   vwind:
     flip_lat: *flip_lat
     flip_z: *flip_z
     ncfile: *gfs_ncfile
     ncvarname: vgrd
     squeeze: *squeeze
     squeeze_axis: *squeeze_axis
     units: mps

The following table describes the respective variable
attributes. Variables without a default value indicate required
configuration variables. All references to ``module`` and ``method``
are relative to the `UFS diagnostics API
<https://ufs-diags.readthedocs.io/en/latest/>`_ applications.

.. list-table::
   :align: left
   :widths: auto
   :header-rows: 1

   * - **Variable**
     - **Description**
     - **Data Type**
     - **Default Value**
   * - `derived`
     - Whether the variable is derived
     - ``bool``
     - ``false``
   * - `flip_lat`
     - Whether latitude is flipped
     - ``bool``
     - ``false``
   * - `flip_z`
     - Whether z-axis is flipped
     - ``bool``
     - ``false``
   * - `method`
     - `UFS diagnostics API <https://ufs-diags.readthedocs.io/en/latest/>`_ method used for derivation (if applicable)
     - ``str``
     - 
   * - `module`
     - `UFS diagnostics API <https://ufs-diags.readthedocs.io/en/latest/>`_ module used for derivation (if applicable)
     - ``str``
     - 
   * - `ncfile`
     - Path to the netCDF-formatted file
     - ``str``
     - 
   * - `scale_mult`
     - Scaling factor (if applicable)
     - ``float``
     - 1.0
   * - `scale_add`
     - Scaling offset (if applicable)
     - ``float``
     - 0.0
   * - `squeeze`
     - Whether the netCDF variable dimensions are to be squeezed; see ``squeeze_axis``
     - ``bool``
     - ``false``
   * - `squeeze_axis`
     - netCDF variable axis to squeeze (if applicable)
     - ``int``
     - 0
   * - `ncvarname`
     - Variable name in the netCDF-formatted file
     - ``str``
     - 
   * - `units`
     - Units of the netCDF prognostic variable; these must be of a unit available within the `pint <https://github.com/hgrecco/pint>`_ unit registry
     - ``str``
     - 

The following variables should not be changed by the user.

- ``io_module``: Specifies the input/output module as ``tcdiags.io.read_analysis``.
- ``io_class``: Specifies the class within the module as ``ReadAnalysis``.
- ``schema``: Specifies the schema file for reading the GFS analysis data.
