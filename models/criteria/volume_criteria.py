from .criteria import Criteria
from models.operator import Operator
from typing import Any
from indicator.volume_indicator import VolumeIndicator
from calendar_utils import get_anchor_date
from constants import constants


class VolumeCriteria(Criteria):
    type: str = 'Volume'
    period: int
    timeframe: str
    operator: Operator
    threshold: int

    def __init__(self, **data):
        super().__init__(**data)

    def is_satisfied(self, df: Any) -> bool:
        avg_volume = VolumeIndicator(self.period, self.timeframe).calculate_avg_volume(period=self.period, dataframe=df)

        if self.operator.getName() == constants.ABOVE :
            return avg_volume > self.threshold

        if self.operator.getName() == constants.BELOW :
            return avg_volume < self.threshold

    def get_data_requirements(self):
        VolumeIndicator(self.period, self.timeframe).get_data_requirements()

    def get_start_date(self):
        return get_anchor_date(self.get_data_requirements(), 'D')