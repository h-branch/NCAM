import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


f_path=('C:/Users/Ncam1988/Downloads/한국농어촌공사_저수지 수위데이터_20240219/백록저수지_lhj_v2.0.csv')

f=pd.read_csv(f_path, encoding='euc-kr', header=None, names=['year', 'month', 'day', 'time', 'ELm', '%'])
f_sort=f.sort_values(by=['year', 'month', 'day', 'time'], ascending=True)

f_sort['datetime']=pd.to_datetime(
    f_sort['year'].astype(str) + '-' +
    f_sort['month'].astype(str).str.zfill(2) + '-' +
    f_sort['day'].astype(str).str.zfill(2) + '-' +
    f_sort['time'].astype(str).str.zfill(2) + ':00'
    )

day=f_sort[f_sort['time']==0]['datetime'].tolist()
day_str = [d.strftime('%m-%d-%H') for d in day]


# 1. 저수지 수위
plt.figure(figsize=(14,6))
plt.plot(f_sort['datetime'], f_sort['ELm'], color='red')
#for dt in day:
#    plt.axvline(x=dt, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.grid(True, axis='x', linestyle='--', alpha=0.3)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.xlabel('date')
plt.ylabel('EL.m')
plt.xticks(rotation=45)
plt.title('Combined rainfall and EL.m [5 July 2023]', fontsize=18, fontweight='bold')
plt.show()


# 2. 저수지 수위 + 저수율(등급, %)
fig, ax1 = plt.subplots(figsize=(14,6))
ax1.plot(f_sort['datetime'], f_sort['ELm'], color='red', label='EL.m')

ax1.axhspan(158.0, 158.5, facecolor='red', alpha=0.2, label='Danger') # 저수용량 90.1% ~ 100%
ax1.axhspan(157.5, 158.0, facecolor='orange', alpha=0.2, label='Warning') # 저수용량 80% ~ 90.1%
ax1.axhspan(156.62, 157.5, facecolor='yellow', alpha=0.2, label='Caution') # 저수용량 70% ~ 80%
ax1.axhspan(155.9, 156.62, facecolor='green', alpha=0.2, label='Attention') # 저수용량 50% ~ 70%
ax1.axhspan(0., 155.9, facecolor='gray', alpha=0.2, label='Dry') # 갈수기

ax1.set_ylim(157.3, 158.52)

ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax1.grid(True, axis='x', linestyle='--', alpha=0.3)
ax1.grid(True, axis='y', linestyle='--', alpha=0.7)

ax1.set_xlabel('Time')
ax1.set_ylabel('EL.m')
plt.xticks(rotation=45)
plt.title('Hydrograph [5 July 2023]', fontsize=18, fontweight='bold')
ax1.legend(loc='upper right')
plt.tight_layout()
plt.show()


# 3. 저수지 수위 + 저수율(등급, %) + 강우
rainfall=pd.read_csv('C:/Users/Ncam1988/Desktop/05/rainfall_timeseries_Baekrok.csv')

# datetime 컬럼이 문자열이면 datetime 타입으로 변환
rainfall['datetime'] = pd.to_datetime(rainfall['datetime'])

# datetime 컬럼을 인덱스로 설정
rainfall.set_index('datetime', inplace=True)

# 1시간 단위로 합계 집계
rainfall_hourly = rainfall['rainfall'].resample('H').sum().reset_index()


fig, ax1 = plt.subplots(figsize=(14,6))
ax1.plot(f_sort['datetime'], f_sort['ELm'], color='red', label='EL.m')

ax1.axhspan(158.0, 158.5, facecolor='red', alpha=0.2, label='Danger') # 저수용량 90.1% ~ 100%
ax1.axhspan(157.5, 158.0, facecolor='orange', alpha=0.2, label='Warning') # 저수용량 80% ~ 90.1%
ax1.axhspan(156.62, 157.5, facecolor='yellow', alpha=0.2, label='Caution') # 저수용량 70% ~ 80%
ax1.axhspan(155.9, 156.62, facecolor='green', alpha=0.2, label='Attention') # 저수용량 50% ~ 70%
ax1.axhspan(0., 155.9, facecolor='gray', alpha=0.2, label='Dry') # 갈수기

ax1.set_ylim(157.3, 158.52)

ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax1.grid(True, axis='x', linestyle='--', alpha=0.3)
ax1.grid(True, axis='y', linestyle='--', alpha=0.7)

ax1.set_xlabel('Time')
ax1.set_ylabel('EL.m')

ax2=ax1.twinx()
ax2.bar(f_sort['datetime'], rainfall_hourly['rainfall'], width=0.03, color='blue', alpha=0.5, label='rainfall')
#ax2.bar(f_sort['datetime'], f_sort['rainfall'], width=0.03, color='blue', alpha=0.5, label='rainfall')
ax2.set_ylabel('Rainfall(mm)')

# 범례 합치기
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')

plt.xticks(rotation=45)
plt.title('Hydrograph [5 July 2023]', fontsize=18, fontweight='bold')
plt.tight_layout()
plt.show()
