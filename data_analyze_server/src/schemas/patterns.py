from pydantic import BaseModel, Field, field_serializer
from datetime import datetime
from typing import Literal

class ClusterRequest(BaseModel):
    """
    조회 대상 장소(location_id)와
    현재 시점에서 며칠 전까지 데이터를 조회할지(lookback_days)를 받는 입력 모델
    """
    location_id: int
    lookback_days: int = Field(
        default=1,
        ge=1,
        le=7,
        description="How many days to look back (1-7)"
    )

class SensorDataResponse(BaseModel):
    collected_at: datetime
    temperature: float
    humidity: float
    tvoc: float
    noise: float
    pm10: float
    pm2_5: float

class SensorDataPoint(BaseModel):
    collected_at: datetime
    value: float

class ClusterResult(BaseModel):
    optimal_k: int
    silhouette_score: float
    cluster_centers: dict[int, float]
    normalized_cluster_centers: list[float]
    original_total_data_points: int
    filtered_total_data_points: int
    outlier_removed_data_points: int
    cluster_counts: dict[int, int]
    cluster_ratios: dict[int, float]
    cluster_time_ranges: dict[int, list[datetime]]

class TimeRange(BaseModel):
    start: str
    end: str

class PeakTimeResponse(BaseModel):
    cluster_id: int
    time_range: TimeRange

# class PatternResult(BaseModel):
#     abs_pattern: str
#     rel_pattern: str
#     final_pattern: str

# class ClusterResponse(BaseModel):
#     optimal_k: int
#     silhouette_score: float
#     cluster_centers: dict[int, float]
#     cluster_counts: dict[int, int]
#     absolute_change: float
#     peak_time: list[PeakTimeResponse]
#     pattern: PatternResult
#     # 소수점 2자리로 직렬화
#     @field_serializer(
#         "absolute_change",
#         "silhouette_score",
#         "cluster_centers",
#         mode="plain"
#     )
#     def _round_floats(self, value):
#         if isinstance(value, list):
#             # 리스트면 각 원소를 반올림
#             return [round(v, 2) for v in value]
#         elif isinstance(value, float):
#             # 그냥 float이면 바로 반올림
#             return round(value, 2)
#         else:
#             return value
    
# class MultiClusterResponse(BaseModel):
#     result: dict[str, ClusterResponse]

class Pattern(BaseModel):
    pattern: Literal[
        "VERY_STABLE", "LOW", "STABLE", "MODERATE", "HIGH", "VERY_HIGH", "EXTREME"
    ]
    center_value: float
    peak_time: TimeRange
    ratio: float

    @field_serializer("center_value", "ratio")
    def serialize_center_value(self, value):
        return round(value, 2)

class PatternResponse(BaseModel):
    temperature: list[Pattern]
    humidity: list[Pattern]
    tvoc: list[Pattern]
    noise: list[Pattern]
    pm10: list[Pattern]
    pm2_5: list[Pattern]
