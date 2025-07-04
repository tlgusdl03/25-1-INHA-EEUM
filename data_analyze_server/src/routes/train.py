from fastapi import APIRouter, Depends
from services.train import train_model
from core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/train", tags=["Train"])


@router.post("/{location_id}")
async def train_sensor_data(
    location_id: int,
    history_days: int = 14,
    lookback_days: int = 7,
    db: AsyncSession = Depends(get_db)
):
    await train_model(db, location_id, history_days, lookback_days)
    return {"message": "Model trained successfully"}
