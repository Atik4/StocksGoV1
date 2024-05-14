from criteria.criteria import Criteria
from indicator.ma_indicator import MA
from constants import constants
from calendar_utils import get_anchor_date

class MACriteria(Criteria):
    def __init__(self, period, operator, timeframe='D'):
        self.name = "MA"
        self.period = period
        self.timeframe = timeframe
        self.operator = operator
        self.ma_obj = MA(self.period, self.timeframe)

    def getName(self):
        return self.name

    def isSatisfied(self, df):
        ma_obj = self.ma_obj
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
        return self.ma_obj.get_data_requirements()

    def get_start_date(self):
        return get_anchor_date(self.get_data_requirements(), 'D')