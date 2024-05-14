from models.criteria.rsi_criteria import RSICriteria
from models.criteria.ema_criteria import EMACriteria
from models.criteria.ma_criteria import MACriteria
from models.criteria.criteria import Criteria
from models.criteria.avwap_criteria import AVWAPResistanceCriteria
from models.criteria.volume_criteria import VolumeCriteria
from models.criteria.market_cap_criteria import MarketCapCriteria
from models.criteria.yearly_high_criteria import YearlyHigh

class CriteriaFactory:
    @staticmethod
    def create(criteria_type: str, **data) -> Criteria:
        criteria_map = {
            "RSI": RSICriteria,
            "EMA": EMACriteria,
            "MA": MACriteria,
            "AVWAPResistance": AVWAPResistanceCriteria,
            "MarketCap": MarketCapCriteria,
            "52WeekHigh": YearlyHigh,
            "Volume": VolumeCriteria
            # Add more mappings as needed
        }
        return criteria_map[criteria_type](**data)