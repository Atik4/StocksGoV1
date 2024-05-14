from pydantic import BaseModel
from models.criteria_types import CriteriaUnion
from typing import List


class ScreenerRequest(BaseModel):
    timeframe: str
    criteria: List[CriteriaUnion]
