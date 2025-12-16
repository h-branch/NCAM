import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParms['font.family']='Malgun Gothic'
plt.rcParms['axes.unicode_minus']=False

grades=list(range(100, 0, -1))
min_idx=[]
max_idx=[]

for g in grades:
  if g==100:
    min_idx.append(300)
    max_idx.append(500)
  elif g==99:
    min_idx.append(501)
    max_idx.append(1000)
  elif g>=2:
    min_val=1001+(98-g)*500
    max_val=min_val+499
    min_idx.append(min_val)
    max_idx.append(max_val)
  else:
    min_idx.append(49500)
    max_idx.append(np.nan)

df=pd.DataFrame({
  'grade': grades,
  'min_idx': min_idx,
  'max_idx': max_idx
})

plt.figure(figsize=(10,5))

for _, row in df.iterrows():
  x=row['grade']
  if pd.isna(row['max_idx']):
    plt.vlines(x, row['min_idx'], row['min_idx']+3000)
    plt.text(x, row['min_idx']+3100, '이상', ha='center', fontsize=8)
  else:
    plt.vlines(x, row['min_idx'], row['max_idx'])

plt.xlabel('재난등급')
plt.ylabel('재난지수')
plt.title('재난등급별 재난지수 범위')

plt.xlim(0, 100)
plt.xticks([1]+list(range(10, 101, 10)))
plt.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()
plt.show()
