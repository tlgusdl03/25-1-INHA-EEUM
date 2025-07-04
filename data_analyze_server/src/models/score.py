from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric
from core.db import Base

class Score(Base):
    __tablename__ = "scores"
    score_id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.location_id"))
    total_score = Column(Numeric(5, 2))
    discomfort_score = Column(Numeric(5, 2))
    cai_score = Column(Numeric(5, 2))
    noise_score = Column(Numeric(5, 2))
    created_at = Column(DateTime)