from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.score import Score
from models.report import Report
from sqlalchemy import select, insert, func
from services.weather import fetch_forecast, fetch_air_pollution
from services.location import get_latlon_by_id
from services.score import read_score
from services.location import get_name
from services.statistics import get_min_max_mean
from schemas.report import ReportResponse
from datetime import datetime, timedelta
from utils.report import (
    AIR_RULES, DI_RULES, NOISE_RULES, crowd_time_message, describe_pattern, PATTERN_TEXT
)

async def write_report(
    location_id: int,
    db: AsyncSession,
):
  # 1) 가장 최근 레코드 1건
  scores = await read_score(db=db, location_id=location_id)
  # 2) location name 생성
  location_name = await get_name(db=db, location_id=location_id)

  # 3) 리포트 생성
  report_outside = await report_outside_brief(db=db, location_id=location_id)
  report = generate_report(scores, location_name)
  report += report_outside

  stmt = (
     insert(Report)
     .values(
        location_id=location_id,
        created_at=func.now(),
        content=report
     ).returning(Report.report_id)
  ) 
  result = await db.execute(stmt)
  await db.commit()
  return result.scalar_one()

def generate_report(scores: Score, location_name: str | None = None):
    """
    사용자 전체 피드백 문장을 만들어 반환
    """
    if location_name:
        header = f"{location_name} - "
    report = header
    report += generate_air_report(scores)
    report += generate_di_report(scores)
    report += generate_noise_report(scores)
    return f"{report}"

def generate_air_report(scores: Score) -> str: 
    """
    공기질 관련련 피드백 문장을 만들어 반환
    """
    air_score = scores.cai_score

    if air_score is None:
        return "공기질질 정보가 부족하여 분석할 수 없습니다.\n"
    
    for threshold, label, advice in AIR_RULES:
        body = ""
        if air_score >= threshold:
            body = f"공기질: [{label}]"
            detail = (
                f" 행동 가이드: {advice}"
            )
            return f"{body}{detail}\n"
    # 이론상 도달 불가
    return "점수를 확인할 수 없습니다."

def generate_di_report(scores: Score) -> str:
    """
    온,습도 불쾌지수 피드백 문장을 만들어 반환
    """
    if scores.discomfort_score is None:
        return "불쾌지수 정보가 부족하여 분석할 수 없습니다.\n"
    
    for threshold, label, advice in DI_RULES:
        if scores.discomfort_score >= threshold:
            body = f"불쾌지수: [{label}]"
            detail = (
                f" 행동 가이드: {advice}"
            )
            return f"{body} {detail}\n"
    # 이론상 도달 불가
    return "점수를 확인할 수 없습니다."

def generate_noise_report(scores: Score) -> str:
    """
    온,습도 불쾌지수 피드백 문장을 만들어 반환
    """
    if scores.noise_score is None:
        return "소음 정보가 부족하여 분석할 수 없습니다.\n"
    
    for threshold, label, advice in NOISE_RULES:
        if scores.noise_score >= threshold:
            body = f"소음: [{label}]"
            detail = (
                f" 행동 가이드: {advice}"
            )
            return f"{body} {detail}\n"
    # 이론상 도달 불가
    return "점수를 확인할 수 없습니다."

async def report_outside_brief(db: AsyncSession, location_id: int) -> ReportResponse:
    coordinate = await get_latlon_by_id(db=db, location_id=location_id)
    if coordinate is None:
      raise HTTPException(404, "location_id not found")
    ny, nx = coordinate #long, lang

    try:
      forecast_data = await fetch_forecast(nx, ny)
      air_data = await fetch_air_pollution(searchDate=datetime.now()-timedelta(days=1))
    except Exception as e:
      raise HTTPException(status_code=502, detail=str(e))

    content = ""
    content += air_data.informCause + "\n"
    content += air_data.informOverall + "\n"

    forecast_data = forecast_data.category_value_dict

    # 1) 기온
    if "TMP" in forecast_data:
        t = float(forecast_data["TMP"])
        temp_txt = f"{abs(int(t))}도"
        if t < 0:
            temp_txt = f"영하 {temp_txt}" 
        content += f"기온은 {temp_txt}입니다. "

    # 2) 하늘 / 강수
    sky_map = {"1": "맑고 ", "3": "구름이 많고 ", "4": "흐리고 "}
    if forecast_data["PTY"] != "0":          # 강수 형태 우선
        pty_map = {"1": "비가 내리고 ", "2": "비 또는 눈이 오고 ", "3": "눈이 내리고 ", "4": "소나기가 내리고 "}
        content += (pty_map.get(forecast_data["PTY"]))
    else:
        content += (sky_map.get(forecast_data.get("SKY")))

    # 3) 습도
    if "REH" in forecast_data:
        h = int(forecast_data["REH"])
        hum_txt = "건조" if h < 40 else "보통" if h < 70 else "습한"
        content += (f"습도는 {h}%로 {hum_txt} 편입니다. ")

    # 4) 강수확률
    if "POP" in forecast_data:
        p = int(forecast_data["POP"])
        pop_txt = "높습니다" if p >= 60 else "낮습니다"
        content += (f"강수확률은 {p}%로 {pop_txt}. ")

    # 5) 바람
    if "WSD" in forecast_data and "VEC" in forecast_data:
        s = float(forecast_data["WSD"])
        d = _wind_direction(forecast_data["VEC"])
        speed_txt = "약한 바람" if s < 4 else "산들바람" if s < 7 else "강한 바람"
        content += (f"{speed_txt}({s} m/s)의 {d}풍이 불겠습니다. ")
    return content
    # await _save_report(location_id=location_id, content=content, db=db)
    # report = await _get_report(location_id=location_id, db=db)
    # report_response = ReportResponse.model_validate(report)

    # return report_response

def _wind_direction(deg: str | float) -> str:
    deg = float(deg)
    dirs = ["북", "북동", "동", "남동", "남", "남서", "서", "북서"]
    return dirs[int(deg / 45)]

async def _save_report(location_id: int, content: str, db: AsyncSession):
    stmt = (
      insert(Report)
      .values(
        location_id=location_id,
        created_at=func.now(),
        content=content
      )
      .returning(Report.report_id)
    ) 

    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one()

async def _get_report(location_id: int, db: AsyncSession) -> Report:
    stmt = (
        select(Report)
        .where(Report.location_id == location_id)
        .order_by(Report.created_at.desc())
        .limit(1)   
    )
    result = await db.execute(stmt)
    report = result.scalar_one()
    return report
