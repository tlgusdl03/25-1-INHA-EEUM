from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean
from core.db import Base

class IoTDevice(Base):
    __tablename__ = "iot_devices"
    device_id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.location_id"))
    status = Column(String)
    is_connected = Column(Boolean)
    last_sent_at = Column(DateTime)