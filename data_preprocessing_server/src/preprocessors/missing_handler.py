from models import SensorData
from sqlalchemy import select, func
from database import async_session
from datetime import datetime, timedelta
from utils.common_time import NOW

SENSOR_COLUMNS = ["temperature", "humidity", "tvoc", "noise", "pm10", "pm2_5"]

_missing_avg_cache = {
    "timestamp": None,
    "values": None,
}

async def get_recent_avg(hours: int = 1, min_count: int = 60) -> dict[str, float | None]:
    now = NOW()
    cached = _missing_avg_cache["values"]
    # 캐시 유효성 검사 (1시간 유효)
    if (
        _missing_avg_cache["timestamp"] and 
        (now - _missing_avg_cache["timestamp"]).total_seconds() < 60 * 60 and
        cached and
        any(v is not None for v in cached.values())  # 하나라도 평균값이 있으면 캐시 사용
    ):
        print("평균값 캐시 사용 (1시간 이내)")
        for k, v in cached.items():
            print(f" - {k}: {v}")
        return cached
    
    since = now - timedelta(hours=hours)
    print(f"📈 평균값 계산 시작 (최근 {hours}시간)")
    

    async with async_session() as session:
        stmt_count = select(func.count()).where(SensorData.collected_at >= since)
        count_result = await session.execute(stmt_count)
        count = count_result.scalar()
        print(f"📊 통계 계산 대상 row 수: {count}")

        if count < min_count:
            print(f"❌ 평균값 계산 불가: 데이터 부족 (최소 {min_count}개 필요)")
            _missing_avg_cache["timestamp"] = now
            _missing_avg_cache["values"] = {key: None for key in SENSOR_COLUMNS}
            return _missing_avg_cache["values"]

        stmt = select(
            func.avg(SensorData.temperature),
            func.avg(SensorData.humidity),
            func.avg(SensorData.tvoc),
            func.avg(SensorData.noise),
            func.avg(SensorData.pm10),
            func.avg(SensorData.pm2_5),
        ).where(SensorData.collected_at >= since)

        result = await session.execute(stmt)
        row = result.first()

        if not row:
            print("❌ 평균값을 계산할 수 있는 row가 없습니다.")
            result_dict = {key: None for key in SENSOR_COLUMNS}
        else:
            (
                avg_temp,
                avg_humidity,
                avg_tvoc,
                avg_noise,
                avg_pm10,
                avg_pm2_5,
            ) = row

            result_dict = {
                "temperature": avg_temp,
                "humidity": avg_humidity,
                "tvoc": avg_tvoc,
                "noise": avg_noise,
                "pm10": avg_pm10,
                "pm2_5": avg_pm2_5,
            }

    print("✅ 평균값 계산 완료:")
    for k, v in result_dict.items():
        print(f"   - {k}: {v}")

    _missing_avg_cache["timestamp"] = now
    _missing_avg_cache["values"] = result_dict

    return result_dict
    
# None값이 들어오면 평균값으로 대체 하기
async def missing_data_check(data: SensorData) -> SensorData:
    print("결측치 확인 중...")
    avg_values = await get_recent_avg()

    for key in SENSOR_COLUMNS:
        if getattr(data, key) is None:
            print(f"결측치 탐지됨: {key} → 평균값으로 대체")
            avg = avg_values.get(key)
            if avg is not None:
                setattr(data, key, avg)
    
    print("✅ 결측치 처리 완료")
    return data