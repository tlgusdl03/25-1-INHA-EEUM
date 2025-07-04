# routers/moving_average.py
from datetime import datetime
from typing import Literal, Annotated
import pandas as pd
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.trend import MAItem, MAResponse
from core.db import get_db          # 세션 DI
from models.sensor_data import SensorData             # Declarative model
from services.trend import add_moving_average

router = APIRouter(prefix="/trend", tags=["moving-average"])

# ──────────────────────── 엔드포인트 ↓ ────────────────────────
@router.get("/{location_id}/moving-average", response_model=MAResponse, description="이동평균선 제공 API")
async def moving_average(
    location_id: int,
    metric: Annotated[
        Literal["temperature", "humidity", "tvoc", "noise", "pm10", "pm2_5"],
        Query(description="센서 항목")
    ],
    window: int = Query(15, gt=0, le=1440),          # 기본 15 샘플
    method: Literal["sma", "ema"] = Query("sma"),
    start: datetime = Query(..., description="시작 시각"),
    end: datetime = Query(..., description="조회 종료 시각"),
    session: AsyncSession = Depends(get_db),
):
    # 1) DB 조회
    stmt = (
        select(SensorData.collected_at, getattr(SensorData, metric))
        .where(
            SensorData.location_id == location_id,
            SensorData.collected_at.between(start, end),
        )
    )
    rows = (await session.execute(stmt)).all()
    if not rows:
        raise HTTPException(404, "데이터가 없습니다")

    # 2) Pandas 변환 & 이동평균
    df = pd.DataFrame(rows, columns=["collected_at", "value"])
    df["ma"] = add_moving_average(df, "value", window, method)

    # 3) 직렬화
    items = [
        MAItem(collected_at=row["collected_at"],
               value=float(row["value"]),
               ma=float(row["ma"]))
        for row in df.to_dict("records")
    ]
    return MAResponse(
        location_id=location_id,
        metric=metric,
        method=method,
        window=window,
        start=start,
        end=end,
        items=items,
    )

