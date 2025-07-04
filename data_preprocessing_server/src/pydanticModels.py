from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ScoreCreate(BaseModel):
  location_id: int
  total_score: float  
  discomfort_score: float
  cai_score: float    
  noise_score: float  

class ScoreResponse(ScoreCreate):
  score_id: int

  model_config = ConfigDict(from_attributes=True)

class ReportCreate(BaseModel):
  location_id: int
  content: str

class ReportResponse(ReportCreate):
    report_id: int

    model_config = ConfigDict(from_attributes=True)

class FeedbackCreate(BaseModel):
  location_id: int
  satisfaction_score: int

class FeedbackResponse(FeedbackCreate):
  feedback_id: int

  model_config = ConfigDict(from_attributes=True)
