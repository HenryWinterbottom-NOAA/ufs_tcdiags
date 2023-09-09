File: jupyter/notebooks/tcdiags.vurk2014_msi.ipynb

Author: Henry R. Winterbottom

Date: 27 August 2023

Version: 0.0.1

License: LGPL v2.1

Topic: This notebook computes and plots tropical cyclone (TC) multi-scale intensity (MSI) attributes described by Vukicevic et al., [2014].

References:

    Vukicevic, T., E., Uhlhorn, P. Reasor, and B. Klotz, A novel multiscale intensity metric for evaluation of tropical cyclone intensity forecasts, J. Atmos. Sci., 71 (4), 1292-13-4, 2014.


```python
from collections import OrderedDict

from tcdiags.tcdiags import TCDiags
import matplotlib.cm as colormaps
import matplotlib.pyplot as plt

import numpy
from ioapps import netcdf4_interface
from IPython.display import HTML, display
from tabulate import tabulate
from tools import parser_interface
```

### User Configuration


```python
# YAML-formatted configuration file.
yaml = "/home/ufs_tcdiags/parm/tcdiags.demo.yaml"

# Define the TC MSI plotting attributes for the total wind and wave-number 0.
vmax_cint = 5.0
vmax_cmax = 30.0
vmax_cmin = 0.0
vmax_cmap = "jet"
vmax_levels = numpy.linspace(vmax_cmin, vmax_cmax, 255)

# Define the TC MSI plotting attributes for the wave-number 1 - wave-number N fields.
wn_cint = 1.0
wn_cmax = 5.0
wn_cmin = -5.0
wn_cmap = "seismic"
wn_levels = numpy.linspace(wn_cmin, wn_cmax, 255)

# Define the TC MSI attributes stored as netCDF global attributes; 
# this dictionary contains the global attribute name and the corresponding units.
tcmsi_attrs_dict = OrderedDict({"lat_deg":{"name": "Center Latitude", "units": "degrees"},
                                "lon_deg":{"name": "Center Longitude", "units": "degrees"},
                                "lat_rmw": {"name": "Radius of Maximum Wind Latitude", "units": "degrees"},
                                "lon_rmw": {"name": "Radius of Maximum Wind Longitude", "units": "degrees"},
                                "vmax": {"name": "Maximum 10-meter Wind Speed", "units": "mps"},
                                "rmw_azimuth": {"name": "Azimuth of Maximum 10-meter Wind Speed", "units": "degrees"},
                                "rmw_radius": {"name": "Radius of Maximum 10-meter Wind Speed", "units": "m"},
                                "wn0_msi": {"name": "Wavenumber-0 Maximum Wind Speed", "units": "mps"},
                                "wn1_msi": {"name": "Wavenumber-1 Maximum Wind Speed", "units": "mps"},
                                "wn0p1_msi": {"name": "Wavenumbers (0+1) Maximum Wind Speed", "units": "mps"},
                                "epsi_msi": {"name": "Residual Wavenumber Maximum Wind Speed", "units": "mps"},
                                }
                              )
```

### Compute the tropical cyclone multi-scale intensity attributes.


```python
options_obj = parser_interface.object_define()
options_obj.yaml = yaml
options_obj.tcmsi = True
tcdiag_obj = TCDiags(options_obj=options_obj)
tcmsi = tcdiag_obj.run().tcmsi
```

    [38;5;226m2023-09-06 14:37:08 :: WARNING :: utils.schema_interface: Schema optional value derived has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:08 :: WARNING :: utils.schema_interface: Schema optional value method has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:08 :: WARNING :: utils.schema_interface: Schema optional value module has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:08 :: WARNING :: utils.schema_interface: Schema optional value scale_mult has not been defined; setting to default value 1.0.[0m
    [38;5;226m2023-09-06 14:37:08 :: WARNING :: utils.schema_interface: Schema optional value scale_add has not been defined; setting to default value 0.0.[0m
    [37;21m2023-09-06 14:37:08 :: INFO :: utils.schema_interface: 
    
    +--------------+--------+------------+-----------------+---------------------------------------------+
    |   Variable   |  Type  |  Optional  | Default Value   | Assigned Value                              |
    +==============+========+============+=================+=============================================+
    |  scale_add   | float  |    True    | 0.0             | 0.0                                         |
    |    units     |  str   |   False    |                 | kg/kg                                       |
    |   flip_lat   |  bool  |    True    | False           | True                                        |
    |    ncfile    |  str   |    True    |                 | /home/ufs_tcdiags/C96_era5anl_2016100100.nc |
    |   derived    |  bool  |    True    | False           | False                                       |
    |   squeeze    |  bool  |    True    | False           | True                                        |
    | squeeze_axis |  int   |    True    | 0               | 0                                           |
    |    flip_z    |  bool  |    True    | False           | True                                        |
    |  ncvarname   |  str   |    True    |                 | spfh                                        |
    |  scale_mult  | float  |    True    | 1.0             | 1.0                                         |
    |     name     |  str   |   False    |                 | spfh                                        |
    +--------------+--------+------------+-----------------+---------------------------------------------+
    
    [0m
    [37;21m2023-09-06 14:37:08 :: INFO :: utils.schema_interface: Schema successfully validated.[0m
    [37;21m2023-09-06 14:37:08 :: INFO :: tcdiags.io.vario: Reading variable specific_humidity from netCDF-formatted file path /home/ufs_tcdiags/C96_era5anl_2016100100.nc.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: tcdiags.io.vario: Flipping array along the vertical axis.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: tcdiags.io.vario: Flipping array along the latitudinal axis.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value derived has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value method has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value module has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value scale_mult has not been defined; setting to default value 1.0.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value scale_add has not been defined; setting to default value 0.0.[0m
    [37;21m2023-09-06 14:37:09 :: INFO :: utils.schema_interface: 
    
    +--------------+--------+------------+-----------------+---------------------------------------------+
    |   Variable   |  Type  |  Optional  | Default Value   | Assigned Value                              |
    +==============+========+============+=================+=============================================+
    |  scale_add   | float  |    True    | 0.0             | 0.0                                         |
    |     name     |  str   |   False    |                 | uwnd                                        |
    |   flip_lat   |  bool  |    True    | False           | True                                        |
    |    ncfile    |  str   |    True    |                 | /home/ufs_tcdiags/C96_era5anl_2016100100.nc |
    |   derived    |  bool  |    True    | False           | False                                       |
    |   squeeze    |  bool  |    True    | False           | True                                        |
    | squeeze_axis |  int   |    True    | 0               | 0                                           |
    |    flip_z    |  bool  |    True    | False           | True                                        |
    |  ncvarname   |  str   |    True    |                 | ugrd                                        |
    |  scale_mult  | float  |    True    | 1.0             | 1.0                                         |
    |    units     |  str   |   False    |                 | mps                                         |
    +--------------+--------+------------+-----------------+---------------------------------------------+
    
    [0m
    [37;21m2023-09-06 14:37:09 :: INFO :: utils.schema_interface: Schema successfully validated.[0m
    [37;21m2023-09-06 14:37:09 :: INFO :: tcdiags.io.vario: Reading variable uwind from netCDF-formatted file path /home/ufs_tcdiags/C96_era5anl_2016100100.nc.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: tcdiags.io.vario: Flipping array along the vertical axis.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: tcdiags.io.vario: Flipping array along the latitudinal axis.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value derived has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value method has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value module has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value scale_mult has not been defined; setting to default value 1.0.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value scale_add has not been defined; setting to default value 0.0.[0m
    [37;21m2023-09-06 14:37:09 :: INFO :: utils.schema_interface: 
    
    +--------------+--------+------------+-----------------+---------------------------------------------+
    |   Variable   |  Type  |  Optional  | Default Value   | Assigned Value                              |
    +==============+========+============+=================+=============================================+
    |  scale_add   | float  |    True    | 0.0             | 0.0                                         |
    |  ncvarname   |  str   |    True    |                 | vgrd                                        |
    |   flip_lat   |  bool  |    True    | False           | True                                        |
    |    ncfile    |  str   |    True    |                 | /home/ufs_tcdiags/C96_era5anl_2016100100.nc |
    |   derived    |  bool  |    True    | False           | False                                       |
    |   squeeze    |  bool  |    True    | False           | True                                        |
    | squeeze_axis |  int   |    True    | 0               | 0                                           |
    |    flip_z    |  bool  |    True    | False           | True                                        |
    |  scale_mult  | float  |    True    | 1.0             | 1.0                                         |
    |    units     |  str   |   False    |                 | mps                                         |
    |     name     |  str   |   False    |                 | vwnd                                        |
    +--------------+--------+------------+-----------------+---------------------------------------------+
    
    [0m
    [37;21m2023-09-06 14:37:09 :: INFO :: utils.schema_interface: Schema successfully validated.[0m
    [37;21m2023-09-06 14:37:09 :: INFO :: tcdiags.io.vario: Reading variable vwind from netCDF-formatted file path /home/ufs_tcdiags/C96_era5anl_2016100100.nc.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: tcdiags.io.vario: Flipping array along the vertical axis.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: tcdiags.io.vario: Flipping array along the latitudinal axis.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value derived has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value method has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value module has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value scale_mult has not been defined; setting to default value 1.0.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value scale_add has not been defined; setting to default value 0.0.[0m
    [37;21m2023-09-06 14:37:09 :: INFO :: utils.schema_interface: 
    
    +--------------+--------+------------+-----------------+---------------------------------------------+
    |   Variable   |  Type  |  Optional  | Default Value   | Assigned Value                              |
    +==============+========+============+=================+=============================================+
    |  ncvarname   |  str   |    True    |                 | tmp                                         |
    |  scale_add   | float  |    True    | 0.0             | 0.0                                         |
    |   flip_lat   |  bool  |    True    | False           | True                                        |
    |    ncfile    |  str   |    True    |                 | /home/ufs_tcdiags/C96_era5anl_2016100100.nc |
    |   derived    |  bool  |    True    | False           | False                                       |
    |   squeeze    |  bool  |    True    | False           | True                                        |
    | squeeze_axis |  int   |    True    | 0               | 0                                           |
    |    flip_z    |  bool  |    True    | False           | True                                        |
    |    units     |  str   |   False    |                 | K                                           |
    |  scale_mult  | float  |    True    | 1.0             | 1.0                                         |
    |     name     |  str   |   False    |                 | temp                                        |
    +--------------+--------+------------+-----------------+---------------------------------------------+
    
    [0m
    [37;21m2023-09-06 14:37:09 :: INFO :: utils.schema_interface: Schema successfully validated.[0m
    [37;21m2023-09-06 14:37:09 :: INFO :: tcdiags.io.vario: Reading variable temperature from netCDF-formatted file path /home/ufs_tcdiags/C96_era5anl_2016100100.nc.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: tcdiags.io.vario: Flipping array along the vertical axis.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: tcdiags.io.vario: Flipping array along the latitudinal axis.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value derived has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value flip_z has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value method has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value module has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value scale_mult has not been defined; setting to default value 1.0.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value squeeze has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value squeeze_axis has not been defined; setting to default value 0.[0m
    [37;21m2023-09-06 14:37:09 :: INFO :: utils.schema_interface: 
    
    +--------------+--------+------------+-----------------+---------------------------------------------+
    |   Variable   |  Type  |  Optional  | Default Value   | Assigned Value                              |
    +==============+========+============+=================+=============================================+
    |    units     |  str   |   False    |                 | degree                                      |
    |  scale_add   | float  |    True    | 0.0             | -360.0                                      |
    |   flip_lat   |  bool  |    True    | False           | True                                        |
    |   derived    |  bool  |    True    | False           | False                                       |
    |    ncfile    |  str   |    True    |                 | /home/ufs_tcdiags/C96_era5anl_2016100100.nc |
    | squeeze_axis |  int   |    True    | 0               | 0                                           |
    |  ncvarname   |  str   |    True    |                 | lon                                         |
    |     name     |  str   |   False    |                 | lon                                         |
    |    flip_z    |  bool  |    True    | False           | False                                       |
    |  scale_mult  | float  |    True    | 1.0             | 1.0                                         |
    |   squeeze    |  bool  |    True    | False           | False                                       |
    +--------------+--------+------------+-----------------+---------------------------------------------+
    
    [0m
    [37;21m2023-09-06 14:37:09 :: INFO :: utils.schema_interface: Schema successfully validated.[0m
    [37;21m2023-09-06 14:37:09 :: INFO :: tcdiags.io.vario: Reading variable longitude from netCDF-formatted file path /home/ufs_tcdiags/C96_era5anl_2016100100.nc.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: tcdiags.io.vario: Flipping array along the latitudinal axis.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value derived has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value flip_z has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value method has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value module has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value scale_mult has not been defined; setting to default value 1.0.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value scale_add has not been defined; setting to default value 0.0.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value squeeze has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value squeeze_axis has not been defined; setting to default value 0.[0m
    [37;21m2023-09-06 14:37:09 :: INFO :: utils.schema_interface: 
    
    +--------------+--------+------------+-----------------+---------------------------------------------+
    |   Variable   |  Type  |  Optional  | Default Value   | Assigned Value                              |
    +==============+========+============+=================+=============================================+
    |    units     |  str   |   False    |                 | degree                                      |
    |  scale_add   | float  |    True    | 0.0             | 0.0                                         |
    |  ncvarname   |  str   |    True    |                 | lat                                         |
    |   flip_lat   |  bool  |    True    | False           | True                                        |
    |   derived    |  bool  |    True    | False           | False                                       |
    |    ncfile    |  str   |    True    |                 | /home/ufs_tcdiags/C96_era5anl_2016100100.nc |
    | squeeze_axis |  int   |    True    | 0               | 0                                           |
    |    flip_z    |  bool  |    True    | False           | False                                       |
    |     name     |  str   |   False    |                 | lat                                         |
    |  scale_mult  | float  |    True    | 1.0             | 1.0                                         |
    |   squeeze    |  bool  |    True    | False           | False                                       |
    +--------------+--------+------------+-----------------+---------------------------------------------+
    
    [0m
    [37;21m2023-09-06 14:37:09 :: INFO :: utils.schema_interface: Schema successfully validated.[0m
    [37;21m2023-09-06 14:37:09 :: INFO :: tcdiags.io.vario: Reading variable latitude from netCDF-formatted file path /home/ufs_tcdiags/C96_era5anl_2016100100.nc.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: tcdiags.io.vario: Flipping array along the latitudinal axis.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value derived has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value flip_z has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value method has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value module has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value scale_mult has not been defined; setting to default value 1.0.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value scale_add has not been defined; setting to default value 0.0.[0m
    [37;21m2023-09-06 14:37:09 :: INFO :: utils.schema_interface: 
    
    +--------------+--------+------------+-----------------+---------------------------------------------+
    |   Variable   |  Type  |  Optional  | Default Value   | Assigned Value                              |
    +==============+========+============+=================+=============================================+
    |  scale_add   | float  |    True    | 0.0             | 0.0                                         |
    |   flip_lat   |  bool  |    True    | False           | True                                        |
    |   derived    |  bool  |    True    | False           | False                                       |
    |    ncfile    |  str   |    True    |                 | /home/ufs_tcdiags/C96_era5anl_2016100100.nc |
    |   squeeze    |  bool  |    True    | False           | True                                        |
    | squeeze_axis |  int   |    True    | 0               | 0                                           |
    |  ncvarname   |  str   |    True    |                 | pressfc                                     |
    |    flip_z    |  bool  |    True    | False           | False                                       |
    |  scale_mult  | float  |    True    | 1.0             | 1.0                                         |
    |    units     |  str   |   False    |                 | pascals                                     |
    |     name     |  str   |   False    |                 | psfc                                        |
    +--------------+--------+------------+-----------------+---------------------------------------------+
    
    [0m
    [37;21m2023-09-06 14:37:09 :: INFO :: utils.schema_interface: Schema successfully validated.[0m
    [37;21m2023-09-06 14:37:09 :: INFO :: tcdiags.io.vario: Reading variable surface_pressure from netCDF-formatted file path /home/ufs_tcdiags/C96_era5anl_2016100100.nc.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: tcdiags.io.vario: Flipping array along the latitudinal axis.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value derived has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value flip_z has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value method has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value module has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value scale_add has not been defined; setting to default value 0.0.[0m
    [37;21m2023-09-06 14:37:09 :: INFO :: utils.schema_interface: 
    
    +--------------+--------+------------+-----------------+---------------------------------------------+
    |   Variable   |  Type  |  Optional  | Default Value   | Assigned Value                              |
    +==============+========+============+=================+=============================================+
    |  scale_add   | float  |    True    | 0.0             | 0.0                                         |
    |   flip_lat   |  bool  |    True    | False           | True                                        |
    |   derived    |  bool  |    True    | False           | False                                       |
    |    ncfile    |  str   |    True    |                 | /home/ufs_tcdiags/C96_era5anl_2016100100.nc |
    |   squeeze    |  bool  |    True    | False           | True                                        |
    | squeeze_axis |  int   |    True    | 0               | 0                                           |
    |  ncvarname   |  str   |    True    |                 | hgtsfc                                      |
    |     name     |  str   |   False    |                 | zsfc                                        |
    |    flip_z    |  bool  |    True    | False           | False                                       |
    |    units     |  str   |   False    |                 | gpm                                         |
    |  scale_mult  | float  |    True    | 1.0             | 0.98                                        |
    +--------------+--------+------------+-----------------+---------------------------------------------+
    
    [0m
    [37;21m2023-09-06 14:37:09 :: INFO :: utils.schema_interface: Schema successfully validated.[0m
    [37;21m2023-09-06 14:37:09 :: INFO :: tcdiags.io.vario: Reading variable surface_height from netCDF-formatted file path /home/ufs_tcdiags/C96_era5anl_2016100100.nc.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: tcdiags.io.vario: Flipping array along the latitudinal axis.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value scale_mult has not been defined; setting to default value 1.0.[0m
    [38;5;226m2023-09-06 14:37:09 :: WARNING :: utils.schema_interface: Schema optional value scale_add has not been defined; setting to default value 0.0.[0m
    [37;21m2023-09-06 14:37:09 :: INFO :: utils.schema_interface: 
    
    +--------------+--------+------------+-----------------+---------------------------------------------+
    |   Variable   |  Type  |  Optional  | Default Value   | Assigned Value                              |
    +==============+========+============+=================+=============================================+
    |     name     |  str   |   False    |                 | pres                                        |
    |  scale_add   | float  |    True    | 0.0             | 0.0                                         |
    |   derived    |  bool  |    True    | False           | True                                        |
    |    module    |  str   |    True    |                 | diags.derived.atmos.pressures               |
    |    method    |  str   |    True    |                 | pressure_from_thickness                     |
    |   flip_lat   |  bool  |    True    | False           | True                                        |
    |    ncfile    |  str   |    True    |                 | /home/ufs_tcdiags/C96_era5anl_2016100100.nc |
    |   squeeze    |  bool  |    True    | False           | True                                        |
    | squeeze_axis |  int   |    True    | 0               | 0                                           |
    |  ncvarname   |  str   |    True    |                 | dpres                                       |
    |    flip_z    |  bool  |    True    | False           | True                                        |
    |  scale_mult  | float  |    True    | 1.0             | 1.0                                         |
    |    units     |  str   |   False    |                 | pascals                                     |
    +--------------+--------+------------+-----------------+---------------------------------------------+
    
    [0m
    [37;21m2023-09-06 14:37:09 :: INFO :: utils.schema_interface: Schema successfully validated.[0m
    [37;21m2023-09-06 14:37:09 :: INFO :: tcdiags.io.vario: Reading variable pressure from netCDF-formatted file path /home/ufs_tcdiags/C96_era5anl_2016100100.nc.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: tcdiags.io.vario: Flipping array along the vertical axis.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: tcdiags.io.vario: Flipping array along the latitudinal axis.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value flip_lat has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value flip_z has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value ncfile has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value scale_mult has not been defined; setting to default value 1.0.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value scale_add has not been defined; setting to default value 0.0.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value squeeze has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value squeeze_axis has not been defined; setting to default value 0.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value ncvarname has not been defined; setting to default value None.[0m
    [37;21m2023-09-06 14:37:10 :: INFO :: utils.schema_interface: 
    
    +--------------+--------+------------+-----------------+-----------------------------+
    |   Variable   |  Type  |  Optional  | Default Value   | Assigned Value              |
    +==============+========+============+=================+=============================+
    |  scale_add   | float  |    True    | 0.0             | 0.0                         |
    |   derived    |  bool  |    True    | False           | True                        |
    | squeeze_axis |  int   |    True    | 0               | 0                           |
    |     name     |  str   |   False    |                 | hght                        |
    |    method    |  str   |    True    |                 | height_from_pressure        |
    |    flip_z    |  bool  |    True    | False           | False                       |
    |   flip_lat   |  bool  |    True    | False           | False                       |
    |    module    |  str   |    True    |                 | diags.derived.atmos.heights |
    |  scale_mult  | float  |    True    | 1.0             | 1.0                         |
    |   squeeze    |  bool  |    True    | False           | False                       |
    |    units     |  str   |   False    |                 | m                           |
    +--------------+--------+------------+-----------------+-----------------------------+
    
    [0m
    [37;21m2023-09-06 14:37:10 :: INFO :: utils.schema_interface: Schema successfully validated.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value flip_lat has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value flip_z has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value ncfile has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value scale_mult has not been defined; setting to default value 1.0.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value scale_add has not been defined; setting to default value 0.0.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value squeeze has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value squeeze_axis has not been defined; setting to default value 0.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value ncvarname has not been defined; setting to default value None.[0m
    [37;21m2023-09-06 14:37:10 :: INFO :: utils.schema_interface: 
    
    +--------------+--------+------------+-----------------+-------------------------------+
    |   Variable   |  Type  |  Optional  | Default Value   | Assigned Value                |
    +==============+========+============+=================+===============================+
    |  scale_add   | float  |    True    | 0.0             | 0.0                           |
    |   derived    |  bool  |    True    | False           | True                          |
    |     name     |  str   |   False    |                 | pslp                          |
    |    module    |  str   |    True    |                 | diags.derived.atmos.pressures |
    | squeeze_axis |  int   |    True    | 0               | 0                             |
    |    flip_z    |  bool  |    True    | False           | False                         |
    |   flip_lat   |  bool  |    True    | False           | False                         |
    |    method    |  str   |    True    |                 | pressure_to_sealevel          |
    |  scale_mult  | float  |    True    | 1.0             | 1.0                           |
    |   squeeze    |  bool  |    True    | False           | False                         |
    |    units     |  str   |   False    |                 | pascal                        |
    +--------------+--------+------------+-----------------+-------------------------------+
    
    [0m
    [37;21m2023-09-06 14:37:10 :: INFO :: utils.schema_interface: Schema successfully validated.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value flip_lat has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value flip_z has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value ncfile has not been defined; setting to default value None.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value scale_mult has not been defined; setting to default value 1.0.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value scale_add has not been defined; setting to default value 0.0.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value squeeze has not been defined; setting to default value False.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value squeeze_axis has not been defined; setting to default value 0.[0m
    [38;5;226m2023-09-06 14:37:10 :: WARNING :: utils.schema_interface: Schema optional value ncvarname has not been defined; setting to default value None.[0m
    [37;21m2023-09-06 14:37:10 :: INFO :: utils.schema_interface: 
    
    +--------------+--------+------------+-----------------+------------------------------+
    |   Variable   |  Type  |  Optional  | Default Value   | Assigned Value               |
    +==============+========+============+=================+==============================+
    |  scale_add   | float  |    True    | 0.0             | 0.0                          |
    |   derived    |  bool  |    True    | False           | True                         |
    |     name     |  str   |   False    |                 | mxrt                         |
    |    method    |  str   |    True    |                 | spfh_to_mxrt                 |
    |    units     |  str   |   False    |                 | kg/kg                        |
    | squeeze_axis |  int   |    True    | 0               | 0                            |
    |    flip_z    |  bool  |    True    | False           | False                        |
    |   flip_lat   |  bool  |    True    | False           | False                        |
    |  scale_mult  | float  |    True    | 1.0             | 1.0                          |
    |   squeeze    |  bool  |    True    | False           | False                        |
    |    module    |  str   |    True    |                 | diags.derived.atmos.moisture |
    +--------------+--------+------------+-----------------+------------------------------+
    
    [0m
    [37;21m2023-09-06 14:37:10 :: INFO :: utils.schema_interface: Schema successfully validated.[0m
    [37;21m2023-09-06 14:37:10 :: INFO :: tcdiags.io.vario: The geographical coordinate arrays are projected to 2-dimensions; doing nothing.[0m
    [37;21m2023-09-06 14:37:10 :: INFO :: diags.derived.atmos.pressures: Computing pressure profile array of dimension (127, 192, 384).[0m
    [37;21m2023-09-06 14:37:10 :: INFO :: diags.derived.atmos.heights: Computing the geometric height profile array of dimension (127, 192, 384).[0m
    [37;21m2023-09-06 14:37:10 :: INFO :: diags.derived.atmos.moisture: Computing the mixing ratio array of dimension (127, 192, 384).[0m
    [1;36m2023-09-06 14:37:10 :: INFO :: tcdiags.tcdiags.TCDiags: Executing application tcmsi.[0m
    [37;21m2023-09-06 14:37:11 :: INFO :: utils.schema_interface: 
    
    +--------------+--------+------------+-----------------+------------------------------+
    |   Variable   |  Type  |  Optional  | Default Value   | Assigned Value               |
    +==============+========+============+=================+==============================+
    | write_output |  bool  |    True    | False           | True                         |
    | output_file  |  str   |   False    |                 | ./tcdiags.vurk2014_msi.%s.nc |
    |    max_wn    |  int   |    True    | 3               | 3                            |
    +--------------+--------+------------+-----------------+------------------------------+
    
    [0m
    [37;21m2023-09-06 14:37:11 :: INFO :: utils.schema_interface: Schema successfully validated.[0m
    [37;21m2023-09-06 14:37:11 :: INFO :: tcdiags.diagnostics.VURK2014: Computing the wind field magnitude.[0m
    [37;21m2023-09-06 14:37:11 :: INFO :: tcdiags.diagnostics.VURK2014: Interpolating the wind field magnitude to a 10-meter elevation.[0m
    [37;21m2023-09-06 14:37:11 :: INFO :: diags.interp.ll2ra: Defining polar projection grid of resolution 40000 meters and 0.2617993877991494 radians centered at longitude coordinate -72 and latitude coordinate location 13.4.[0m
    [37;21m2023-09-06 14:37:42 :: INFO :: diags.transforms.fft: Computing the forward Fourier transform of input array dimension (31, 25).[0m
    [37;21m2023-09-06 14:37:42 :: INFO :: diags.transforms.fft: Computing the inverse Fourier transform of input array dimension (31, 25).[0m
    [37;21m2023-09-06 14:37:42 :: INFO :: diags.transforms.fft: Computing the inverse Fourier transform of input array dimension (31, 25).[0m
    [37;21m2023-09-06 14:37:42 :: INFO :: diags.transforms.fft: Computing the inverse Fourier transform of input array dimension (31, 25).[0m
    [38;5;226m2023-09-06 14:37:43 :: WARNING :: utils.schema_interface: Schema optional value tablefmt has not been defined; setting to default value outline.[0m
    [38;5;226m2023-09-06 14:37:43 :: WARNING :: utils.schema_interface: Schema optional value numalign has not been defined; setting to default value ['center', 'center'].[0m
    [38;5;226m2023-09-06 14:37:43 :: WARNING :: utils.schema_interface: Schema optional value colalign has not been defined; setting to default value ['center', 'center'].[0m
    [38;5;226m2023-09-06 14:37:43 :: WARNING :: utils.schema_interface: Schema optional value disable_numparse has not been defined; setting to default value False.[0m
    [37;21m2023-09-06 14:37:43 :: INFO :: utils.schema_interface: Schema successfully validated.[0m
    [37;21m2023-09-06 14:37:43 :: INFO :: tcdiags.diagnostics.VURK2014: 
    
    +----------------------+----------------------------+
    |  TC 14L Wave Number  |  Maximum Wind Speed (mps)  |
    +======================+============================+
    |          0           |          18.1448           |
    |          1           |          3.10168           |
    |          2           |          2.06525           |
    +----------------------+----------------------------+
    
    [0m
    [37;21m2023-09-06 14:37:43 :: INFO :: utils.schema_interface: Schema successfully validated.[0m
    [37;21m2023-09-06 14:37:43 :: INFO :: tcdiags.diagnostics.VURK2014: 
    
    +---------------------------------------+---------+---------+
    |         TC 14L MSI Attribute          |  Value  | Units   |
    +=======================================+=========+=========+
    |          Maximum wind speed           | 22.0972 | mps     |
    |        Radius of maximum wind         | 120000  | m       |
    |         Maximum wind latitude         | 12.3731 | deg     |
    |        Maximum wind longitude         | -72.306 | deg     |
    |   Azimuth of radius of maximum wind   |   60    | deg     |
    |    Wavenumber 0 Maximum Wind Speed    | 18.1448 | mps     |
    |    Wavenumber 1 Maximum Wind Speed    | 3.10168 | mps     |
    | Wavenumber (0 + 1) Maximum Wind Speed | 19.8317 | mps     |
    |          Residual wind speed          | 2.26555 | mps     |
    +---------------------------------------+---------+---------+
    
    [0m
    [37;21m2023-09-06 14:37:43 :: INFO :: tcdiags.diagnostics.VURK2014: Writing netCDF-formatted output file ./tcdiags.vurk2014_msi.14L.nc for TC event 14L.[0m


### Plot the tropical cyclone multi-scale intensity attributes.


```python
# Build a table containing the TC MSI attributes.
tcids = parser_interface.object_getattr(object_in=tcmsi, key="tcids")
for tcid in tcids:
    header = [f"TC {tcid} MSI Attributes", "Value (Units)"]
    tcobj = parser_interface.object_getattr(object_in=tcmsi, key=tcid)
    table = []
    for tcmsi_attr in tcmsi_attrs_dict:
        try:
            value = parser_interface.object_getattr(object_in=tcobj, key=tcmsi_attr)._magnitude
        except Exception:
            value = parser_interface.object_getattr(object_in=tcobj, key=tcmsi_attr)
        name = parser_interface.dict_key_value(dict_in=tcmsi_attrs_dict[tcmsi_attr],
                                               key="name", no_split=True)
        units = parser_interface.dict_key_value(dict_in=tcmsi_attrs_dict[tcmsi_attr],
                                                key="units", no_split=True)
        msg = [name, f"{value} ({units})"]
        table.append(msg)
    
    # Display the table.
    table = tabulate(table, header, tablefmt="html", numalign=("center", "center"),
                    colalign=("center","center")) 
    display(HTML(table))
   
    # Collect/define the grid attributes.
    azimuth = tcobj.wnds10m.azimuth
    radial = tcobj.wnds10m.radial/1000.0
    xticks = numpy.radians(numpy.arange(0., 360.0, 45.0))
    yticks = []

    # Plot the total wind field.
    (fig, ax) = plt.subplots(subplot_kw={'projection': 'polar'})
    total_wind = tcobj.wnds10m.varout
    plot = ax.contourf(azimuth, radial, total_wind, levels=vmax_levels, cmap=vmax_cmap)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)
    ax.spines['polar'].set_color('none')
    ticks = numpy.arange(vmax_cmin, (vmax_cmax + 0.01), vmax_cint)
    plt.colorbar(plot, orientation="horizontal", ticks=ticks, pad=0.1,
                 aspect=50, label=f"TC {tcid} 10-meter Wind Speed (ms$^{-1}$)")
    plt.savefig(f"tcwnmsi.10m_wind.{tcid}.png", dpi=500, transparent=False, 
                bbox_inches="tight")
    plt.show()
    
    # Plot the wave-number 0 wind field.
    (fig, ax) = plt.subplots(subplot_kw={'projection': 'polar'})
    wn0 = tcobj.wndspec.wn0
    plot = ax.contourf(azimuth, radial, wn0, levels=vmax_levels, cmap=vmax_cmap)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)
    ax.spines['polar'].set_color('none')
    ticks = numpy.arange(vmax_cmin, (vmax_cmax + 0.01), vmax_cint)
    plt.colorbar(plot, orientation="horizontal", ticks=ticks, pad=0.1,
                 aspect=50, label=f"TC {tcid} Wavenumber-0 Wind Speed (mps)")
    plt.savefig(f"tcwnmsi.wn0_wind.{tcid}.png", dpi=500, transparent=False, bbox_inches="tight")
    plt.show()

    # Plot the wave-number 0+1 wind field.
    (fig, ax) = plt.subplots(subplot_kw={'projection': 'polar'})
    wn0p1 = wn0 + tcobj.wndspec.wn1
    plot = ax.contourf(azimuth, radial, wn0p1, levels=vmax_levels, cmap=vmax_cmap)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)
    ax.spines['polar'].set_color('none')
    ticks = numpy.arange(vmax_cmin, (vmax_cmax + 0.01), vmax_cint)
    plt.colorbar(plot, orientation="horizontal", ticks=ticks, pad=0.1,
                 aspect=50, label=f"TC {tcid} Wavenumbers (0+1) Wind Speed (mps)")
    plt.savefig(f"tcwnmsi.wn0p1_wind.{tcid}.png", dpi=500, transparent=False, bbox_inches="tight")
    plt.show()

    # Plot the residual components of the wind field.
    (fig, ax) = plt.subplots(subplot_kw={'projection': 'polar'})
    wnres = numpy.abs(total_wind - wn0p1._magnitude)
    plot = ax.contourf(azimuth, radial, wnres, levels=vmax_levels, cmap=vmax_cmap)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)
    ax.spines['polar'].set_color('none')
    ticks = numpy.arange(vmax_cmin, (vmax_cmax + 0.01), vmax_cint)
    plt.colorbar(plot, orientation="horizontal", ticks=ticks, pad=0.1,
                 aspect=50, label=f"TC {tcid} Residual Wavenumbers Wind Speed (mps)")
    plt.savefig(f"tcwnmsi.wnres_wind.{tcid}.png", dpi=500, transparent=False, bbox_inches="tight")
    plt.show()    

    # Plot the wave number spectra for the wind field.
    for wn in range(1, tcobj.ncoeffs):
        (fig, ax) = plt.subplots(subplot_kw={'projection': 'polar'})
        wnspec = parser_interface.object_getattr(object_in=tcobj.wndspec, key=f"wn{wn}")
        plot = ax.contourf(azimuth, radial, wnspec, levels=wn_levels, cmap=wn_cmap)
        ax.set_xticks(xticks)
        ax.set_yticks(yticks)
        ax.xaxis.grid(False)
        ax.yaxis.grid(False)
        ax.spines['polar'].set_color('none')
        ticks = numpy.arange(wn_cmin, (wn_cmax + 0.01), wn_cint)
        plt.colorbar(plot, orientation="horizontal", ticks=ticks, pad=0.1,
                     aspect=50, label=f"TC {tcid} Wavenumber-{wn} Wind Speed (mps)")
        plt.savefig(f"tcwnmsi.wn{wn}_wind.{tcid}.png", dpi=500, transparent=False, bbox_inches="tight")
        plt.show()

```


<table>
<thead>
<tr><th style="text-align: center;">        TC 14L MSI Attributes         </th><th style="text-align: center;">       Value (Units)        </th></tr>
</thead>
<tbody>
<tr><td style="text-align: center;">           Center Latitude            </td><td style="text-align: center;">       13.4 (degrees)       </td></tr>
<tr><td style="text-align: center;">           Center Longitude           </td><td style="text-align: center;">       -72 (degrees)        </td></tr>
<tr><td style="text-align: center;">   Radius of Maximum Wind Latitude    </td><td style="text-align: center;">12.373095556722303 (degrees)</td></tr>
<tr><td style="text-align: center;">   Radius of Maximum Wind Longitude   </td><td style="text-align: center;">-72.30604517770875 (degrees)</td></tr>
<tr><td style="text-align: center;">     Maximum 10-meter Wind Speed      </td><td style="text-align: center;">  22.09724998474121 (mps)   </td></tr>
<tr><td style="text-align: center;">Azimuth of Maximum 10-meter Wind Speed</td><td style="text-align: center;">60.000000000000135 (degrees)</td></tr>
<tr><td style="text-align: center;">Radius of Maximum 10-meter Wind Speed </td><td style="text-align: center;">        120000.0 (m)        </td></tr>
<tr><td style="text-align: center;">   Wavenumber-0 Maximum Wind Speed    </td><td style="text-align: center;">  18.144823659624375 (mps)  </td></tr>
<tr><td style="text-align: center;">   Wavenumber-1 Maximum Wind Speed    </td><td style="text-align: center;">  3.1016818996685966 (mps)  </td></tr>
<tr><td style="text-align: center;"> Wavenumbers (0+1) Maximum Wind Speed </td><td style="text-align: center;">  19.831703222806482 (mps)  </td></tr>
<tr><td style="text-align: center;">Residual Wavenumber Maximum Wind Speed</td><td style="text-align: center;">  2.265546761934729 (mps)   </td></tr>
</tbody>
</table>



    
![png](tcdiags.vurk2014_msi_files/tcdiags.vurk2014_msi_7_1.png)
    



    
![png](tcdiags.vurk2014_msi_files/tcdiags.vurk2014_msi_7_2.png)
    



    
![png](tcdiags.vurk2014_msi_files/tcdiags.vurk2014_msi_7_3.png)
    



    
![png](tcdiags.vurk2014_msi_files/tcdiags.vurk2014_msi_7_4.png)
    



    
![png](tcdiags.vurk2014_msi_files/tcdiags.vurk2014_msi_7_5.png)
    



    
![png](tcdiags.vurk2014_msi_files/tcdiags.vurk2014_msi_7_6.png)
    

