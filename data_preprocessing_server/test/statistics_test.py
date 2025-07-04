# import sys
# import os
# import asyncio
# import pytest
# import pytest_asyncio
# from datetime import datetime, timedelta

# # src 경로 추가
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# from models import SensorData
# from database import async_session
# from preprocessors.outlier_handler import get_recent_statistics, _stat_cache
# from preprocessors.missing_handler import get_recent_avg, _missing_avg_cache
# from utils.common_time import NOW

# @pytest_asyncio.fixture(scope="function")
# async def insert_dummy_data():
#     now = NOW()
#     dummy_entries = [
#         SensorData(
#             device_id=1,
#             temperature=20.0 + i % 3,
#             humidity=40.0 + i % 5,
#             tvoc=100.0 + i,
#             noise=60.0 + i % 2,
#             pm10=20.0 + i % 4,
#             pm2_5=10.0 + i % 3,
#             collected_at=now - timedelta(minutes=i),
#         )
#         for i in range(60)
#     ]

#     async with async_session() as session:
#         session.add_all(dummy_entries)
#         await session.commit()
#         await session.close()

#     yield

#     async with async_session() as session:
#         from sqlalchemy import text
#         await session.execute(text("DELETE FROM sensor_datas WHERE device_id = 1"))
#         await session.commit()

# # # 📊 통계값 테스트
# # @pytest.mark.asyncio
# # async def test_get_recent_statistics(insert_dummy_data):
# #     stats = await get_recent_statistics(hours=2)
# #     print(stats["temperature"][0], stats["humidity"][1], stats["pm2_5"][2])
# #     assert stats["temperature"][0] is not None
# #     assert stats["humidity"][1] is not None
# #     assert stats["pm2_5"][2] is not None

# # # 📈 평균값 테스트
# # @pytest.mark.asyncio
# # async def test_get_recent_avg(insert_dummy_data):
# #     averages = await get_recent_avg(hours=2)
# #     assert averages["tvoc"] is not None
# #     assert averages["noise"] is not None

# @pytest.mark.asyncio
# async def test_statistics_and_avg(insert_dummy_data):
#     # 📊 통계값 테스트
#     stats = await get_recent_statistics(hours=2)
#     print("통계값 확인 (median, Q1, Q3):")
#     print("temperature:", stats["temperature"])
#     print("humidity:", stats["humidity"])
#     print("pm2_5:", stats["pm2_5"])
    
#     assert stats["temperature"][0] is not None  # median
#     assert stats["humidity"][1] is not None     # Q1
#     assert stats["pm2_5"][2] is not None        # Q3

#     # 📈 평균값 테스트
#     averages = await get_recent_avg(hours=2)
#     print("평균값 확인:")
#     print("tvoc:", averages["tvoc"])
#     print("noise:", averages["noise"])

#     assert averages["tvoc"] is not None
#     assert averages["noise"] is not None