from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import sensor_data
from datetime import datetime, timedelta, timezone
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.metrics import silhouette_score
from schemas.patterns import SensorDataPoint, ClusterRequest, SensorDataResponse, ClusterResult, PeakTimeResponse, TimeRange, Pattern, PatternResponse
from fastapi import HTTPException
from utils.cache import redis_client

ABSOLUTE_VALUE_STANDARD = {
    "temperature": {
        "EXTREME": (30, 50),
        "VERY_HIGH": (28, 30),
        "HIGH": (26, 28),
        "MODERATE": (24, 26),
        "STABLE": (22, 24),
        "VERY_STABLE": (18, 22),
        "LOW": (0, 18)
    },
    "humidity": {
        "EXTREME": (70, 100),    # 위로
        "VERY_HIGH": (60, 70),
        "HIGH": (55, 60),
        "MODERATE": (50, 55),
        "STABLE": (45, 50),
        "VERY_STABLE": (40, 45),
        "LOW": (0, 40)           # 아래로
    },
    "noise": {
        "EXTREME": (70, 120),
        "VERY_HIGH": (65, 70),
        "HIGH": (60, 65),
        "MODERATE": (55, 60),
        "STABLE": (50, 55),
        "VERY_STABLE": (40, 50),
        "LOW": (0, 40)
    },
    "tvoc": {
        "EXTREME": (3000, 10000),
        "VERY_HIGH": (1000, 3000),
        "HIGH": (500, 1000),
        "MODERATE": (300, 500),
        "STABLE": (100, 300),
        "VERY_STABLE": (0, 100)
    },
    "pm10": {
        "EXTREME": (150, 1000),
        "VERY_HIGH": (75, 150),
        "HIGH": (45, 75),
        "MODERATE": (30, 45),
        "STABLE": (15, 30),
        "VERY_STABLE": (0, 15)
    },
    "pm2_5": {
        "EXTREME": (50, 1000),
        "VERY_HIGH": (25, 50),
        "HIGH": (15, 25),
        "MODERATE": (10, 15),
        "STABLE": (5, 10),
        "VERY_STABLE": (0, 5)
    }
}

async def get_filtered_data(
    db: AsyncSession,
    request: ClusterRequest
) -> list[SensorDataResponse]:
    """
    지정한 location_id의 lookback_days 기간(UTC 기준) 동안의
    데이터를 반환
    """

    end_time = datetime.now(timezone.utc).replace(tzinfo=None)
    start_time = end_time - timedelta(days=request.lookback_days)

    result = await db.execute(
        select(sensor_data.SensorData).where(
            sensor_data.SensorData.location_id == request.location_id,
            sensor_data.SensorData.collected_at >= start_time,
            sensor_data.SensorData.collected_at <= end_time
        ).order_by(sensor_data.SensorData.collected_at)
    )
    records = result.scalars().all()

    if not records:
        raise HTTPException(
            status_code=404,
            detail=f"No sensor data found for location_id={request.location_id}",
        )
    if len(records) < 2:
        raise HTTPException(
            status_code=422,
            detail="Not enough data to compute statistics (contains NULL)",
        )

    return [
        SensorDataResponse(
            collected_at=record.collected_at,
            temperature=float(record.temperature),
            humidity=float(record.humidity),
            tvoc=float(record.tvoc),
            noise=float(record.noise),
            pm10=float(record.pm10),
            pm2_5=float(record.pm2_5)
        )
        for record in records
        if None not in (
            record.collected_at,
            record.temperature,
            record.humidity,
            record.tvoc,
            record.noise,
            record.pm10,
            record.pm2_5
        )
    ]

def remove_outliers(data_points: list[SensorDataPoint]) -> list[SensorDataPoint]:
    """
    IQR 방법을 사용하여 이상치를 제거합니다.
    Q1 - 1.5 * IQR < x < Q3 + 1.5 * IQR 범위를 벗어나는 데이터를 이상치로 간주합니다.
    """
    positive_points = [point for point in data_points if point.value >= 0]
    values = np.array([point.value for point in positive_points])

    # # Q1, Q3, IQR 계산
    # Q1 = np.percentile(values, 25)
    # Q3 = np.percentile(values, 75)
    # IQR = Q3 - Q1

    # # 이상치 범위 설정
    # lower_bound = max(0, Q1 - 1.5 * IQR)
    # upper_bound = Q3 + 1.5 * IQR

    # # 이상치가 아닌 데이터만 필터링
    # filtered_points = [
    #     point for point in positive_points
    #     if lower_bound <= point.value <= upper_bound
    # ]

    if not positive_points:
        raise HTTPException(
            status_code=424,
            detail="No data points after removing outliers",
        )

    return positive_points

def get_normalized_data(data: list[SensorDataPoint]) -> tuple[np.ndarray, StandardScaler]:
    """
    데이터를 평균 0, 표준편차 1로 정규화
    """
    scaler = StandardScaler()
    X = np.array([[point.value] for point in data])  
    X_scaled = scaler.fit_transform(X)
    return X_scaled, scaler

def get_denormalized_data(data: np.ndarray, scaler: StandardScaler) -> np.ndarray:
    """
    정규화된 데이터를 원래 데이터로 복원
    """
    X_denormalized = scaler.inverse_transform(data)
    return X_denormalized

def find_optimal_clusters(
    data_points: list[SensorDataPoint],
    max_clusters: int = 5
) -> ClusterResult:
    """
    최적의 클러스터 개수 찾기, 이후 클러스터링 진행
    """
    filtered_data_points = remove_outliers(data_points)

    X, scaler = get_normalized_data(filtered_data_points)

    silhouette_scores = []
    possible_k = range(2, min(max_clusters + 1, len(filtered_data_points)))

    for k in possible_k:
        kmeans = KMeans(n_clusters=k, random_state=42)
        labels = kmeans.fit_predict(X)

        if len(set(labels)) == 1:
            continue

        score = silhouette_score(X, labels)
        silhouette_scores.append(score)
    
    if not silhouette_scores:
        raise HTTPException(
            status_code=423,
            detail="Not enough clusters to compute statistics",
        )

    optimal_k = np.argmax(silhouette_scores) + 2
    optimal_silhouette_score = silhouette_scores[optimal_k - 2]

    final_kmeans = KMeans(n_clusters=optimal_k, random_state=42)
    cluster_labels = final_kmeans.fit_predict(X)

    normalized_cluster_centers = final_kmeans.cluster_centers_.flatten()
    cluster_centers = get_denormalized_data(
        final_kmeans.cluster_centers_, scaler).flatten()
    cluster_centers = {
        i: cluster_centers[i] for i in range(optimal_k)
    }

    cluster_time_ranges = {}
    for i in range(optimal_k):
        cluster_indices = np.where(cluster_labels == i)[0]
        if len(cluster_indices) > 0:
            cluster_times = [
                filtered_data_points[idx].collected_at for idx in cluster_indices
            ]
            cluster_time_ranges[i] = cluster_times

    # 클러스터 포인트 수
    cluster_counts = {i: int(np.sum(cluster_labels == i))
                      for i in range(optimal_k)}
    
    cluster_ratios = {
        i: cluster_counts[i] / len(filtered_data_points) for i in range(optimal_k)}

    result = ClusterResult(
        optimal_k=int(optimal_k),
        silhouette_score=float(optimal_silhouette_score),
        cluster_centers=cluster_centers,
        normalized_cluster_centers=normalized_cluster_centers.tolist(),
        original_total_data_points=len(data_points),  
        filtered_total_data_points=len(filtered_data_points),
        outlier_removed_data_points=len(data_points) - len(filtered_data_points),
        cluster_counts=cluster_counts,
        cluster_ratios=cluster_ratios,
        cluster_time_ranges=cluster_time_ranges,
    )

    return result

def extract_peak_hour(cluster_result: ClusterResult) -> list[PeakTimeResponse]:
    """
    클러스터링 결과에서 피크 시간대 추출
    """
    peak_time = []
    for index in range(cluster_result.optimal_k):
        hours = [time.hour for time in cluster_result.cluster_time_ranges[index]]
        most_common_hour = max(set(hours), key=hours.count)

        start_hour = most_common_hour
        end_hour = (start_hour + 1) % 24
        
        peak_time.append(PeakTimeResponse(
            cluster_id=index,
            time_range=TimeRange(
                start=f"{start_hour:02d}:00",
                end=f"{end_hour:02d}:00"
            )
        ))
    return peak_time

def classify_absolute_value(value: float, metric: str) -> str:
    """
    절대 값 기준 패턴 분류
    """
    threshold = ABSOLUTE_VALUE_STANDARD[metric]
    for label, (lower, upper) in threshold.items():
        if lower <= value <= upper:
            return label
    return "VERY_STABLE"
    
def final_pattern(cluster_result: ClusterResult, metric: str) -> list[Pattern]:
    """
    절대 값 기반 최종 패턴 분석
    """
    cluster_centers = cluster_result.cluster_centers
    cluster_ratios = cluster_result.cluster_ratios
    peak_time = extract_peak_hour(cluster_result)

    pattern_info_dict = {}

    seen_patterns = set()
    
    for cluster_id, center in cluster_centers.items():
        pattern = classify_absolute_value(center, metric)

        if pattern not in seen_patterns:
            # 처음 보는 패턴의 경우
            seen_patterns.add(pattern)
            info = Pattern(
                pattern=pattern,
                center_value=center,
                peak_time=peak_time[cluster_id].time_range,
                ratio=cluster_ratios[cluster_id]
            )
            pattern_info_dict[pattern] = info
        else:
            pattern_info_dict[pattern].ratio += cluster_ratios[cluster_id]

    # 딕셔너리를 리스트로 변환
    pattern_info_list = list(pattern_info_dict.values())
    
    # 심각한 순서대로 정렬
    pattern_order = ["VERY_STABLE", "LOW", "STABLE", "MODERATE", "HIGH", "VERY_HIGH", "EXTREME"]
    pattern_info_list.sort(key=lambda x: pattern_order.index(x.pattern), reverse=True)
    
    return pattern_info_list

async def update_pattern_cache_for_location(db: AsyncSession, location_id: int, lookback_days: int):
    request = ClusterRequest(
        location_id=location_id,
        lookback_days=lookback_days
    )
    result = await generate_pattern_report_service(db, request)
    await redis_client.set(f"pattern_cache:{location_id}:{lookback_days}", result.model_dump_json(), ex=60 * 60 * 24)
    print(f"Cache updated for location_id={location_id}")

async def generate_pattern_report_service(
    db: AsyncSession,
    request: ClusterRequest
) -> PatternResponse:
    """
    데이터 분포 패턴 파악 (절대값 기준 + 패턴별 분류류)
    """
    data_points = await get_filtered_data(db, request)

    metrics = ["temperature", "humidity", "tvoc", "noise", "pm10", "pm2_5"]

    response = {}

    for metric in metrics:
        metric_data = [
            SensorDataPoint(
                collected_at=dp.collected_at,
                value=getattr(dp, metric)
            )
            for dp in data_points
        ]

        # 클러스터링
        cluster_result = find_optimal_clusters(metric_data)
        
        # 최종 패턴 분석
        patterns = final_pattern(cluster_result, metric)

        # 리포트 저장
        response[metric] = patterns

    return PatternResponse(**response)
