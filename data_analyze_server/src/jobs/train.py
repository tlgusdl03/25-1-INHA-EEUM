from services.train import train_model
from core.db import get_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def train_task():
    for location_id in [1, 2, 3, 4, 5]:
        async for session in get_db():
            try:
                await train_model(session, location_id=location_id, history_days=30, lookback_days=7)
            finally:
                await session.close()
            break 

def register_jobs(scheduler: AsyncIOScheduler):
    scheduler.add_job(
        train_task,
        trigger='cron',
        hour=3,
        minute=0,
        id='daily_model_training',
        replace_existing=True,
    )