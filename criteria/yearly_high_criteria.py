from criteria.criteria import Criteria
from calendar_utils import get_one_year_ago
from constants.constants import HIGH
import numpy as np

class YearlyHigh(Criteria):

    def __init__(self):
        self.name = "52WeekHigh"

    def getName(self):
        return self.name

    def isSatisfied(self, df):
        high_prices = df[HIGH].values
        max_high_index = np.argmax(high_prices)
        return max_high_index == len(high_prices) - 1

    def get_data_requirements(self):
        pass

    def get_start_date(self):
        return get_one_year_ago()