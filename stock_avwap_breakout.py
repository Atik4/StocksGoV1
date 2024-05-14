import datetime
# from main import login, app_id, fyers
from stock_utils.lot_size import lot_size
from mainV3 import fyers
from stock_utils.all_stocks_list import symbols_list
from utils import get_historical_data, convert_column_from_epoch_to_date, \
    trigger_exit_order, get_anchor_date, get_previous_anchored_vwap
from concurrent.futures import ThreadPoolExecutor
import time
from prettytable import PrettyTable

# fyers = fyersModel.FyersModel(is_async=False, client_id=app_id, token=login(),
#                               log_path="/Users/atik.agarwal/Projects/personal/trading/logs/")

positions = {}
is_position = {}


def get_previous_anchored_vwap(df):
    last_row = df.iloc[-1]
    df.drop(df.index[-1], inplace=True)
    max_high_index = df[2].idxmax()

    print(df.iloc[max_high_index:][2])
    df.loc[len(df.index)] = last_row

    sum__of_vol_by_price = (df.iloc[max_high_index:][5] * df.iloc[max_high_index:][2]).sum()
    total_volume = df.iloc[max_high_index:][5].sum()
    info = {
        "symbol": "",
        "closing_price": 0,
        "avwap": round(sum__of_vol_by_price / total_volume, 2),
        "anchor_date": df[0][max_high_index],
        "total_period": len(df) - max_high_index
    }

    return info



# Function to check if the exit conditions for a strategy are met
def exit_conditions_met(position, closing_price):
    if position.get_direction() == "up" and position.get_entry_price() - closing_price >= position.get_sl_underlying():
        print("stop loss hit: exit condition met")
        return True

    if position.get_direction() == "up" and closing_price - position.get_entry_price() >= position.get_target():
        print("target achieved: exit condition met")
        return True

    if position.get_direction() == "down" and closing_price - position.get_entry_price() >= position.get_sl_underlying():
        print("stop loss hit: exit condition met")
        return True

    if position.get_direction() == "down" and position.get_entry_price() - closing_price >= position.get_target():
        print("target achieved: exit condition met")
        return True

    return False


def get_candles_data(symbol, timeframe, period):
    today = datetime.date.today()
    range_from = get_anchor_date(period, timeframe)
    range_to = today.strftime("%Y-%m-%d")
    print(range_from)
    df = get_historical_data(fyers, symbol, timeframe, range_from, range_to)
    if df.empty:
        return df

    df[0] = convert_column_from_epoch_to_date(df[0])

    print(df)
    return df


def check_for_existing_position(symbol, closing_price):
    if symbol in positions:
        if exit_conditions_met(positions[symbol], closing_price):
            trigger_exit_order(positions[symbol], positions, fyers)
            print(len(positions))
            return True
    return False


broken_out_list = []
broken_out_list_dict = []

def check_for_breakout(symbol, df, prev_closing_price, closing_price, timeframe, period):
    try:
        # avwap = get_anchored_vwap(fyers, symbol, timeframe, period)
        info = get_previous_anchored_vwap(df)
        avwap = info["avwap"]
        print(f"closing price: {closing_price} and avwap: {avwap}")
        if closing_price > avwap > prev_closing_price:
            print(f"{symbol} has broken out from AVWAP at {avwap}")
            anchor_date = info["anchor_date"]
            total_period = info["total_period"]
            print(f"anchor date: {anchor_date} and total period: {total_period}")
            broken_out_list.append(symbol)
            info["symbol"] = symbol
            info["closing_price"] = closing_price
            broken_out_list_dict.append(info)
            return True
        return False
    except Exception as e:
        print(e)


def check_one(symbol, timeframe, period):
    try:
        df = get_candles_data(f"NSE:{symbol}-EQ", timeframe, period)
        if df.empty:
            return

        closing_prices = df[4]
        last_index = len(closing_prices) - 1

        if check_for_existing_position(symbol, closing_prices[last_index]):
            return

        # if check_for_breakout(f"NSE:{symbol}-EQ", closing_prices[last_index], timeframe, period):
        #     return
        check_for_breakout(f"NSE:{symbol}-EQ", df, closing_prices[last_index - 1], closing_prices[last_index], timeframe,
                           period)

        # else:
        #     print("Order not placed now since price is: " + str(closing_prices[last_index]))
    except Exception as e:
        print(e)


def check(symbols, timeframe, period):
    try:
        for symbol in symbols:
            check_one(symbol, timeframe, period)
            time.sleep(0.5)
    except Exception as e:
        print(e)


# def check(symbols, timeframe, period):
#     try:
#         for symbol in symbols:
#             df = get_candles_data(f"NSE:{symbol}-EQ", timeframe, period)
#             if df.empty:
#                 continue
#
#             closing_prices = df[4]
#             last_index = len(closing_prices) - 1
#
#             if check_for_existing_position(symbol, closing_prices[last_index]):
#                 continue
#
#             # if check_for_breakout(f"NSE:{symbol}-EQ", closing_prices[last_index], timeframe, period):
#             #     return
#             check_for_breakout(f"NSE:{symbol}-EQ", closing_prices[last_index - 1], closing_prices[last_index], timeframe, period)
#
#             # else:
#             #     print("Order not placed now since price is: " + str(closing_prices[last_index]))
#     except Exception as e:
#         print(e)
#

start = time.time()
sym = []
for i in range(700):
    sym.append(symbols_list[i])

with ThreadPoolExecutor(max_workers=10) as executor:
    # check(lot_size, "D", 100)
    check(sym, "D", 100)
print(broken_out_list)

table = PrettyTable()

# Add columns to the table
table.field_names = list(broken_out_list_dict[0].keys())

# Add data to the table
for row in broken_out_list_dict:
    table.add_row(row.values())

# Print the table
print(table)

end = time.time()

print(f"total time = {end-start}")






# Set the start and end times for the trading session
# start_time = datetime.time(12, 45)
# end_time = datetime.time(15, 30)

# while datetime.datetime.now().time() < end_time:
#     current_time = datetime.datetime.now().time()
#     # Check if the current time is within the trading session
#     if current_time >= start_time:
#         print(current_time)
#         period = 100
#         check(symbols, "15", period)
#         time.sleep(900)
#     else:
#         time_remaining = (datetime.datetime.now().replace(hour=start_time.hour, minute=start_time.minute, second=start_time.second) - datetime.datetime.now()).total_seconds()
#         print(f"Wait for {time_remaining} seconds")
#         time.sleep(time_remaining)
