from sqlalchemy.ext.asyncio import AsyncSession
from models import sensor_data
from datetime import datetime, timedelta, timezone
import numpy as np
from fastapi import HTTPException
from sqlalchemy import select
import pandas as pd

async def get_filtered_data(
    db: AsyncSession,
    location_id: int,
    target_days: int,
    require_future: bool = True,
) -> np.ndarray:
    """
    지정한 location_id의 target_days 기간(UTC 기준) 동안의
    데이터를 반환, 부족하면 과거로 범위를 확장
    """

    end_time = datetime.now(timezone.utc).replace(tzinfo=None)
    start_time = end_time - timedelta(days=target_days, hours=1)

    # 최소 필요 포인트 수 계산 
    if require_future:
        minimum_required_points = (7 + 1) * 24
    else:
        minimum_required_points = 7 * 24
    
    MAX_EXPANSION_DAYS = 14

    while True:
        result = await db.execute(
            select(sensor_data.SensorData).where(
                sensor_data.SensorData.location_id == location_id,
                sensor_data.SensorData.collected_at >= start_time,
                sensor_data.SensorData.collected_at <= end_time
            ).order_by(sensor_data.SensorData.collected_at)
        )  

        records = result.scalars().all()

        if not records:
            print(f"No sensor data found for location_id={location_id}")
            raise HTTPException(
                status_code=404,
                detail=f"No sensor data found for location_id={location_id}",
            )
        
        df = pd.DataFrame([{
            "timestamp": record.collected_at,
            "temperature": record.temperature,
            "humidity": record.humidity,
            "tvoc": record.tvoc,
            "noise": record.noise,
            "pm10": record.pm10,
            "pm2_5": record.pm2_5
        } for record in records if None not in (
            record.temperature,
            record.humidity,
            record.tvoc,
            record.noise,
            record.pm10,
            record.pm2_5
        )])

        # timestamp를 datetime 타입으로 변환
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
        df.set_index("timestamp", inplace=True)

        # 1시간 간격으로 리샘플링
        df_resampled = df.resample("1h").median().fillna(method="ffill").infer_objects(copy=False)

        if df_resampled.shape[0] >= minimum_required_points:
            print(f"df_resample_size : {df_resampled.shape[0]}")
            break

        start_time -= timedelta(days=1)

        if (end_time - start_time).days > MAX_EXPANSION_DAYS:
            print(f"Not enough data even after expanding {MAX_EXPANSION_DAYS} days for location_id={location_id}")
            raise HTTPException(
                status_code=422,
                detail=f"Not enough data even after expanding {MAX_EXPANSION_DAYS} days for location_id={location_id}",
            )
    
    # 시간 관련 Feature 추가
    df_resampled["hour"] = df_resampled.index.hour                               # 시간
    df_resampled["day_of_week"] = df_resampled.index.dayofweek                   # 요일
    df_resampled["is_weekend"] = (df_resampled['day_of_week'] >= 5).astype(int)  # 주말 여부

    # 특성 컬럼 선택
    feature_columns = ["temperature", "humidity", "tvoc", "noise", "pm10", "pm2_5", "hour", "day_of_week", "is_weekend"]
    
    # ndarray로 변환
    data = df_resampled[feature_columns].to_numpy()

    return data

def create_dataset(data: np.ndarray, lookback_days: int) -> tuple[np.ndarray, np.ndarray]:
    """
    과거 lookback_days 데이터를 사용해 다음 하루를 예측하는 학습 데이터 생성
    """
    X = []
    y = []

    # 7일 * 24시간 = 168개 포인트
    window_size = lookback_days * 24  
    # 8개 포인트 (3시간 간격)
    # target_size = 8                

    # 24시간 확보
    for i in range(len(data) - window_size - 24 + 1):
        # 입력 데이터
        X.append(data[i:i + window_size].flatten())
        # 출력 데이터
        y.append(data[i + window_size:i + window_size + 24 : 3].flatten())

    return np.array(X), np.array(y)

def prepare_training_data(data: np.ndarray, lookback_days: int) -> tuple[np.ndarray, np.ndarray]:

    if data.shape[0] < (lookback_days + 1) * 24:
        print(f"Not enough data to make a prediction problem occurred when prepare_training_data")
        raise HTTPException(
            status_code=422,
            detail=f"Not enough data to make a prediction problem occurred when prepare_training_data",
        )
    
    return create_dataset(data, lookback_days)

def prepare_prediction_data(data: np.ndarray, lookback_days: int) -> np.ndarray:
    """
    과거 lookback_days 데이터를 사용해 다음 하루를 예측하는 예측 데이터 생성
    """
    x_input = data[-lookback_days * 24:].flatten().reshape(1, -1)

    return x_input