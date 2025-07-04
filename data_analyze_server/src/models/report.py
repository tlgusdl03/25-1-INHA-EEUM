from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from core.db import Base

class Report(Base):
    __tablename__ = "reports"
    report_id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.location_id"))
    created_at = Column(DateTime)
    content = Column(String)