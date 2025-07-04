from core.db import get_db
from services.prediction import predict_future
from schemas.prediction import PredictionResponse
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/prediction", tags=["Prediction"])

@router.get("/", response_model=PredictionResponse)
async def predict_sensor_data(
    location_id: int, 
    lookback_days: int = 7,
    db: AsyncSession = Depends(get_db)
):
    return await predict_future(db, location_id, lookback_days)

