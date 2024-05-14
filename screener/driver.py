from influx import queryInflux
from screener.rsi_screener import RSI
from stock_utils.all_stocks_list import symbols_list

# import rsi_screener
# import time
#
# start = time.time()
#
# symbols = ['ITC', 'TCS', 'RELIANCE']
# range_from = '2024-01-10'
# range_to = '2024-02-29'
# table_name = "stock_ohlcv"
#
# df = queryInflux.get_data_for_batch(symbols, range_from, range_to, "stock_prices")
# print(df)
#
# results = rsi_screener.run(symbols, df)
# print(results)
#
# end = time.time()
# print(f"Time taken: {end - start} seconds")

def partition_list(input_list, partition_size=10):
    return [input_list[i:i + partition_size] for i in range(0, len(input_list), partition_size)]


screener = RSI(14, "D")
range_from = '2023-12-10'
range_to = '2024-03-01'
table_name = "stock_ohlcv"

partitions = partition_list(symbols_list, 10)

for partition in partitions:
    df = queryInflux.get_data_for_batch(partition, range_from, range_to, "stock_prices")
    results = screener.run(df, partition)

    print(results)

