import pandas as pd
import geopandas as gpd


# 1. 데이터 불러오기
hail_v = gpd.read_file('D:/lhj/과업(연구과제)/hail/1. gis/clip_p.shp')

# 2. 실제 값 컬럼명 설정 (예: 'value')
value_col = 'VALUE'  # 실제 컬럼명으로 바꿔주세요

# 3. '0' 포함한 범주형 지정 (미발령 0도 범주에 포함)
value_levels = [0, 20, 40, 60, 80, 100]
hail_v[value_col] = pd.Categorical(hail_v[value_col], categories=value_levels, ordered=True)

# 4. 0 등급이 실제 데이터에 없으면 따로 0 값 할당 필요
# 예: 만약 미발령 격자(0)가 데이터에 없으면 직접 추가할 수도 있음
# (아래는 예시, 실제 데이터 상황에 맞게 조절 필요)
# hail_v = hail_v.append(pd.DataFrame({'SGG': ['dummy'], value_col: 0, 'geometry': None}), ignore_index=True)

# 5. 시군구별 교차표 생성
table = pd.crosstab(hail_v['SGG'], hail_v[value_col])

# 6. 없으면 0 컬럼 추가 (안전 처리)
for col in [0, 20, 40, 60, 80, 100]:
    if col not in table.columns:
        table[col] = 0

# 7. 컬럼 순서 정렬
table = table[[0, 20, 40, 60, 80, 100]]

# 8. Total 열 추가
table['Total'] = table.sum(axis=1)

# 9. 위험도 계산 함수 (위에서 설명한 대로)
def determine_risk(row):
    # 위험도는 20~100 등급만 계산
    present_levels = [lvl for lvl in value_levels if lvl in row.index and lvl != 0]
    level_counts = row[present_levels]
    total = row['Total']

    if level_counts.sum() >= total * 0.5:
        max_count = level_counts.max()
        most_common_levels = [lvl for lvl in present_levels if level_counts[lvl] == max_count]
        final_risk = max(most_common_levels)  # 높은 등급 우선
        return final_risk
    else:
        return 0  # 미발령

# 10. 위험도 컬럼 추가
table['위험도_값'] = table.apply(determine_risk, axis=1)

risk_labels = {
    0: '미발령',
    20: '관심',
    40: '주의',
    60: '경계',
    80: '위험',
    100: '심각'
}

table['최종위험도'] = table['위험도_값'].map(risk_labels)

# 11. 출력 및 저장
print(table)
table.to_excel('D:/lhj/과업(연구과제)/hail/1. gis/value_counts_with_zero.xlsx')
