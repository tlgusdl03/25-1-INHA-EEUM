from pydantic import BaseModel, ConfigDict
from datetime import datetime
class ScoreResponse(BaseModel):
  score_id: int
  location_id: int
  total_score: float
  discomfort_score: float
  cai_score: float
  noise_score: float
  created_at: datetime

  model_config = ConfigDict(from_attributes=True)
