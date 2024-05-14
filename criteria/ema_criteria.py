from criteria.criteria import Criteria
from indicator.ema_indicator import EMA
from constants import constants
from calendar_utils import get_anchor_date

class EMACriteria(Criteria):
    def __init__(self, period, operator, timeframe='D'):
        self.period = period
        self.timeframe = timeframe
        self.operator = operator
        self.name = "EMA"
        self.ema_obj = EMA(self.period, self.timeframe)

    def getName(self):
        return self.name

    def isSatisfied(self, df):
        ema_obj = self.ema_obj
        ema_value = ema_obj.calculateValue(df)

        print(f"symbol: {df['symbol']}  close: {df['close'].iloc[-1]} ema: {ema_value[constants.CURR]}")

        if self.operator.getName() == "Above":
            return df['close'].iloc[-1] > ema_value[constants.CURR]
        elif self.operator.getName() == "Below":
            return df['close'].iloc[-1] < ema_value[constants.CURR]
        elif self.operator.getName() == "CrossAbove":
            return df['close'].iloc[-2] < ema_value[constants.PREV] and df['close'].iloc[-1] > ema_value[constants.CURR]
        elif self.operator.getName() == "CrossBelow":
            return df['close'].iloc[-2] > ema_value[constants.PREV] and df['close'].iloc[-1] < ema_value[constants.CURR]
        return False

    def get_data_requirements(self):
        return self.ema_obj.get_data_requirements()

    def get_start_date(self):
        return get_anchor_date(self.get_data_requirements(), 'D')