from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from routes import report, patterns, statistics, trend, prediction, train
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from jobs.snapshot import register_jobs
from jobs.train import register_jobs as train_register_jobs
from jobs.pattern import register_jobs as pattern_register_jobs

scheduler = AsyncIOScheduler(timezone="Asia/Seoul")
# ─────────────────── lifespan 컨텍스트 ────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: 스케줄러 구동
    register_jobs(scheduler)
    train_register_jobs(scheduler)
    pattern_register_jobs(scheduler)
    scheduler.start()
    print("APS-scheduler started.")
    try:
        yield                                      # 앱 실행 구간
    finally:
        # shutdown: 스케줄러 정지
        scheduler.shutdown()
        print("APS-scheduler stopped.")

app = FastAPI(title="IoT Score API", lifespan=lifespan, root_path="/api2")

origins = [
    "*",
    # "http://localhost:8000",
    # "http://43.201.82.148:*",
    # "http://43.201.82.148"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],    # GET, POST, PUT, DELETE 등
    allow_headers=["*"],
)


app.include_router(report.router)
app.include_router(patterns.router)
app.include_router(statistics.router)
app.include_router(trend.router)
app.include_router(prediction.router)
app.include_router(train.router)

# 간단한 헬스체크 엔드포인트
@app.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"db": result.scalar()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
