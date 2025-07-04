from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from core.db import Base

class Sensor(Base):
    __tablename__ = "sensors"
    sensor_id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("iot_devices.device_id"))
    sensor_type = Column(String)
    status = Column(String)
    interval_ms = Column(Integer)
    priority = Column(Integer)
    measured_at = Column(DateTime)