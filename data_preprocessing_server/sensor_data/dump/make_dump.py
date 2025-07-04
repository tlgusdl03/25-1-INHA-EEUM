import pandas as pd
import os
from datetime import timedelta

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "sensor_data.csv")
xlsx_path = os.path.join(base_dir, "ICW0W2000398_20211001_20211031.xlsx")

# 1. CSV 로드
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"{csv_path} 없음")

csv_df = pd.read_csv(csv_path)

# 2. 기존 엑셀 로드 (없으면 빈 프레임 생성)
if os.path.exists(xlsx_path):
    xlsx_df = pd.read_excel(xlsx_path)
    expected_columns = xlsx_df.columns.tolist()
else:
    expected_columns = [
        "데이터 시간", "미세먼지", "초미세먼지", "이산화탄소", "휘발성유기화합물", "온도", "습도", "소음",
        "통합지수", "시리얼넘버", "스테이션명", "제품등록일", "위도", "경도", "고객사"
    ]
    xlsx_df = pd.DataFrame(columns=expected_columns)

# 3. 리샘플링 및 가공
csv_df["collected_at"] = pd.to_datetime(csv_df["collected_at"])
csv_df["location_id"] = 2
csv_df.set_index("collected_at", inplace=True)

resampled = csv_df.resample("1T").first().reset_index()

column_mapping = {
    "collected_at": "데이터 시간",
    "pm10": "미세먼지",
    "pm2_5": "초미세먼지",
    "tvoc": "휘발성유기화합물",
    "temperature": "온도",
    "humidity": "습도",
    "noise": "소음"
}
resampled = resampled.rename(columns=column_mapping)

# 누락 열 채움
for col in expected_columns:
    if col not in resampled.columns:
        resampled[col] = None

# 시간 보정
resampled["데이터 시간"] = pd.to_datetime(resampled["데이터 시간"]) + timedelta(hours=9)
resampled["데이터 시간"] = resampled["데이터 시간"].dt.tz_localize(None)

# 열 정렬
resampled = resampled[expected_columns]

# 4. 기존 데이터 + 신규 데이터 붙이기
appended = pd.concat([xlsx_df, resampled], ignore_index=True)

# 👉 여기서 시간 순으로 정렬 추가
appended = appended.sort_values(by="데이터 시간").reset_index(drop=True)

# 5. 다시 기존 파일 덮어쓰기
appended.to_excel(xlsx_path, index=False)
print(f"엑셀 파일에 append 완료: {xlsx_path}")
