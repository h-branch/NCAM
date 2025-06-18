import geopandas as gpd


hail_v=gpd.read_file('D:/lhj/과업(연구과제)/hail/1. gis/clip_p.shp')

hail_v

counts = hail_v['SGG'].value_counts()
print(counts)

counts.to_excel('D:/lhj/과업(연구과제)/hail/1. gis/output.xlsx')
