import pandas as pd

# Read the CSV file
df = pd.read_csv('/Users/atik.agarwal/Projects/personal/trading/stock_utils/Stock_Symbols_NSE.csv', nrows=2190)

filtered_df = df
# Get the list of symbols
symbols_list = filtered_df['Symbol'].tolist()

# print(f"Symbols with MarketCap > 100000: {symbols_list}")


import csv

def load_symbols_from_csv(filename):
    symbols_dict = {}

    with open(filename, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            symbol = row['SYMBOL']
            nse_symbol = row['NSE_SYMBOL']
            symbols_dict[symbol] = nse_symbol

    return symbols_dict


filename = "/Users/atik.agarwal/Projects/personal/StocksGo/StocksGo/stock_utils/Equity_symbols.csv"
symbols_dict = load_symbols_from_csv(filename)

# for stock in symbols_list:
#     if stock in symbols_dict:
#         print(f"stock: {stock} symbol{symbols_dict[stock]}")


def get_symbol_for_stock(stock):
    if stock in symbols_dict:
        return symbols_dict[stock]
    return None

def get_market_cap_for_stock(symbol):
    stock_df = df[df['Symbol'] == symbol]

    # Check if the DataFrame is not empty (i.e., the symbol was found)
    if not stock_df.empty:
        # Extract the MarketCap value
        market_cap = stock_df['MarketCap'].iloc[0]
        return market_cap
    else:
        return 0

# print(df)
# print(get_symbol_for_stock("SIEMENS"))
print(get_market_cap_for_stock('HAL'))