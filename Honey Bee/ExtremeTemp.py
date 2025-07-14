# 일별 극한기온 추출(0.25, 10, 90, 99.75%ile)

# 구글 드라이브 마운트 (구글 colab 사용시)
# from google.colab import drive
# drive.mount('/content/drive')

# 라이브러리 호출
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


# 데이터 불러오기
df=pd.read_csv("/content/drive/MyDrive/1997_2023_AWS_영암_일평균.csv", encoding='euckr', parse_dates=["일시"])
df.set_index("일시", inplace=True)
df['day']=df.index.day
df['month']=df.index.month
df['year']=df.index.year

# 2023년 11월 데이터 필터링
df_2023_nov=df[(df['year']==2023)&(df['month']==11)].dropna(subset=['평균기온'])
# 1997~2022년 11월 데이터 필터링
df_hist_nov=df[(df['year']<2023)&(df['month']==11)]

# 날짜별로 그룹화하여 일별 평균, 최고, 최저 기온 계산
df_2023_summary=df_2023_nov.groupby(['day']).agg(
    최고기온=('최고기온', 'mean'),
    최저기온=('최저기온', 'mean'),
    평균기온=('평균기온', 'mean')
).reset_index()

# 월, 일 데이터를 mm-dd 형태로 변환
dates=df_2023_summary['day'].apply(lambda x: f'11-{x:02d}') # 원하는 월로

# 극단적인 기온을 탐지하는 시각화
def plot_extreme_weather(dates, y_2023, mean_temp, std_temp):
    min_length=min(len(dates), len(y_2023))
    dates=dates[:min_length]
    y_2023=y_2023[:min_length]
    plt.figure(figsize=(15,6))
    
    # 정규분포의 퍼센타일 계산
    high_extreme=stats.norm(mean_temp, std_temp).ppf(0.9975)
    low_extreme=stats.norm(mean_temp, std_temp).ppf(0.0025)
    high_90=stats.norm(mean_temp, std_temp).ppf(0.9)
    low_10=stats.norm(mean_temp, std_temp).ppf(0.1)

    # 기온 시각화
    plt.plot(dates, y_2023, color='black', label='2023 Temperature')
    plt.axhline(y=high_extreme, color='red', linestyle='--', label='99.75%ile (+2σ)')
    plt.axhline(y=low_extreme, color='blue', linestyle='--', label='0.25%ile (-2σ)')
    plt.fill_between(dates, y_2023, high_90, where=(y_2023>high_90), interpolate=True, color='red', alpha=0.3, label='Above 90%ile')
    plt.fill_between(dates, y_2023, low_10, where=(y_2023<low_10), interpolate=True, color='blue', alpha=0.3, label='Below 10%ile')
    plt.fill_between(dates, y_2023, high_extreme, where=(y_2023>high_extreme), interpolate=True, color='red', alpha=0.7, label='Above 99.75%ile')
    plt.fill_between(dates, y_2023, low_extreme, where=(y_2023<low_extreme), interpolate=True, color='blue', alpha=0.7, label='Below 0.025%ile')

    # 축 및 레이블 설정
    plt.xticks(rotation=45, fontsize=12) # 그래프 x축 범위
    plt.yticks(rotation=12) # 그래프 y축 범위
    plt.grid(True) # 그래프 격자 여부
    plt.xlabel('Date (Month-Day)', fontsize=15) #그래프 x축 라벨
    plt.ylabel('Temperature (℃)', fontsize=15) #그래프 y축 라벨
    plt.title('Extreme Weather Detection [November 2023]', fontsize=18, fontweight='bold') # 그래프 제목
    plt.legend(loc='lower left', fontsize=12) # 그래프 범례
    plt.show()

# 11월의 평균과 표준편차 계산 (1997-2022)
mean_temp=df_hist_nov['평균기온'].mean() # 11월 평균기온
std_temp=df_hist_nov['평균기온'].std() # 11월 표준편차

# 시각화
plot_extreme_weather(dates, df_2023_summary['평균기온'], mean_temp, std_temp)
