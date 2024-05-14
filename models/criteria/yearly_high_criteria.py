from .criteria import Criteria
from models.operator import Operator
from typing import Any
from constants.constants import HIGH
import numpy as np
from calendar_utils import get_one_year_ago


class YearlyHigh(Criteria):
    type: str = '52WeekHigh'

    class Config:
        arbitrary_types_allowed = True

    def is_satisfied(self, df: Any) -> bool:
        high_prices = df[HIGH].values
        max_high_index = np.argmax(high_prices)
        return max_high_index == len(high_prices) - 1

    def get_data_requirements(self):
        pass

    def get_start_date(self):
        return get_one_year_ago()