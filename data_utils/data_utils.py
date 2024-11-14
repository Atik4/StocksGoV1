import datetime
from utils import get_historical_data, convert_column_from_epoch_to_date, get_historical_data_v1
from calendar_utils import get_anchor_date_for_ma, get_anchor_date, get_today_in_yyyy_mm_dd
import pandas as pd
from mainV3 import fyers
from dao import ohlc_couchbase_dao
# from dao import couchbase_cloud
from dao import ohlc_dao
from dao.ohlc_couchbase_dao_cloud import CouchbaseCloud
from dao.ohlc_couchbase_dao_local import CouchbaseLocal

# def get_candles_data_for_ma(symbol, timeframe, period, fyers):
#     today = datetime.date.today()
#     range_from = get_anchor_date_for_ma(period, timeframe)
#     range_to = today.strftime("%Y-%m-%d")
#     print(range_from)
#     df = get_historical_data(fyers, symbol, timeframe, "2023-02-03", range_to)
#     if df.empty:
#         return df
#
#     df[0] = convert_column_from_epoch_to_date(df[0])
#
#     print(df)
#     return df


from datetime import timedelta


def get_candles_data_for_given_period_for_ma(symbol, timeframe, period, fyers):
    range_from = datetime.datetime.strptime(get_anchor_date_for_ma(period, timeframe), "%Y-%m-%d")
    return get_data(range_from, symbol, timeframe, period, fyers)


def get_candles_data_for_given_period(symbol, timeframe, period, fyers):
    range_from = datetime.datetime.strptime(get_anchor_date(period, timeframe), "%Y-%m-%d")
    return get_data(range_from, symbol, timeframe, period, fyers)


def get_data(range_from, symbol, timeframe, period, fyers):
    today = datetime.date.today()
    range_to = datetime.datetime(today.year, today.month, today.day)
    print(range_from)

    # Initialize an empty DataFrame
    df = pd.DataFrame()

    # Check if range_from and range_to are more than 365 days apart
    if (range_to - range_from).days > 365:
        # Create a loop that iterates over the range in chunks of 365 days or less
        while range_from < range_to:
            end_range = range_from + timedelta(days=365)
            if end_range > range_to:
                end_range = range_to

            chunk_df = get_historical_data_v1(fyers, symbol, timeframe, range_from.strftime("%Y-%m-%d"),
                                              end_range.strftime("%Y-%m-%d"))
            range_from = end_range + timedelta(days=1)

            if chunk_df.empty:
                continue
            df = pd.concat([df, chunk_df])
    else:
        df = get_historical_data_v1(fyers, symbol, timeframe, range_from.strftime("%Y-%m-%d"),
                                    range_to.strftime("%Y-%m-%d"))
        if df.empty:
            return df

    return df


def get_last_traded_price(symbol):
    try:
        if "NIFTY" in symbol:
            symbol = f"NSE:{symbol}-INDEX"
        else:
            symbol = f"NSE:{symbol}-EQ"

        data = {
            "symbols": symbol
        }

        response = fyers.quotes(data=data)
        print(response)
        return response["d"][0]["v"]["lp"]
    except Exception as e:
        print(e)
        return None


# def fetch_data_for_screener(period, timeframe):
#     start_date = get_anchor_date(period, timeframe)
#     end_date = get_today_in_yyyy_mm_dd()
#
#     df = ohlc_couchbase_dao.query_all_stocks_data_between_time_range(start_date, end_date)
#
#     return df


# def fetch_data_for_screener_with_start_date(start_date, timeframe):
#     end_date = get_today_in_yyyy_mm_dd()
#     df = ohlc_couchbase_dao.query_all_stocks_data_between_time_range(start_date, end_date)
#     return df

def fetch_data_for_screener_with_start_date(start_date, timeframe):
    end_date = get_today_in_yyyy_mm_dd()
    # dao = CouchbaseCloud()
    dao = CouchbaseLocal()
    df = dao.query_all_stocks_data_between_time_range(start_date, end_date)
    return df
