from typing import Union
from models.criteria.rsi_criteria import RSICriteria
from models.criteria.ema_criteria import EMACriteria
from models.criteria.ma_criteria import MACriteria
from models.criteria.avwap_criteria import AVWAPResistanceCriteria
from models.criteria.volume_criteria import VolumeCriteria
from models.criteria.market_cap_criteria import MarketCapCriteria
from models.criteria.yearly_high_criteria import YearlyHigh

CriteriaUnion = Union[RSICriteria, EMACriteria, MACriteria, AVWAPResistanceCriteria, VolumeCriteria, MarketCapCriteria, YearlyHigh]