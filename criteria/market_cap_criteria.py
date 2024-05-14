from criteria.criteria import Criteria
from constants.constants import BETWEEN, ABOVE, BELOW
from stock_utils.all_stocks_list import get_market_cap_for_stock


class MarketCapCriteria(Criteria):
    def getName(self):
        return self.name

    def isSatisfied(self, df):
        pass

    def satisfies(self, symbol):
        operator = self.operator
        market_cap = get_market_cap_for_stock(symbol)
        condition = operator["condition"]

        if condition == BETWEEN:
            lower_bound = operator["lower_bound"]
            upper_bound = operator["upper_bound"]

            if lower_bound < market_cap < upper_bound:
                return True

        if condition == ABOVE:
            threshold = operator["threshold"]
            return market_cap > threshold

        if condition == BELOW:
            threshold = operator["threshold"]
            return market_cap < threshold

    def get_data_requirements(self):
        pass

    def __init__(self, operator):
        self.name = "MarketCap"
        self.operator = operator
