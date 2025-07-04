from pydantic import BaseModel, Field, field_serializer
from typing import Literal

class StatisticsRequest(BaseModel):
    """
    조회 대상 장소(location_id)와
    현재 시점에서 며칠 전까지 데이터를 조회할지(lookback_days)를 받는 입력 모델
    """
    location_id: int
    lookback_days: int = Field(
        default=1,          # 기본값 1일
        ge=1,               # 최소 1일
        le=7,               # 최대 7일
        description="How many days to look back (1-7)"
    )
    

class AggregatedStats(BaseModel):
    """한 센서의 최소·최대·평균 값"""
    min: float = Field(description="가장 낮은 값")
    max: float = Field(description="가장 높은 값")
    mean: float = Field(description="평균 값")

    # ── ⚡️ 소수점 2자리로 반올림하여 JSON 직렬화 ──
    @field_serializer("min", "max", "mean", return_type=float)
    def _round_two_decimals(self, value):
        # 내부 계산값은 유지하고, 응답(JSON)만 2째 자리로
        return round(value, 2)

    
class AggregatedSensors(BaseModel):
    temperature: AggregatedStats
    humidity: AggregatedStats
    tvoc: AggregatedStats
    noise: AggregatedStats
    pm10: AggregatedStats
    pm2_5: AggregatedStats

    unit_temperature: Literal["°C"] = "°C"
    unit_humidity:    Literal["%"]   = "%"
    unit_tvoc:        Literal["ppb"] = "ppb"
    unit_noise:       Literal["dB(A)"] = "dB(A)"
    unit_pm:          Literal["µg/m³"] = "µg/m³"

class StatisticsResponse(AggregatedSensors):
    location_id: int
    lookback_days: int = Field(
        default=1,
        ge=1,
        le=7,
        description="How many days to look back (1-7)"
    )




