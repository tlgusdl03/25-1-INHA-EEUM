from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.db import get_db
from services.patterns import update_pattern_cache_for_location

async def update_pattern_task():
  for location_id in [1, 2, 3, 4, 5]:
    for lookback_days in [1,7]:
      async for session in get_db():
        try:
          await update_pattern_cache_for_location(session, location_id, lookback_days)
        finally:
          await session.close()
        break

def register_jobs(scheduler: AsyncIOScheduler):
  scheduler.add_job(
    update_pattern_task,
    trigger='cron',
    hour=2,
    minute=0,
    id='daily_pattern_update',
    replace_existing=True,
  )
