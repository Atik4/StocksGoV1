import time
import pandas as pd
# from influxTest import client
from influx.influxTest import client
import pandas_ta as pta
from influx.query_generator import generate_influx_query

start = time.time()
token = "InR7yqiHQAQNVmR1od6IVpGoHu-BoFT2Qjd6L7-zH_TCGloL0iFTOoegZWo3ragfgravEZ57itww-l16GrxG_Q=="
print(token)
org = "Test"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"
database="StocksGoV1"


def get_data_for_batch(symbols, range_from, range_to, table_name):
    query = generate_influx_query(symbols, range_from, range_to, table_name)
    print(query)
    table = client.query(query=query, database=database, language='sql')
    df = table.to_pandas()
    return df


def get_ath_value(table_name, symbol):
    query = f"""SELECT max("high") FROM "{table_name}" WHERE "symbol" = '{symbol}'"""
    table = client.query(query=query, database=database, language='sql')
    df = table.to_pandas()
    return df

print(get_ath_value("stock_prices", "ASIANPAINT"))


# symbols = ['ITC', 'TCS', 'RELIANCE']
# range_from = '2024-01-10'
# range_to = '2024-02-29'
# get_data_for_batch(symbols, range_from, range_to, "stock_prices")

# query = """SELECT *
# FROM 'stock_prices'
# WHERE "symbol" = 'ASIANPAINT'"""

# query = """SELECT *
# FROM "stock_prices"
# WHERE time = '2024-02-27T05:30:00Z'
# AND "close" < "21ema" """
#
# table = client.query(query=query, database=database, language='sql')
#
# # Convert to dataframe
# df = table.to_pandas().sort_values(by="time")
# df["21ema"] = pta.ema(df["close"], 21)
# df["21ema"] = df["21ema"].round(2)

# print(df)
#
# client.process_dataframe(df, "stock_prices", tag_columns=["symbol"], database=database, timestamp_column="time")

end = time.time()

# print(f"Time taken: {end - start} seconds")