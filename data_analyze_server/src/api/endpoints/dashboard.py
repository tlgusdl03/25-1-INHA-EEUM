# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from models.database import SessionLocal
# from services.score import compute_total_score
# from services.report import generate_summary
# from schemas.dashboard import DashboardResponse
# from services.weather import fetch_external_weather

# router = APIRouter()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.get("/dashboard", response_model=DashboardResponse)
# async def read_dashboard(db: Session = Depends(get_db)):
#     # 1. 최근 sensor_data 가져오기 (device별 latest)
#     latest = db.query(...).order_by(...).first()
#     # 2. 점수 계산
#     scores = compute_total_score(latest)
#     # 3. 외부 날씨 재조회
#     weather = await fetch_external_weather(latest.location)
#     # 4. 리포트 생성
#     report = generate_summary(scores, weather)
#     return DashboardResponse(**scores, report=report)
