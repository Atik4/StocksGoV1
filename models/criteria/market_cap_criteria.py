from .criteria import Criteria
from models.operator import Operator
from typing import Any
from constants.constants import BETWEEN, ABOVE, BELOW
from stock_utils.all_stocks_list import get_market_cap_for_stock


class MarketCapCriteria(Criteria):
    type: str = 'MarketCap'
    operator: Operator

    class Config:
        arbitrary_types_allowed = True

    def satisfies(self, symbol):
        operator = self.operator
        market_cap = get_market_cap_for_stock(symbol)
        condition = operator.getName()

        if condition == BETWEEN:
            lower_bound = operator.get_lower_bound()
            upper_bound = operator.get_upper_bound()

            if lower_bound < market_cap < upper_bound:
                return True

        if condition == ABOVE:
            lower_bound = operator.get_lower_bound()
            return market_cap > lower_bound

        if condition == BELOW:
            upper_bound = operator.get_upper_bound()
            return market_cap < upper_bound

    def is_satisfied(self, df: Any) -> bool:
        pass

    def get_data_requirements(self):
        pass