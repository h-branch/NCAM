from netCDF4 import Dataset
import numpy as np
import rasterio
from rasterio.transform import from_origin


nc='D:/lhj/과업(연구과제)/hail/1. gis/grid/NCAM_ensemble_hailcast-2025-05-01_1500KST.nc'
netCDF4.Dataset(nc)
ds=Dataset(nc, 'r')
print(ds.variables.keys())

hail=ds.variables['Ensemble_Hail_probability(%)'][:]
lats=ds.variables['Latitude'][:]
lons=ds.variables['Longitude'][:]

if lats.ndim == 2 and lons.ndim == 2:
    lat0=lats[0,0]
    lon0=lons[0,0]
    dlat=lats[1,0]-lats[0,0]
    dlon=lons[0,1]-lons[0,0]
else:
    raise ValueError("lat/lon 값이 예상과 다름")

transform=from_origin(lon0, lat0 + dlat * hail.shape[0], dlon, -dlat)

with rasterio.open(
    'D:/lhj/과업(연구과제)/hail/1. gis/grid/hail.tif',
    'w',
    driver='GTiff',
    height=hail.shape[0],
    width=hail.shape[1],
    count=1,
    dtype=hail.dtype,
    crs='EPSG:4326',
    transform=transform
) as dst:
    dst.write(hail, 1)
