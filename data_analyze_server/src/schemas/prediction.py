from pydantic import BaseModel, field_serializer
from datetime import datetime

class PredictionItem(BaseModel):
    datetime: datetime
    temperature: float
    humidity: float
    tvoc: float
    noise: float
    pm10: float
    pm2_5: float

    # 소수점 2자리로 직렬화
    @field_serializer(
        "temperature",
        "humidity",
        "tvoc",
        "noise",
        "pm10",
        "pm2_5",
        mode="plain"
    )
    def _round_floats(self, value):
        if isinstance(value, list):
            # 리스트면 각 원소를 반올림
            return [round(v, 2) for v in value]
        elif isinstance(value, float):
            # 그냥 float이면 바로 반올림
            return round(value, 2)
        else:
            return value

class PredictionResponse(BaseModel):
    predictions: list[PredictionItem]
