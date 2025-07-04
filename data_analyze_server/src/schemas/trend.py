from datetime import datetime
from typing import Literal
from pydantic import BaseModel

# ──────────────────────── Pydantic ↓ ────────────────────────
class MAItem(BaseModel):
    collected_at: datetime
    value: float
    ma: float

class MAResponse(BaseModel):
    location_id: int
    metric: str
    method: Literal["sma", "ema"]
    window: int
    start: datetime
    end: datetime
    items: list[MAItem]
