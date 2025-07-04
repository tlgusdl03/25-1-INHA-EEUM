from pydantic import BaseModel
from typing import Dict

class FcstResponse(BaseModel):
    category_value_dict: Dict[str, str]

class AirPollution(BaseModel):
   informCause: str
   informOverall: str
