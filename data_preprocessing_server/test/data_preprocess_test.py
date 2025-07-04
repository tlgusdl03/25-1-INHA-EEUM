# import sys
# import os

# # src 폴더를 import 경로에 추가
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# import pytest
# import pytest_asyncio
# from models import Location, IoTDevice, SensorData
# from preprocessors.missing_handler import missing_data_check, _missing_avg_cache
# from preprocessors.outlier_handler import outlier_data_check, _stat_cache
# from database import async_session
# from datetime import datetime, timedelta
# from decimal import Decimal
# from utils.common_time import NOW
# from sqlalchemy import select, func

# def create_test_data():
#     print("테스트 데이터 생성")

#     return SensorData(
#         device_id=1,
#         temperature=Decimal("999.0"),  # 이상치
#         humidity=None,      # 결측치
#         tvoc=Decimal("350.0"),
#         noise=Decimal("80.0"),
#         pm10=Decimal("25.0"),
#         pm2_5=None          # 결측치
#     )

# @pytest_asyncio.fixture(scope="function")
# async def insert_dummy_data():
#     print("더미 센서 데이터 삽입 시작")
#     async with async_session() as session:
#         now = NOW()
#         # 1. 센서 데이터 60개 삽입
#         dummy_entries = []
#         for i in range(60):  # 60분치
#             dummy_entries.append(SensorData(
#                 device_id=1,
#                 temperature=Decimal(20 + i % 5),
#                 humidity=Decimal(40 + i % 10),
#                 tvoc=Decimal(100 + i * 2),
#                 noise=Decimal(60 + i % 3),
#                 pm10=Decimal(20 + i % 7),
#                 pm2_5=Decimal(10 + i % 4),
#                 collected_at=now - timedelta(minutes=i)
#             ))
#         session.add_all(dummy_entries)
#         await session.commit()
#         count = await session.scalar(select(func.count()).select_from(SensorData))
#         assert count > 0, "❌ sensor_datas에 데이터가 없음"
#         await session.close()

#     yield  # 테스트 끝나고 나면 여기로 옴

#     # 테스트 후 정리
#     print("테스트 종료 후 더미 데이터 삭제")
#     async with async_session() as session:
#         await session.execute("DELETE FROM sensor_datas WHERE device_id = 1")
#         await session.commit()
    
# @pytest.mark.asyncio
# async def test_outlier_and_missing_data_check(insert_dummy_data):
#     print("🧪 이상치 + 결측치 처리 통합 테스트")
#     _stat_cache["timestamp"] = None
#     _missing_avg_cache["timestamp"] = None

#     # 1. 테스트용 데이터 생성
#     data = create_test_data()

#     # 2. 이상치 처리
#     data = await outlier_data_check(data)
#     print("⛔ 이상치 처리 결과:", data)

#     assert data.temperature is None     # 이상치로 제거됨
#     assert data.tvoc is None            # 이상치로 제거됨
#     assert data.noise is None           # 이상치로 제거됨
#     assert data.pm10 == 25.0            # 정상값 유지

#     # 3. 결측치 처리
#     data = await missing_data_check(data)
#     print("🩺 결측치 보완 결과:", data)

#     assert data.temperature is not None  # 평균으로 대체
#     assert data.humidity is not None     # 평균으로 대체
#     assert data.pm2_5 is not None        # 평균으로 대체
#     assert data.tvoc is not None         # 결측 -> 평균 대체