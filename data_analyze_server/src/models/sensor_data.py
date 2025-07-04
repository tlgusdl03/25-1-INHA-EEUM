from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.sql import func
from core.db import Base

class SensorData(Base):
    __tablename__ = "sensor_datas"
    location_id = Column(Integer, ForeignKey("locations.location_id"), primary_key=True)
    collected_at = Column(DateTime, primary_key=True)
    temperature = Column(Numeric(6, 2))
    humidity = Column(Numeric(6, 2))
    tvoc = Column(Numeric(6, 2))
    noise = Column(Numeric(6, 2))
    pm10 = Column(Numeric(6, 2))
    pm2_5 = Column(Numeric(6, 2))