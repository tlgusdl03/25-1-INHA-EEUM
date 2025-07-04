from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer, Boolean, Numeric
from sqlalchemy.sql import func
from database import Base

class Location(Base):
    __tablename__ = "locations"
    location_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    coordinates = Column(String, nullable=False)
    uri = Column(String, nullable=False)

class IoTDevice(Base):
    __tablename__ = "iot_devices"
    device_id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.location_id"))
    status = Column(String)
    is_connected = Column(Boolean)
    last_sent_at = Column(DateTime)

class Sensor(Base):
    __tablename__ = "sensors"
    sensor_id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("iot_devices.device_id"))
    sensor_type = Column(String)
    status = Column(String)
    interval_ms = Column(Integer)
    priority = Column(Integer)
    measured_at = Column(DateTime)

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

class Score(Base):
    __tablename__ = "scores"
    score_id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.location_id"))
    total_score = Column(Numeric(5, 2))
    discomfort_score = Column(Numeric(5, 2))
    cai_score = Column(Numeric(5, 2))
    noise_score = Column(Numeric(5, 2))
    created_at = Column(DateTime)

class Report(Base):
    __tablename__ = "reports"
    report_id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.location_id"))
    created_at = Column(DateTime)
    content = Column(String)

class Feedback(Base):
    __tablename__ = "feedbacks"
    feedback_id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.location_id"))
    created_at = Column(DateTime)
    satisfaction_score = Column(Integer)
    used_for_training = Column(Boolean)
