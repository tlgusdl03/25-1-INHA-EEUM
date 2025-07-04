from datetime import datetime
from pydantic import BaseModel, ConfigDict

class SensorDataCreate(BaseModel):
    location_id: int
    collected_at: datetime
    temperature: float | None = None
    humidity: float | None = None
    tvoc: float | None = None
    noise: float | None = None
    pm10: float | None = None
    pm2_5: float | None = None
class SensorDataRequest(SensorDataCreate):

    model_config = ConfigDict(from_attributes=True)

class SensorDataResponse(SensorDataCreate):
    
    model_config = ConfigDict(from_attributes=True)

class SensorDataOut(BaseModel):
    location_id: int
    value: float
    collected_at: datetime

    model_config = ConfigDict(from_attributes=True)


