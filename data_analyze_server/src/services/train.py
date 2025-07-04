from sqlalchemy.ext.asyncio import AsyncSession
from xgboost import XGBRegressor
from sklearn.multioutput import MultiOutputRegressor
import numpy as np
import os
import pickle
from services.data_loader import get_filtered_data, prepare_training_data

def save_model(model, path:str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(model, f)

def load_model(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found: {path}")
    with open(path, "rb") as f:
        model = pickle.load(f)
    return model

async def train_model(db: AsyncSession, location_id: int, history_days: int, lookback_days: int):
    """
    주어진 location_id에 대해 XGBoost 모델을 학습
    """
    # 데이터 가져오기 (history_days일치 데이터)
    sensor_data = await get_filtered_data(db, location_id=location_id, target_days=history_days, require_future=True)

    X_train, y_train = prepare_training_data(sensor_data, lookback_days=lookback_days)
    
    print(f"✅ 학습 데이터 크기: {X_train.shape}, 타겟 데이터 크기: {y_train.shape}")

    # 모델 생성
    model = MultiOutputRegressor(
        XGBRegressor(
            n_estimators=400,        # 트리 수 증가 (기존 100 → 400)
            max_depth=3,             # 트리 깊이 (기존 3 → 6)
            learning_rate=0.05,      # 학습률 낮춤 (0.1 → 0.05)
            subsample=0.8,           # 샘플링 비율 (과적합 방지)
            colsample_bytree=0.8,    # feature 샘플링 비율
            random_state=42,
            n_jobs=-1                # 모든 CPU 사용
        )
    )

    # 모델 학습
    model.fit(X_train, y_train)

    print("✅ 모델 학습 완료")

    # 모델 저장
    os.makedirs('models', exist_ok=True)
    save_model(model, f"models/{location_id}.pkl")
    print(f"✅ 모델 저장 완료: models/{location_id}.pkl")

    return model




