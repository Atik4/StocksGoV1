from models.criteria.rsi_criteria import RSICriteria
from models.criteria.ema_criteria import EMACriteria
from models.criteria.avwap_criteria import AVWAPResistanceCriteria
from models.criteria.yearly_high_criteria import YearlyHigh
from models.criteria.market_cap_criteria import MarketCapCriteria
from operator_condition.operator import Above, CrossAbove
from constants import constants

from calendar_utils import get_anchor_date, get_today_in_yyyy_mm_dd
from data_utils import data_utils


def apply_stock_criteria(symbol, df, criteria_list):
    print(f"Checking criteria for symbol: {symbol}")

    for criteria in criteria_list:

        if isinstance(criteria, MarketCapCriteria):
            if not criteria.satisfies(symbol):
                return False
            continue

        if not criteria.is_satisfied(df):
            return False

    print(f"Criteria satisfied for {symbol}")
    return True


def run(timeframe, criteria_list):
    oldest_date = criteria_list[0].get_start_date()
    for criteria in criteria_list:
        if isinstance(criteria, MarketCapCriteria):
            continue
        oldest_date = min(oldest_date, criteria.get_start_date())

    # print(f"data required for days: {}")

    df = data_utils.fetch_data_for_screener_with_start_date(oldest_date, timeframe)

    # print(df)
    ans = []

    for symbol, group in df.groupby('symbol'):
        print(f"Processing data for {symbol}")

        if apply_stock_criteria(symbol, group, criteria_list):
            ans.append(symbol)

        # print(group)

    print(ans)
    return ans


# def run(timeframe, criteria_list):
#     number_of_candles_data_required = 0
#     for criteria in criteria_list:
#         number_of_candles_data_required = max(number_of_candles_data_required, criteria.get_data_requirements())
#
#     print(f"data required for days: {number_of_candles_data_required}")
#
#     df = data_utils.fetch_data_for_screener(number_of_candles_data_required, timeframe)
#
#     # print(df)
#     ans = []
#     for symbol, group in df.groupby('symbol'):
#         print(f"Processing data for {symbol}")
#
#         if apply_stock_criteria(symbol, group, criteria_list):
#            ans.append(symbol)
#
#
#         # print(group)
#
#     print(ans)


if __name__ == "__main__":
    criteria_list = []
    timeframe = 'D'
    # criteria1 = RSICriteria(period=14, threshold=75, CrossAbove(), timeframe='D')
    criteria2 = EMACriteria(10, Above(), 'D')
    criteria3 = AVWAPResistanceCriteria(50, Above(), 'D')
    criteria4 = YearlyHigh()
    criteria5 = MarketCapCriteria({"condition": constants.BETWEEN, "upper_bound": 13464613, "lower_bound": 3384184})
    criteria_list.append(criteria1)
    criteria_list.append(criteria2)
    # criteria_list.append(criteria3)
    criteria_list.append(criteria4)
    criteria_list.append(criteria5)

    run('D', criteria_list)
