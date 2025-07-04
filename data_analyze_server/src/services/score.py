from fastapi import HTTPException
from schemas.score import ScoreResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, insert
from models.sensor_data import SensorData
from models.score import Score
from datetime import datetime, timedelta
from utils.scoring import (                   # <- 개별 스코어 계산 함수 모듈화
    cai_score_pm10,
    cai_score_pm2_5,
    cai_score_tvoc,
    discomfort_index,
)

# ────────────────────── 등가 소음도 (Noise) ──────────────────────
#등가 소음도
#-----추후 수정 필요요
async def noise_score_mean(
    db: AsyncSession,
    location_id: int,
    ) -> float :
  now = datetime.now()
  start = now - timedelta(hours=3)
  subq = (
      select(SensorData.noise)
      .where(SensorData.location_id == location_id)
      .order_by(SensorData.collected_at.desc())
      .limit(1000)
      .subquery()
  )
  stmt = (
      select(
          func.avg(subq.c.noise).label("avg"),
      )
  )
  avg_noise = (await db.execute(stmt)).scalar_one_or_none()

  if avg_noise is None:
        return None                # 데이터가 없을 때 처리
  
  if (avg_noise > 100): avg_noise = 100
  elif (avg_noise < 50): avg_noise = 50

  score = 100 - 100 * ((avg_noise - 50) / 50)
  return score

async def get_latest_data(
    db: AsyncSession,
    location_id: int,
    ) -> SensorData:
    stmt = (
        select(
            SensorData
        )
        .where(
            SensorData.location_id == location_id
        )
        .order_by(
            SensorData.
            collected_at.desc()
        )
        .limit(1)
    )
    row = (await db.execute(stmt)).scalar_one_or_none()

    if row is None:
      raise HTTPException(404, "no sensor data")

    return row
    
# 1시간 등가 소음도
# def noise_score(db: float)

# ────────────────────── 종합 계산 헬퍼 ──────────────────────
# `sensor`는 SQLAlchemy SensorData 객체와 호환되는 형태
async def compute_scores(db: AsyncSession, location_id: int)-> Score:
    sensor = await get_latest_data(db, location_id)
    noise = float(await noise_score_mean(db, location_id))
    cai_pm10 = float(cai_score_pm10(sensor.pm10))
    cai_pm25 = float(cai_score_pm2_5(sensor.pm2_5))
    cai_tvoc = float(cai_score_tvoc(sensor.tvoc))
    cai_score = (cai_pm10 + cai_pm25 + cai_tvoc) / 3
    di  = discomfort_index(float(sensor.temperature), float(sensor.humidity))
    #----total 함수 구현 필요---
    total = (cai_score + di + noise) / 3
    return Score(
        location_id=location_id,
        cai_score=round(cai_score, 2),
        discomfort_score=round(di, 2),
        noise_score=round(noise, 2),
        total_score=round(total, 2),
        created_at= datetime.now()
    )

async def read_score(
    db: AsyncSession,
    location_id : int,
    ) -> Score :
    score = (
        await db.execute(
            select(Score)
            .where(Score.location_id == location_id)
            .order_by(Score.created_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()

    if score is None:
        raise HTTPException(
            status_code=404,
            detail=f"No score for location_id={location_id}",
        )

    return score

async def write_score(
    db:AsyncSession,
    location_id: int,
    ):
    score = await compute_scores(db, location_id)

    stmt = insert(
        Score
    ).values(
        location_id=score.location_id,
        cai_score=score.cai_score,
        discomfort_score=score.discomfort_score,
        noise_score=score.noise_score,
        total_score=score.total_score,
        created_at=score.created_at,
    ).returning(Score.score_id)

    await db.execute(stmt)
    await db.commit()