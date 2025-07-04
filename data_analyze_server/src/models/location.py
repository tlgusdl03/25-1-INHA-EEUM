from sqlalchemy import Column, String, Integer
from core.db import Base

class Location(Base):
    __tablename__ = "locations"
    location_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    coordinates = Column(String, nullable=False)
    uri = Column(String, nullable=False)