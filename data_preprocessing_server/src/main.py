from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from models import *
from pydanticModels import *
from database import get_db
from contextlib import asynccontextmanager
import threading
import mqtt_client
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 FastAPI lifespan start - MQTT 실행")
    loop = asyncio.get_event_loop()
    mqtt_client.init(loop)
    threading.Thread(target=mqtt_client.run_mqtt, daemon=True).start()
    yield
    print("🧹 FastAPI lifespan end")
    
app = FastAPI(title="test", lifespan=lifespan, root_path="/api1")

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

# ---------- 엔드포인트 ----------
@app.get("/test")
async def test():
    return "ok"

@app.get("/locations")
async def get_locations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Location))
    return result.scalars().all()

@app.get("/locations/{location_id}")
async def location_get_by_id(location_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Location).where(Location.location_id == location_id))
    location = result.scalar_one_or_none()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@app.get("/iot_devices/{location_id}")
async def get_iot_devices_by_location_id(location_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(IoTDevice).where(IoTDevice.location_id == location_id))
    iot_devices = result.scalars().all()
    return iot_devices


@app.get("/scores", response_model=list[ScoreResponse])
async def get_scores(db: AsyncSession = Depends(get_db)):
    subq = (
        select(
            Score.location_id,
            func.max(Score.created_at).label("max_created_at")
        )
        .group_by(Score.location_id)
        .subquery()
    )

    ScoreAlias = aliased(Score)

    stmt = (
        select(ScoreAlias)
        .join(subq, (ScoreAlias.location_id == subq.c.location_id) & (ScoreAlias.created_at == subq.c.max_created_at))
    )

    result = await db.execute(stmt)
    return result.scalars().all()

@app.get("/scores/{location_id}", response_model=ScoreResponse)
async def get_score_by_location_id(location_id: int, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Score)
        .where(Score.location_id == location_id)
        .order_by(desc(Score.created_at))
        .limit(1)
    )
    result = await db.execute(stmt)
    score = result.scalar_one_or_none()
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")
    return score

@app.get("/reports", response_model=list[ReportResponse])
async def get_reports(db: AsyncSession = Depends(get_db)):
    subq = (
        select(
            Report.location_id,
            func.max(Report.created_at).label("max_created_at")
        )
        .group_by(Report.location_id)
        .subquery()
    )

    ReportAlias = aliased(Report)

    stmt = (
        select(ReportAlias)
        .join(subq, (ReportAlias.location_id == subq.c.location_id) & (ReportAlias.created_at == subq.c.max_created_at))
    )

    result = await db.execute(stmt)
    return result.scalars().all()

@app.get("/reports/{location_id}", response_model=ReportResponse)
async def get_report_by_location_id(location_id: int, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Report)
        .where(Report.location_id == location_id)
        .order_by(desc(Report.created_at))
        .limit(1)
    )
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return ReportResponse(
        report_id=report.report_id,
        location_id=report.location_id,
        content=report.content,
    )

# @app.post("/feedbacks", response_model=FeedbackResponse)
# async def create_feedback(feedback: FeedbackCreate, db: AsyncSession = Depends(get_db)):
#     created_feedback = await feedback_create(feedback, db)
#     return created_feedback

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
