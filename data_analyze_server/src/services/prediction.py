from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from schemas.prediction import PredictionItem, PredictionResponse
from services.train import load_model
from services.data_loader import get_filtered_data, prepare_prediction_data

KST = timezone(timedelta(hours=9))

async def predict_future(db: AsyncSession, location_id: int, lookback_days: int) -> PredictionResponse:
    """
    지정한 location_id에 대해 미래 24시간(3시간 간격, 총 8개 포인트) 예측
    """
    # 1. 모델 불러오기
    model = load_model(f"models/{location_id}.pkl")
    
    # 2. 입력 데이터 가져오기 (7일치 리샘플링 168포인트)
    x_input = await get_filtered_data(db, location_id, lookback_days, False)
    
    # 3. Flatten + 모델 입력 형태 맞추기
    x_input = prepare_prediction_data(x_input, lookback_days=lookback_days)

    # 4. 예측
    y_pred = model.predict(x_input)  # (1, 48) shape
    y_pred = y_pred.reshape(8, 9)    # (8, 6) -> 8포인트, 6개 항목

    # 5. 예측 시간 생성 (오늘 0시 기준 3시간 간격)
    now = datetime.now(KST)
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    times = [today + timedelta(hours=i * 3) for i in range(8)]

    # 6. PredictionItem으로 포장
    results = []
    for i, dt in enumerate(times):
        results.append(
            PredictionItem(
                datetime=dt.astimezone(timezone.utc).isoformat(),
                temperature=y_pred[i][0],
                humidity=y_pred[i][1],
                tvoc=y_pred[i][2],
                noise=y_pred[i][3],
                pm10=y_pred[i][4],
                pm2_5=y_pred[i][5]
            )
        )

    return PredictionResponse(predictions=results)
