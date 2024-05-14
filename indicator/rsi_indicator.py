from indicator.indicator import Indicator
import pandas_ta as ta
from constants import constants
class RSI(Indicator):
    def __init__(self, period=14, timeframe='D'):
        self.name = "RSI"
        self.period = period
        self.timeframe = timeframe

    def getName(self):
        return self.name

    def calculateValue(self, df):
        # Implementation of RSI calculation
        df['RSI'] = ta.rsi(df['close'], length=self.period).round(2)
        value = {
            constants.CURR: df['RSI'].iloc[-1],
            constants.PREV: df['RSI'].iloc[-2]
        }
        return value

    def isCriteriaSatisfied(self, df, operator):
        if operator.getName() == "Above":
            return df['close'].iloc[-1] > self.calculateValue(df)[constants.CURR]

        elif operator.getName() == "Below":
            return df['close'].iloc[-1] < self.calculateValue(df)[constants.CURR]

        elif operator.getName() == "CrossAbove":
            curr_value = self.calculateValue(df)[constants.CURR]
            prev_value = self.calculateValue(df)[constants.PREV]
            return prev_value < 30 and curr_value > 30

        elif operator.getName() == "CrossBelow":
            curr_value = self.calculateValue(df)[constants.CURR]
            prev_value = self.calculateValue(df)[constants.PREV]
            return prev_value > 70 and curr_value < 70

    def get_data_requirements(self):
        return round(self.period * 4.61)