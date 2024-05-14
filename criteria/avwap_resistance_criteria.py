from criteria.criteria import Criteria
from indicator.avwap_resistance_indicator import AVWAPResistance
from constants import constants
from calendar_utils import get_anchor_date

class AVWAPCriteria(Criteria):
    def __init__(self, period, operator, timeframe='D'):
        self.name = "AVWAP"
        self.period = period
        self.timeframe = timeframe
        self.operator = operator
        self.avwap_resistance_obj = AVWAPResistance(self.period, self.timeframe)

    def getName(self):
        return self.name

    def isSatisfied(self, df):
        avwap_resistance_obj = self.avwap_resistance_obj
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
        return self.avwap_resistance_obj.get_data_requirements()

    def get_start_date(self):
        return get_anchor_date(self.get_data_requirements(), 'D')