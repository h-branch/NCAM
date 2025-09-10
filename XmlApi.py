import requests
import urllib3
import xml.etree.ElementTree as ET
import pandas as pd
from time import sleep

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.safetydata.go.kr/V2/api/DSSP-IF-20286"
key = "1R550W0GK8X3P778"

data_list = []

for page in range(1, 31):  # ✅ 예: 1~30페이지까지 자동으로
    payload = {
        "serviceKey": key,
        "returnType": "xml",
        "pageNo": str(page),
        "numOfRows": "30",
        "RSRVR_CD": "4372010019",
        "MSRN_DT": "202508010000"
    }

    print(f"📄 {page} 페이지 요청 중...")

    try:
        response = requests.get(url, params=payload, verify=False, timeout=10)
        root = ET.fromstring(response.content)
        items = list(root.iter('item'))

        if not items:
            print("📭 데이터 없음, 종료.")
            break

        for item in items:
            data_list.append({
                "측정시각": item.findtext('MSRN_DT'),
                "수위(m)": item.findtext('LOLE'),
                "저수율(%)": item.findtext('WRERATES')
            })

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        break

    sleep(0.5)  # 서버 과부하 방지

# ✅ pandas로 저장
df = pd.DataFrame(data_list)
df.to_csv("D:/lhj/과업(연구과제)/저수지 지점강우/250910 백록저수지 25년 8월 10분 단위/reservoir_data_all_pages.csv", index=False, encoding="utf-8-sig")

print("\n✅ 전체 페이지 데이터를 CSV로 저장 완료!")
