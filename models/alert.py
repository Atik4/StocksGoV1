from pydantic import BaseModel
from models.criteria.criteria import Criteria
from models.criteria.rsi_criteria import RSICriteria
from models.criteria.ema_criteria import EMACriteria
from models.criteria.ma_criteria import MACriteria
from models.criteria.avwap_criteria import AVWAPResistanceCriteria
from models.criteria.volume_criteria import VolumeCriteria
from models.criteria.market_cap_criteria import MarketCapCriteria
from models.criteria.yearly_high_criteria import YearlyHigh
from typing import List, Union
from models.user import User


class Alert(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    criteria_list: List[Union[RSICriteria, EMACriteria, MACriteria, AVWAPResistanceCriteria, VolumeCriteria, MarketCapCriteria, YearlyHigh]]
    users: List[User]
