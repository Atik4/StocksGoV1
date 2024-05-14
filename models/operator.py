from pydantic import BaseModel
from typing import Optional


class Operator(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    type: str  # 'Above', 'Below', 'CrossAbove', 'CrossBelow', 'Between'
    lower_bound: Optional[int] = None
    upper_bound: Optional[int] = None

    def getName(self):
        return self.type

    def get_lower_bound(self):
        return self.lower_bound

    def get_upper_bound(self):
        return self.upper_bound
