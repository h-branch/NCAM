from netCDF4 import Dataset
import numpy as np
import rasterio
from rasterio.transform import Affine


ds = Dataset("D:/lhj/과업(연구과제)/hail/1. gis/grid/NCAM_ensemble_hailcast-2025-05-01_1500KST.nc")

lats = ds.variables['Latitude'][:]
lons = ds.variables['Longitude'][:]

print("Latitude min/max:", np.min(lats), np.max(lats))
print("Longitude min/max:", np.min(lons), np.max(lons))

hail = ds.variables['Ensemble_Hail_probability(%)'][:]

min_lon = np.min(lons)
max_lon = np.max(lons)
min_lat = np.min(lats)
max_lat = np.max(lats)
height, width = hail.shape
pixel_width = (max_lon - min_lon) / width
pixel_height = (max_lat - min_lat) / height
transform = Affine.translation(min_lon, max_lat) * Affine.scale(pixel_width, -pixel_height)

flip = np.flipud(hail)

with rasterio.open(
    'D:/lhj/과업(연구과제)/hail/1. gis/hail99.tiff',
    'w',
    driver='GTiff',
    height=height,
    width=width,
    count=1,
    dtype=hail.dtype,
    crs='EPSG:4326',
    transform=transform
) as dst:
    dst.write(flip, 1)
