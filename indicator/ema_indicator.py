from indicator.indicator import Indicator
import pandas_ta as ta
from constants import constants

class EMA(Indicator):
    def __init__(self, period, timeframe='D'):
        self.name = f"{period}EMA"
        self.period = period
        self.timeframe = timeframe

    def getName(self):
        return self.name

    def calculateValue(self, df):
        # Implementation of EMA calculation
        df[self.getName()] = ta.ema(df['close'], length=self.period).round(2)

        value = {
            constants.CURR: df[self.getName()].iloc[-1],
            constants.PREV: df[self.getName()].iloc[-2]
        }
        return value

    def get_data_requirements(self):
        return round(self.period * 4.61)