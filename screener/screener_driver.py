class Screener:
    def __init__(self, criteria_list, stock_universe):
        self.criteria_list = criteria_list
        self.stock_universe = stock_universe

    def get_data_requirement(self):
        return 0

    def get_screened_list(self):
        return None