import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pyproj
import gzip
import glob
import os


# 지점 좌표, 격자 정보
t_lon=127.857
t_lat=36.391
# 격자 정보
nx, ny = 2305, 2881
cell_size=500
center_lat=38
center_lon=126
center_grid=(1681, 1121)

# 프로젝션 정의
projection = pyproj.Proj(proj='lcc', lat_1=30, lat_2=60, lat_0=center_lat, lon_0=center_lon, datum='WGS84')
# 격자 위치 계산
j_indices, i_indices = np.meshgrid(np.arange(nx), np.arange(ny))
x = (j_indices - center_grid[1]) * cell_size
y = (i_indices - center_grid[0]) * cell_size
# 프로젝션 변환 (벡터화된 함수 사용)
lon, lat = projection(x, y, inverse=True)

# 위경도 meshgrid일 경우 (2D)
i, j = np.unravel_index(np.argmin((lat - t_lat)**2 + (lon - t_lon)**2), lat.shape)

# Z-R 변환 함수
ZRa = 200.
ZRb = 1.6
def dbz_to_rain(dbz):
    # za와 zb 계산
    za = 0.1 / ZRb
    zb = np.log10(ZRa) / ZRb
    # 강수량 계산
    rain = dbz * za - zb
    rain = 10.0 ** rain
    return rain

# 데이터 파일 목록
data_dir='C:/Users/Ncam1988/Desktop/05'
f_list=sorted(glob.glob(os.path.join(data_dir, '*.bin.gz')))

rain_series=[]
timestamps=[]

for f_path in f_list:
    with open(f_path, 'rb') as f:
        decompressed_bytes=gzip.decompress(f.read())

    rain_rate=np.frombuffer(decompressed_bytes, dtype=np.int16, offset=1024).astype(np.float32).reshape(ny,nx)
    rain_rate[rain_rate <= -20000] = np.nan
    rain_rate /= 100

    rain_val=dbz_to_rain(rain_rate)

    # 해당 지점의 강우값 추출
    val=rain_val[i, j]
    rain_series.append(val)

    # 타임스탬프 추출 (예: RDR_CMP_CPP_PUB_202307050000.bin.gz → 202307050000)
    fname=os.path.basename(f_path)
    timestamp=fname.split('_')[-1].replace('.bin.gz', '')
    timestamps.append(timestamp)

# 시계열 저장
df=pd.DataFrame({
    'datetime':pd.to_datetime(timestamps, format='%Y%m%d%H%M'),
    'rainfall':rain_series
})

df.to_csv('C:/Users/Ncam1988/Desktop/05/rainfall_timeseries_Baekrok.csv', index=False)

# 시각화
plt.figure(figsize=(14, 5))
plt.plot(df['datetime'], df['rainfall'], color='blue', linewidth=2)
plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
plt.title('Rainfall Time Series at Baekrok', fontsize=16)
plt.xlabel('Time')
plt.ylabel('Rainfall')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
