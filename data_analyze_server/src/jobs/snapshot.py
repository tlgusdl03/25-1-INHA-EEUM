from sqlalchemy import select
from fastapi import HTTPException
from core.db import AsyncSessionLocal
from models.location import Location
from services.score import write_score
from services.report import write_report
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def send_score():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Location.location_id))
        location_ids = [row[0] for row in result.fetchall()]

        for loc in location_ids:
            try:
                await write_score(session, loc)
            except HTTPException as exc:
                # 데이터 없거나 NULL → 스킵 / 로깅
                print(f"[{loc}] skip -> {exc.detail}")

        await session.commit()

async def send_3hour_report():
    async with AsyncSessionLocal() as session:
      result = await session.execute(select(Location.location_id))
      location_ids = [row[0] for row in result.fetchall()]

      for location_id in location_ids:
          try:
              await write_report(db=session, location_id= location_id)
          except HTTPException as exc:
              # 데이터 없거나 NULL → 스킵 / 로깅
              print(f"[{location_id}] skip -> {exc.detail}")


def register_jobs(scheduler: AsyncIOScheduler):
    scheduler.add_job(send_score, IntervalTrigger(hours=3))
    scheduler.add_job(send_3hour_report, CronTrigger(hour='7,10,13,16,19,22', minute=0))