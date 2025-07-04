from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from schemas.report import ReportResponse 
from models.report import Report 
from sqlalchemy import select, insert
from services.location import get_name
from services.report import write_report
from typing import List

router = APIRouter(prefix="/report", tags=["Report"])

@router.get("/", response_model=str)
async def read_report(
    location_id: int = Query(description="location 식별자"),
    db: AsyncSession = Depends(get_db),
):
  report = (
        await db.execute(
            select(Report)
            .where(Report.location_id == location_id)
            .order_by(Report.created_at.desc())
            .limit(1)
        )
    ).scalar_one()

  return report.content

@router.get("/all", response_model=List[ReportResponse])
async def read_sensor_report(
    location_id: int = Query(description="location 식별자"),
    db: AsyncSession = Depends(get_db),
):
  reports = (
        await db.execute(
            select(Report)
            .where(Report.location_id == location_id)
            .order_by(Report.created_at.desc())
        )
    ).scalars().all()

  return reports

@router.post("", response_model=int)
async def write_three_report(
  location_id: int = Query(description="location 식별자"),
  db: AsyncSession = Depends(get_db),
):
  return await write_report(db=db, location_id=location_id)