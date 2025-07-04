from models import SensorData
from sqlalchemy import select, func
from database import async_session
from datetime import datetime, timedelta, timezone
from utils.common_time import NOW
from decimal import Decimal

SENSOR_COLUMNS = ["temperature", "humidity", "tvoc", "noise", "pm10", "pm2_5"]

_stat_cache = {
    "timestamp" : None,
    "values": None,
}

async def get_recent_statistics(hours: int = 1, min_count: int = 60):
    now = NOW()
    cached = _stat_cache["values"]
    if (
        _stat_cache["timestamp"] and 
        (now - _stat_cache["timestamp"]).total_seconds() < 60 * 60 and
        cached and
        any(med is not None for (med, _, _) in cached.values())  # median이 하나라도 유효하면 캐시 사용
    ):
        print("통계값 캐시 사용 (1시간 이내)")
        for k, (med, q1, q3) in cached.items():
            print(f" - {k}: median={med}, Q1={q1}, Q3={q3}")
        return cached

    from_time = now - timedelta(hours=hours)
    print(f"📊 통계값 계산 시작 (최근 {hours}시간 기준)")

    async with async_session() as session:
        stmt = select(
            SensorData.temperature,
            SensorData.humidity,
            SensorData.tvoc,
            SensorData.noise,
            SensorData.pm10,
            SensorData.pm2_5,
        ).where(SensorData.collected_at >= from_time)

        result = await session.execute(stmt)
        rows = result.all()
        print(f"📎 수집된 데이터 row 수: {len(rows)}")

    if len(rows) < min_count:
        print(f"❌ 데이터 개수 {len(rows)}개로 부족하여 전처리 생략 (최소 {min_count} 필요)")
        _stat_cache["timestamp"] = now
        _stat_cache["values"] = {col: (None, None, None) for col in SENSOR_COLUMNS}
        return _stat_cache["values"]

    # 컬럼별로 분리
    columns_data = {col: [] for col in SENSOR_COLUMNS}
    for row in rows:
        for i, col in enumerate(SENSOR_COLUMNS):
            value = row[i]
            if value is not None:
                columns_data[col].append(value)

    # 통계 계산
    stats = {}
    for col, values in columns_data.items():
        if not values:
            stats[col] = (None, None, None)
            continue

        values_sorted = sorted(values)
        n = len(values_sorted)
        median = values_sorted[n // 2]
        q1 = values_sorted[n // 4]
        q3 = values_sorted[(3 * n) // 4]
        stats[col] = (median, q1, q3)

    print("✅ 통계값 계산 완료:")
    for k, (med, q1, q3) in stats.items():
        print(f" - {k}: median={med}, Q1={q1}, Q3={q3}")

    _stat_cache["timestamp"] = now
    _stat_cache["values"] = stats

    return stats


async def outlier_data_check(data: SensorData) -> SensorData:
    print("이상치 탐지 시작")
    stats = await get_recent_statistics(hours=24)

    for key in SENSOR_COLUMNS:
        value = getattr(data, key)
        median, q1, q3 = stats.get(key, (None, None, None))
        print(f"[{key}] median: {median}, Q1: {q1}, Q3: {q3}")

        if value is None or q1 is None or q3 is None:
            print(f"{key}는 결측 또는 기준 없음 → 이상치 판별 제외")
            continue

        iqr = q3 - q1
        lower_bound = q1 - Decimal(1.5) * iqr
        upper_bound = q3 + Decimal(1.5) * iqr
        print(f"값: {value}, 기준: {lower_bound} ~ {upper_bound}")


        if not (lower_bound <= value <= upper_bound):
            print(f"이상치 감지 → {key}: {value} → None으로 대체")
            setattr(data, key, None)
        else:
            print(f"{key}: {value} → 정상")

    print("이상치 처리 완료")
    return data