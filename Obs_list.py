import numpy as np
import pandas as pd
import os
import glob


f_path='D:/lhj/과업(연구과제)/꿀벌/260318 공주, 청주, 진주 기온 데이터(97_25)/진주'
csv=glob.glob(os.path.join(f_path, '*.csv'))

if not csv:
  print('csv 파일이 없습니다.')
else:
  df_list=[]

  for file in csv:
    try:
      try:
        df=pd.read_csv(file, encoding='utf-8-sig')
      except:
        try:
          df=pd.read_csv(file, encoding='cp949')
        except:
          df=pd.read_csv(file, encoding='euc-kr')

      df['source_file']=os.path.basename(file)
      df_list.append(df)
      print(f'읽기 성공: {os.path.basename(file)}')

    except Exception as e:
      print(f'읽기 실패: {os.path.basename(file)} / 오류: {e}')

  merged_df=pd.concat(df_list, ignore_index=Ture)

merged_df['일시']=pd.to_datetime(merged_df['일시'])
date_range=pd.date_range(start=merged_df['일시'].min(), end=merged_df['일시'].max(), freq='D')
full_dates=pd.DataFrame({'일시': date_range})
df_full=pd.merge(full_dates, merged_df, on='일시', how='left')
df_full=df_full.sort_values('일시').reset_index(drop=True)

idx=df_full.columns.get_loc('지점')
df_full.insert(idx+1, '지점명', '진주')

date_col=df_full.pop('일시')
idx=df_full.columns.get_loc('지점명')
df_full.insert(idx+1, '일시', date_col)
end_col='최고기온 시각(hhmi)'
df_full=df_full.loc[:, :'최고기온 시각(hhmi)']

output_path='D:/lhj/과업(연구과제)/꿀벌/260318 공주, 청주, 진주 기온 데이터(97_25)/1997_2021_AWS_진주_일평균.csv'
df_full.to_csv(output_path, index=False, encoding='utf-8-sig')
