from datetime import datetime, timedelta
from schemas.statistics import StatisticsResponse, AggregatedStats
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from models.sensor_data import SensorData
from fastapi import HTTPException

async def get_min_max_mean(
    db: AsyncSession, 
    location_id: int, 
    lookback_days: int) -> StatisticsResponse :
  """
    지정한 location_id의 lookback_days 기간(UTC 기준) 동안
    temperature·humidity·tvoc·noise·pm10·pm2_5의
    min / max / mean을 한번에 집계하여 반환.
  """
  start_time = datetime.now() - timedelta(days=lookback_days)

  stmt = (
    select(
       # temperature
            func.min(SensorData.temperature),
            func.max(SensorData.temperature),
            func.avg(SensorData.temperature),
            # humidity
            func.min(SensorData.humidity),
            func.max(SensorData.humidity),
            func.avg(SensorData.humidity),
            # tvoc
            func.min(SensorData.tvoc),
            func.max(SensorData.tvoc),
            func.avg(SensorData.tvoc),
            # noise
            func.min(SensorData.noise),
            func.max(SensorData.noise),
            func.avg(SensorData.noise),
            # pm10
            func.min(SensorData.pm10),
            func.max(SensorData.pm10),
            func.avg(SensorData.pm10),
            # pm2_5
            func.min(SensorData.pm2_5),
            func.max(SensorData.pm2_5),
            func.avg(SensorData.pm2_5),
    )
    .where(
      SensorData.location_id == location_id,
      SensorData.collected_at >= start_time
    )
  )
  
  row = (await db.execute(stmt)).one()

# ────────────── ① 집계 결과 자체가 없을 때 ──────────────
  if row is None:
      raise HTTPException(
          status_code=404,
          detail=f"No sensor data found for location_id={location_id}",
      )

# ────────────── ② 일부 센서 값이 None인 경우 ──────────────
  if any(value is None for value in row):
      raise HTTPException(
          status_code=422,
          detail="Not enough data to compute statistics (contains NULL)",
      )

# ────────────── ③ 정상 응답 ──────────────
  return StatisticsResponse(
        location_id=location_id,
        lookback_days=lookback_days,
        temperature=AggregatedStats(min=row[0],  max=row[1],  mean=row[2]),
        humidity   =AggregatedStats(min=row[3],  max=row[4],  mean=row[5]),
        tvoc       =AggregatedStats(min=row[6],  max=row[7],  mean=row[8]),
        noise      =AggregatedStats(min=row[9],  max=row[10], mean=row[11]),
        pm10       =AggregatedStats(min=row[12], max=row[13], mean=row[14]),
        pm2_5      =AggregatedStats(min=row[15], max=row[16], mean=row[17]),
    )
  