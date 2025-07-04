from pydantic import BaseModel, ConfigDict
class ReportResponse(BaseModel):
  report_id: int
  location_id: int
  content: str

  model_config = ConfigDict(from_attributes=True)

