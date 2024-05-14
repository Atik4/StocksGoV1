from .criteria import Criteria
from models.operator import Operator
from typing import Any
from indicator.rsi_indicator import RSI
from constants import constants
from calendar_utils import get_anchor_date


class RSICriteria(Criteria):
    type: str = 'RSI'
    period: int
    timeframe: str
    threshold: int
    operator: Operator
    # rsi_obj: RSI = None


    def __init__(self, **data):
        super().__init__(**data)

        # self.rsi_obj = RSI(self.period, self.timeframe)

    def is_satisfied(self, df: Any) -> bool:
        # rsi_obj = self.rsi_obj
        rsi_obj = RSI(self.period, self.timeframe)
        rsi_value = rsi_obj.calculateValue(df)

        print(f"symbol: {df['symbol']}  close: {df['close'].iloc[-1]} rsi: {rsi_value[constants.CURR]}")

        if self.operator.getName() == "Above":
            return rsi_value[constants.CURR] > self.threshold
        elif self.operator.getName() == "Below":
            return rsi_value[constants.CURR] < self.threshold
        elif self.operator.getName() == "CrossAbove":
            return rsi_value[constants.PREV] < self.threshold and rsi_value[constants.CURR] > self.threshold
        elif self.operator.getName() == "CrossBelow":
            return rsi_value[constants.PREV] > self.threshold and rsi_value[constants.CURR] < self.threshold
        return False

    def get_data_requirements(self):
        rsi_obj = RSI(self.period, self.timeframe)
        return rsi_obj.get_data_requirements()
        # return self.rsi_obj.get_data_requirements()

    def get_start_date(self):
        return get_anchor_date(self.get_data_requirements(), 'D')