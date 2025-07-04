from pandas import read_excel
from datetime import datetime, timedelta, timezone
import math
import os

def validate_dataframe(df):
    required_columns = ["데이터 시간", "온도", "습도", "휘발성유기화합물", "소음", "미세먼지", "초미세먼지"]
    if df.empty:
        raise ValueError("DataFrame is empty")

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns: {', '.join(missing_columns)}")

    sensor_columns = [col for col in required_columns if col != "데이터 시간"]
    df_clean = df.copy()

    # -99가 포함된 행 삭제
    mask = (df_clean[sensor_columns] == -99).any(axis=1)
    df_clean = df_clean[~mask].copy()

    # IQR 이상치 제거
    for col in sensor_columns:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df_clean = df_clean[(df_clean[col].isna()) | ((df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound))]

    return df_clean

def escape_sql_value(value):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "NULL"
    if isinstance(value, str):
        escaped = value.replace("'", "''")
        return f"'{escaped}'"
    return value

def is_all_nan(*args):
    return all(val is None or (isinstance(val, float) and math.isnan(val)) for val in args)

def generate_sql_file():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_paths = [f for f in os.listdir(BASE_DIR) if f.endswith(".xlsx")]

    for i, file_path in enumerate(file_paths):
        try:
            file_path = os.path.join(BASE_DIR, file_path)
            df = read_excel(file_path)
            df = validate_dataframe(df)

            # 시간 정렬 → 최신순 역순 정렬
            df = df.sort_values(by="데이터 시간").iloc[::-1].reset_index(drop=True)

            row_count = len(df)

            # 1. 현재시간 (로컬) 기준을 KST로 간주하고, UTC로 바꿔 (9시간 빼기)
            now_kst_naive = datetime.now()
            now_utc_naive = now_kst_naive - timedelta(hours=9)

            end_dateTime = now_utc_naive.replace(tzinfo=None)

            insert_stmt = "INSERT INTO sensor_datas (location_id, collected_at, temperature, humidity, tvoc, noise, pm10, pm2_5) VALUES"
            values = []

            for index in range(row_count):
                # 최신 시간에서 과거로 1분씩
                current_time = end_dateTime - timedelta(minutes=(row_count - 1 - index))

                temperature = df["온도"].values[index]
                humidity = df["습도"].values[index]
                tvoc = df["휘발성유기화합물"].values[index]
                noise = df["소음"].values[index]
                pm10 = df["미세먼지"].values[index]
                pm2_5 = df["초미세먼지"].values[index]

                if is_all_nan(temperature, humidity, tvoc, noise, pm10, pm2_5):
                    continue

                values.append(
                    f"({i + 1}, '{current_time}', {escape_sql_value(temperature)}, "
                    f"{escape_sql_value(humidity)}, {escape_sql_value(tvoc)}, "
                    f"{escape_sql_value(noise)}, {escape_sql_value(pm10)}, "
                    f"{escape_sql_value(pm2_5)})"
                )
                
            final_sql = insert_stmt + "\n" + ",\n".join(values) + ";"

            output_dir = os.path.join(BASE_DIR, "output")
            os.makedirs(output_dir, exist_ok=True)

            output_path = os.path.join(output_dir, f"5.{i + 1}_insert_sensor_datas.sql")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(final_sql)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    generate_sql_file()
