from .criteria import Criteria
from models.operator import Operator
from typing import Any
from indicator.avwap_resistance_indicator import AVWAPResistance
from calendar_utils import get_anchor_date
from constants import constants

class AVWAPResistanceCriteria(Criteria):
    type: str = 'AVWAPResistance'
    period: int
    timeframe: str
    operator: Operator


    def __init__(self, **data):
        super().__init__(**data)

    def is_satisfied(self, df: Any) -> bool:
        avwap_resistance_obj = AVWAPResistance(self.period, self.timeframe)
        curr_value = avwap_resistance_obj.calculateValue(df)[constants.CURR]
        prev_value = avwap_resistance_obj.calculateValue(df.drop(df.index[-1]))[constants.CURR]

        print(f"symbol: {df['symbol']}  close: {df['close'].iloc[-1]} avwap: {curr_value}")

        if self.operator.getName() == "Above":
            return df['close'].iloc[-1] > curr_value
        elif self.operator.getName() == "Below":
            return df['close'].iloc[-1] < curr_value
        elif self.operator.getName() == "CrossAbove":
            return df[constants.CLOSE][-2] < prev_value and df[constants.CLOSE][-1] > curr_value
        elif self.operator.getName() == "CrossBelow":
            return df[constants.CLOSE][-2] > prev_value and df[constants.CLOSE][-1] < curr_value
        return False

    def get_data_requirements(self):
        return AVWAPResistance(self.period, self.timeframe).get_data_requirements()

    def get_start_date(self):
        return get_anchor_date(self.get_data_requirements(), 'D')