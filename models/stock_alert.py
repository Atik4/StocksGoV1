from pydantic import BaseModel
from typing import List
from models.alert import Alert


class StockAlert(BaseModel):
    class Config:
        orm_mode = True

    symbol: str
    alerts: List[Alert]

