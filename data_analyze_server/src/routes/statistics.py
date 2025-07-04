from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.statistics import StatisticsRequest, StatisticsResponse
from services.statistics import get_min_max_mean
from core.db import get_db

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get("/all", response_model=StatisticsResponse)
async def read_all_statistics(
    params: StatisticsRequest = Depends(),  # location_id, lookback_days(1~7)
    db: AsyncSession = Depends(get_db),
):
    """
    여러 센서의 min·max·mean을 한 번에 반환.
    """
    return await get_min_max_mean(
        db=db,
        location_id=params.location_id,
        lookback_days=params.lookback_days,
    )