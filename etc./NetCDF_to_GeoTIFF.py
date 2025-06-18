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

lat0=np.max(lats)
lon0=np.min(lons)
dlon=np.mean(np.diff(lons[0,:]))
dlat=np.mean(np.diff(lats[:,0]))
transform=from_origin(lon0, lat0, dlon, abs(dlat))

flip=np.flipud(hail)

with rasterio.open(
    'D:/lhj/과업(연구과제)/hail/1. gis/hail5.tif',
    'w',
    driver='GTiff',
    height=hail.shape[0],
    width=hail.shape[1],
    count=1,
    dtype=hail.dtype,
    crs='EPSG:4326',
    transform=transform
) as dst:
    dst.write(flip, 1)
