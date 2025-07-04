from sqlalchemy import Column, DateTime, ForeignKey, Integer, Boolean
from core.db import Base

class Feedback(Base):
    __tablename__ = "feedbacks"
    feedback_id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.location_id"))
    created_at = Column(DateTime)
    satisfaction_score = Column(Integer)
    used_for_training = Column(Boolean)