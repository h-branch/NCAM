import numpy as np
import pandas as pd
import os
import glob


f_path = 'D:/lhj/과업(연구과제)/꿀벌/260318 공주, 청주, 진주 기온 데이터(97_25)/진주'
csv_files = glob.glob(os.path.join(f_path, '*.csv'))

if not csv_files:
    raise FileNotFoundError('csv 파일이 없습니다.')

df_list = []

for file in csv_files:
    try:
        try:
            df = pd.read_csv(file, encoding='utf-8-sig')
        except:
            try:
                df = pd.read_csv(file, encoding='cp949')
            except:
                df = pd.read_csv(file, encoding='euc-kr')

        if '일시' not in df.columns:
            print(f"'일시' 열 없음: {os.path.basename(file)}")
            continue

        df['source_file'] = os.path.basename(file)
        df_list.append(df)
        print(f'읽기 성공: {os.path.basename(file)}')

    except Exception as e:
        print(f'읽기 실패: {os.path.basename(file)} / 오류: {e}')

if not df_list:
    raise ValueError('읽어들인 데이터프레임이 없습니다. 모든 파일 읽기에 실패했습니다.')

merged_df = pd.concat(df_list, ignore_index=True)

# 일시를 날짜형으로 변환
merged_df['일시'] = pd.to_datetime(merged_df['일시'], errors='coerce')

# 일시가 변환되지 않은 행 제거
merged_df = merged_df.dropna(subset=['일시'])

# 전체 날짜 범위 생성
date_range = pd.date_range(start=merged_df['일시'].min(),
                           end=merged_df['일시'].max(),
                           freq='D')

full_dates = pd.DataFrame({'일시': date_range})

# 전체 날짜와 병합
df_full = pd.merge(full_dates, merged_df, on='일시', how='left')
df_full = df_full.sort_values('일시').reset_index(drop=True)

# 지점명 열 추가
if '지점' in df_full.columns:
    idx = df_full.columns.get_loc('지점')
    df_full.insert(idx + 1, '지점명', '진주')
else:
    df_full.insert(0, '지점명', '진주')

# 일시 열을 지점명 다음으로 이동
date_col = df_full.pop('일시')
idx = df_full.columns.get_loc('지점명')
df_full.insert(idx + 1, '일시', date_col)

# 최고기온 시각(hhmi)까지만 남기기
end_col = '최고기온 시각(hhmi)'
if end_col in df_full.columns:
    df_full = df_full.loc[:, :end_col]
else:
    print(f"'{end_col}' 열이 없어 열 자르기를 수행하지 않았습니다.")

output_path = 'D:/lhj/과업(연구과제)/꿀벌/260318 공주, 청주, 진주 기온 데이터(97_25)/1997_2021_AWS_진주_일평균.csv'
df_full.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f'저장 완료: {output_path}')
