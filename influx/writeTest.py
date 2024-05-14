from influxTest import client
# from influxdb_client_3 import InfluxDBClient3, Point
import os, time
import pandas as pd
from mainV3 import fyers
from utils import get_historical_data_v1
from data_utils import data_utils
from stock_utils.all_stocks_list import symbols_list

token = "InR7yqiHQAQNVmR1od6IVpGoHu-BoFT2Qjd6L7-zH_TCGloL0iFTOoegZWo3ragfgravEZ57itww-l16GrxG_Q=="
print(token)
org = "Test"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"
database="StocksGoV1"




# for key in data:
#     point = (
#         Point("stock_prices")
#         .tag("symbol", key)
#         .field("open", data[key]["open"])
#         .field("high", data[key]["high"])
#         .field("low", data[key]["low"])
#         .field("close", data[key]["close"])
#         .time("2024-02-22T00:00:00Z")
#     )
#     client.write(database=database, record=point)
#     # time.sleep(1) # separate points by 1 second


def transform_dataframe(df, symbol):
    # Rename columns
    df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']

    # Convert time column to datetime and then to ISO format for InfluxDB
    df['time'] = pd.to_datetime(df['time'], format='%d-%m-%Y %H:%M:%S').dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Add symbol column
    df['symbol'] = symbol

    return df

def ingest_data(symbol, period):
    table_name = "stock_ohlcv"
    df = data_utils.get_candles_data_for_given_period(symbol, "D", period, fyers)
    transformed_df = transform_dataframe(df, symbol)
    print(transformed_df)
    client.process_dataframe(transformed_df, table_name, tag_columns=["symbol"], database=database, timestamp_column="time")
    print("Data ingested for ", symbol)



error_symbols = []
# symbol = "NESTLEIND"
# ingest_data(symbol, 2000)
count = 1987
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

# symbol = "NESTLEIND
# transformed_df[['open', 'high', 'low', 'close']] = transformed_df[['open', 'high', 'low', 'close']].round().astype(int)


# client.process_dataframe(transformed_df, "stock_prices", tag_columns=["symbol"], database=database, timestamp_column="time")
#
#
print("Complete. Return to the InfluxDB UI.")
print(error_symbols)

