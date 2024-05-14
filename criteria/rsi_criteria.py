from criteria.criteria import Criteria
from indicator.rsi_indicator import RSI
from constants import constants
from calendar_utils import get_anchor_date

class RSICriteria(Criteria):

    def __init__(self, period, threshold, operator, timeframe='D'):
        self.name = "RSI"
        self.period = period
        self.timeframe = timeframe
        self.threshold = threshold
        self.operator = operator
        self.rsi_obj = RSI(self.period, self.timeframe)

    def getName(self):
        return self.name

    def isSatisfied(self, df):
        rsi_obj = self.rsi_obj
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
        return self.rsi_obj.get_data_requirements()

    def get_start_date(self):
        return get_anchor_date(self.get_data_requirements(), 'D')
