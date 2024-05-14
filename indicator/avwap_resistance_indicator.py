from indicator.indicator import Indicator
from constants import constants
import numpy as np

class AVWAPResistance(Indicator):
    def __init__(self, period, timeframe):
        self.name = f"{period}AVWAP"
        self.period = period
        self.timeframe = timeframe

    def getName(self):
        return self.name

    def calculateValue(self, original_df):
        # Implementation of AVWAP calculation
        df = original_df.tail(self.period)
        value = {
            constants.CURR: self.getValue(df),
            constants.PREV: self.calculate_prev_value(original_df)
        }
        return value

    def calculate_prev_value(self, original_df):
        df = original_df.tail(self.period + 1)

        high_prices = df[constants.HIGH].values
        volumes = df[constants.VOLUME].values

        last_high_price = high_prices[len(high_prices) - 1]
        last_volume = volumes[len(volumes) - 1]

        high_prices = high_prices[:-1]
        volumes = volumes[:-1]
        max_high_index = np.argmax(high_prices)

        high_prices_sub = high_prices[max_high_index:]
        volumes_sub = volumes[max_high_index:]

        high_prices_sub = np.append(high_prices_sub, last_high_price)
        volumes_sub = np.append(volumes_sub, last_volume)

        # Ensure there is data to process
        if len(high_prices_sub) == 0 or len(volumes_sub) == 0:
            print("Sub-array is empty, no data to process.")
            return None

        sum_of_vol_by_price = np.sum(volumes_sub * high_prices_sub)

        total_volume = np.sum(volumes_sub)

        if total_volume == 0:
            print("Total volume is zero, cannot compute AVWAP.")
            return None

        # Calculate and return AVWAP
        avwap = round(sum_of_vol_by_price / total_volume, 2)
        return avwap

        return round(sum__of_vol_by_price / total_volume, 2)



    def getValue(self, df):
        high_prices = df[constants.HIGH].values
        volumes = df[constants.VOLUME].values

        max_high_index = np.argmax(high_prices)

        high_prices_sub = high_prices[max_high_index:]
        volumes_sub = volumes[max_high_index:]

        # Ensure there is data to process
        if len(high_prices_sub) == 0 or len(volumes_sub) == 0:
            print("Sub-array is empty, no data to process.")
            return None

        sum_of_vol_by_price = np.sum(volumes_sub * high_prices_sub)

        total_volume = np.sum(volumes_sub)

        # Avoid division by zero
        if total_volume == 0:
            print("Total volume is zero, cannot compute AVWAP.")
            return None

        # Calculate and return AVWAP
        avwap = round(sum_of_vol_by_price / total_volume, 2)
        return avwap

        return round(sum__of_vol_by_price / total_volume, 2)

    def isCriteriaSatisfied(self, df, operator):
        if operator.getName() == "Above":
            return df.iloc[constants.CLOSE][-1] > self.calculate_prev_value(df)

        elif operator.getName() == "Below":
            return df.iloc[constants.CLOSE][-1] < self.calculate_prev_value(df)

        elif operator.getName() == "CrossAbove":
            curr_value = self.calculateValue(df)[constants.CURR]
            df_with_last_row_removed = df.drop(df.index[-1])
            prev_value = self.calculateValue(df_with_last_row_removed)[constants.CURR]
            return df[constants.CLOSE][-2] < prev_value and df[constants.CLOSE][-1] > curr_value

        elif operator.getName() == "CrossBelow":
            curr_value = self.calculateValue(df)[constants.CURR]
            df_with_last_row_removed = df.drop(df.index[-1])
            prev_value = self.calculateValue(df_with_last_row_removed)[constants.CURR]
            return df[constants.CLOSE][-2] > prev_value and df[constants.CLOSE][-1] < curr_value

    def get_data_requirements(self):
        return self.period + 1