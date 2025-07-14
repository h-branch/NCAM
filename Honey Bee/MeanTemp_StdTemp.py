# 1. 평균 기온 구하기 / 2. 평균 기온에 대한 표준편차 구하기

# 구글 드라이브 마운트 (구글 colab 사용 시)
# from google.colab import drive
# drive.mount('/content/drive')

# 라이브러리 호출
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


# 데이터 불러오기
df=pd.read_csv("/content/drive/MyDrive/1997_2023_AWS_영암_일평균.csv", encoding='euckr')
# '일시' 열을 datetime 형식으로 변환
df['일시']=pd.to_datetime(df['일시'])
# 0월 데이터만 필터링
month_data=df[df['일시'].dt.month==11] # 원하는 월을 설정
# 0월 평균기온과 표준편차 계산
month_mean_temp=month_data['평균기온'].mean()
month_std_temp=month_data['평균기온'].std()

# 연도별 0월 평균기온 계산
month_mean_temp_yearly=month_data.groupby(month_data['일시'].dt.year)['평균기온'].mean()

# 연도별 0월 평균기온의 표준편차 계산
month_std_temp_yearly=month_data.groupby(month_data['일시'].dt.year)['평균기온'].std()


# 그래프 그리기
plt.figure(figsize=(15,6))
plt.plot(month_mean_temp_yearly.index, month_mean_temp_yearly.values, color='red') # (평균기온)
plt.axhline(y=month_mean_temp, color='black', linestyle='-') # (평균기온)

plt.plot(month_std_temp_yearly.index, month_std_temp_yearly.values, color='green') # (표준편차)
plt.axhline(y=month_std_temp, color='black', linestyle='-') # (표준편차)


# x축, y축 범위 설정
plt.xticks(np.arange(1997, 2024, 1), rotation=45, fontsize=15, fontname='DejaVu Sans') # x축 범위 설정

plt.yticks(np.arange(4, 14.1, 1), fontsize=15, fontname='DejaVu Sans') # y축 범위 설정(평균기온)
plt.yticks(np.arange(1.0, 7.1, 0.5), fontsize=15, fontname='DejaVu Sans') # y축 범위 설정(표준편차)


# 제목, x축, y축 이름 설정
plt.title('Nov. Average Monthly Temperature', fontsize=15, fontweight='bold', fontname='DejaVu Sans') # (평균기온)
plt.title('Nov. Monthly Temperature Std.', fontsize=15, fontweight='bold', fontname='DejaVu Sans') # (표준편차)

plt.xlabel('Year', fontsize=15, fontname='DejaVu Sans')

plt.ylabel('Temperature(℃)', fontsize=15, fontname='DejaVu Sans') # (평균기온)
plt.text(1996, 9.2, "Mean Temp.", fontsize=15, fontname='DejaVu Sans') # 그래프 안 텍스트좌표(x,y)(평균기온)

plt.ylabel('Standard Deviation of October Temperature(℃)', fontsize=15, fontname='DejaVu Sans') # (표준편차)
plt.text(1996.3, 3.9, "Temp Std.", fontsize=15, fontname='DejaVu Sans') # 그래프 안 텍스트좌표(x,y)(표준편차)

plt.grid(True)
plt.rcParams['axes.unicode_minus']=False
plt.show()
