import pandas_ta as pta
from utils import get_historical_data, convert_column_from_epoch_to_date
from data_utils import data_utils
from utils import get_historical_data_v1
from mainV3 import fyers
from datetime import datetime, timedelta
import calendar_utils
# import ma_dao
def get_ema(symbol, timeframe, period):
    try:


        field = construct_ma_string(period, "ema")
        # info = ma_dao.get_stock_moving_average_info(symbol)
        info = {"symbol": "MANINFRA", "moving_averages": {"21ema": {"value": 228.04975894732786, "date": "09-02-2024 05:30:00"}, "10ema": {"value": 231.93077904026055, "date": "09-02-2024 05:30:00"}}, "ltp": 226}
        if info is not None:
             if field in info["moving_averages"]:
                prev_ema = info["moving_averages"][field]["value"]
                date = info["moving_averages"][field]["date"]

                date_obj = datetime.strptime(date, "%d-%m-%Y %H:%M:%S").strftime("%Y-%m-%d")
                date_obj = datetime.strptime(date_obj, "%Y-%m-%d")


                print(date_obj)
                lwd_from_today = calendar_utils.get_last_working_day()
                lwd_from_today_date_obj = datetime.strptime(lwd_from_today, "%Y-%m-%d")
                print(lwd_from_today_date_obj)
                diff = lwd_from_today_date_obj - date_obj
                if diff.days == 0:
                    return prev_ema

                range_from = (date_obj + timedelta(days=1)).strftime("%Y-%m-%d")

                print(lwd_from_today)

                df = get_historical_data_v1(fyers, symbol, "D", range_from, lwd_from_today)
                df[field] = calculate_ema_from_previous_date(prev_ema, df[4], period)
                return df
        #
        #          return info["moving_averages"][field]
        df = data_utils.get_candles_data_for_given_period_for_ma(symbol, timeframe, period, fyers)
        # print(df)

        df[field] = pta.ema(df[4], period)
        print(df)

        return df
    except Exception as e:
        print(e)
        return None

def get_ma(symbol, timeframe, period):
    df = data_utils.get_candles_data_for_given_period_for_ma(symbol, timeframe, period, fyers)
    # print(df)
    field = f"{period}ma"
    df[field] = pta.sma(df[4], period)
    print(df)
    return df

def construct_ma_string(period, ma):
    return f"{period}{ma}"


def calculate_ema_from_previous_date(prev_ema, closing_prices, period):
    smoothing_factor = 2/(period + 1)
    ema_today = prev_ema
    ema_list = []
    for closing_price in closing_prices:
        ema_today = (closing_price*smoothing_factor) + (ema_today*(1 - smoothing_factor))
        ema_list.append(ema_today)
    return ema_list


# get_ema("MANINFRA", "D", 21)
# prev_ema = 228.05
# closing_prices = [225, 220, 223]
# print(calculate_ema_from_previous_date(prev_ema, closing_prices, 21))
