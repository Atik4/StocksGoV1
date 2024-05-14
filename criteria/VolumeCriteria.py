from criteria.criteria import Criteria
from constants import constants
from indicator.volume_indicator import VolumeIndicator
from calendar_utils import get_anchor_date

class VolumeCriteria(Criteria):

    def __init__(self, period, operator, threshold, timeframe='D'):
        self.name = self.getName()
        self.period = period
        self.timeframe = timeframe
        self.operator = operator
        self.threshold = threshold
        self.volume_indicator_obj = VolumeIndicator(period, timeframe)

    def getName(self):
        return 'VolumeCriteria'

    def isSatisfied(self, df):
        avg_volume = self.volume_indicator_obj.calculate_avg_volume(period=self.period, dataframe=df)

        if self.operator.getName() == constants.ABOVE :
            return avg_volume > self.threshold

        if self.operator.getName() == constants.BELOW :
            return avg_volume < self.threshold

    def get_data_requirements(self):
        self.volume_indicator_obj.get_data_requirements()

    def get_start_date(self):
        return get_anchor_date(self.get_data_requirements(), 'D')