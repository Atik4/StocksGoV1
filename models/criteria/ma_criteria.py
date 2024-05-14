from .criteria import Criteria
from models.operator import Operator
from typing import Any
from indicator.ma_indicator import MA
from calendar_utils import get_anchor_date
from constants import constants


class MACriteria(Criteria):
    type: str = 'MA'
    period: int
    timeframe: str
    operator: Operator


    def __init__(self, **data):
        super().__init__(**data)


    def is_satisfied(self, df: Any) -> bool:
        ma_obj = MA(self.period, self.timeframe)
        ma_value = ma_obj.calculateValue(df)

        print(f"symbol: {df['symbol']}  close: {df['close'].iloc[-1]} ma: {ma_value[constants.CURR]}")

        if self.operator.getName() == "Above":
            return df['close'].iloc[-1] > ma_value[constants.CURR]
        elif self.operator.getName() == "Below":
            return df['close'].iloc[-1] < ma_value[constants.CURR]
        elif self.operator.getName() == "CrossAbove":
            return df['close'].iloc[-2] < ma_value[constants.PREV] and df['close'].iloc[-1] > ma_value[constants.CURR]
        elif self.operator.getName() == "CrossBelow":
            return df['close'].iloc[-2] > ma_value[constants.PREV] and df['close'].iloc[-1] < ma_value[constants.CURR]
        return False

    def get_data_requirements(self):
        return MA(self.period, self.timeframe).get_data_requirements()

    def get_start_date(self):
        return get_anchor_date(self.get_data_requirements(), 'D')