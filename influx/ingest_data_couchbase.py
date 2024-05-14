import os, time
import pandas as pd
from mainV3 import fyers
from utils import get_historical_data_v1
from data_utils import data_utils
from stock_utils.all_stocks_list import symbols_list
from dao import ohlc_couchbase_dao


def transform_dataframe(df, symbol):
    # Rename columns
    df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']

    # Convert time column to datetime and then to ISO format for InfluxDB
    # df['time'] = pd.to_datetime(df['time'], format='%d-%m-%Y %H:%M:%S').dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    df['time'] = df['time'].str.replace(' 05:30:00', ' 00:00:00', regex=False)
    # Add symbol column
    df['symbol'] = symbol

    return df


def ingest_data(symbol, period):
    bucket_name = "stock_ohlc"
    df = data_utils.get_candles_data_for_given_period(symbol, "D", period, fyers)
    transformed_df = transform_dataframe(df, symbol)
    print(transformed_df)
    ohlc_couchbase_dao.upload_data_from_dataframe(df)
    print("Data ingested for ", symbol)



error_symbols = []
# symbol = "NESTLEIND"
# ingest_data(symbol, 100)
count = 0
while count < len(symbols_list):
    symbol = symbols_list[count]
    try:
        ingest_data(symbol, 2000)
        count += 1
        print("index: ", count)
        time.sleep(20)
    except Exception as e:
        print(e)
        error_symbols.append(symbol)
        time.sleep(20)
        count += 1
        continue

    if count == 500:
        break

print(error_symbols)

