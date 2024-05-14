from indicator.indicator import Indicator
from constants import constants

class VolumeIndicator(Indicator):
    def __init__(self, period, timeframe='D'):
        self.name = self.getName()
        self.period = period
        self.timeframe = timeframe

    def getName(self):
        return 'VolumeIndicator'

    def calculateValue(self, dataframe):
        return dataframe.iloc[constants.VOLUME][-1]

    def calculate_avg_volume(self, period, dataframe):
        df = dataframe.tail(period)
        volumes = df[constants.VOLUME].values
        return round(sum(volumes)/(len(volumes)))

    def get_data_requirements(self):
        return self.period
