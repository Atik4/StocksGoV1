from mainV3 import fyers
import datetime
import time
from utils import get_historical_data_v1, get_candles_data, get_previous_resistance_anchored_vwap
from watchlist_dao import get_watchlist, update_watchlist
from calendar_utils import get_today_in_yyyy_mm_dd

RESISTANCE_LEVEL = "resistance_level"
RESISTANCE_ZONE = "resistance_zone"
SUPPORT_LEVEL = "support_level"
AVWAP_RESISTANCE = "avwap_resistance"
AVWAP_SUPPORT = "avwap_support"
CLOSING_PRICE = "closing_price"
TIMEFRAME = "timeframe"
STRATEGIES = "strategies"
SYMBOL = "symbol"


def check_for_breakout(symbol, df, prev_closing_price, closing_price, timeframe, period, stock):
    try:
        info = get_previous_resistance_anchored_vwap(df)
        avwap = info["avwap"]
        anchor_date = info["anchor_date"]
        total_period = info["total_period"]
        print(f"anchor date: {anchor_date} and total period: {total_period}")
        stock[AVWAP_RESISTANCE]["value"] = avwap
        stock[AVWAP_RESISTANCE]["anchor_date"] = anchor_date
        stock[AVWAP_RESISTANCE]["anchor_period"] = total_period

        print(f"closing price: {closing_price} and avwap: {avwap}")
        if closing_price > avwap > prev_closing_price:
            print(f"{symbol} has broken out from AVWAP at {avwap}")

            return True
        return False
    except Exception as e:
        print(e)


def check_for_avwap_breakout(symbol, avwap_resistance, stock):
    try:
        period = avwap_resistance["period"]
        if TIMEFRAME in avwap_resistance:
            timeframe = avwap_resistance[TIMEFRAME]
        else:
            timeframe = "D"
        df = get_candles_data(fyers, symbol, timeframe, period)
        if df.empty:
            return False
        closing_prices = df[4]
        last_index = len(closing_prices) - 1

        return check_for_breakout(symbol, df, closing_prices[last_index - 1], closing_prices[last_index], timeframe,
                           period, stock)
    except Exception as e:
        print(e)


def create_avwap_message(message, avwap_details, symbol):
    avwap_timeframe = avwap_details["timeframe"]
    avwap_period = avwap_details["period"]
    avwap_value = avwap_details["value"]

    if avwap_timeframe == "D":
        avwap_string = f"{avwap_period} day Avwap"
    else:
        avwap_string = f"{avwap_period} {avwap_timeframe} min Avwap"

    if message == "":
        message = f"{symbol} has broken out of {avwap_string} resistance {avwap_value}"
    else:
        message = f"{message} and {avwap_string} resistance {avwap_value}"

    return message

def check_for_conditions(stock, timeframe):
    try:
        symbol = f"NSE:{stock['symbol']}-EQ"
        print(stock[SYMBOL])
        df = get_historical_data_v1(fyers, stock["symbol"], timeframe, get_today_in_yyyy_mm_dd(), get_today_in_yyyy_mm_dd())
        if df.empty:
            return False
        # df[0] = convert_column_from_epoch_to_date(df[0])
        print(df)
        latest_closing_price = df.iloc[-1, 4]

        stock[CLOSING_PRICE] = latest_closing_price
        message = ""
        # print(stock[STRATEGIES])
        for strategy in stock[STRATEGIES]:
            if RESISTANCE_LEVEL in strategy:
                print("resistance level: ")
                print(strategy[RESISTANCE_LEVEL])
                if latest_closing_price > strategy[RESISTANCE_LEVEL]:
                    print(f"{stock['symbol']} has broken out of resistance level {strategy[RESISTANCE_LEVEL]}")
                    message = f"{stock['symbol']} has broken out of resistance level {strategy[RESISTANCE_LEVEL]}"
            elif RESISTANCE_ZONE in strategy:
                print("resistance zone: ")
                print(strategy[RESISTANCE_ZONE])
                if latest_closing_price > strategy[RESISTANCE_ZONE][1]:
                    # notify the user
                    print(f"{stock['symbol']} has broken out of resistance zone {strategy[RESISTANCE_ZONE]}")
                    message = f"{stock['symbol']} has broken out of resistance zone {strategy[RESISTANCE_ZONE]}"

                elif latest_closing_price > strategy[RESISTANCE_ZONE][0]:
                    # notify the user
                    print(f"{stock['symbol']} is within the resistance zone {strategy[RESISTANCE_ZONE]}")
                    message = f"{stock['symbol']} is within the resistance zone {strategy[RESISTANCE_ZONE]}"
                    stock[CLOSING_PRICE] = latest_closing_price
            if AVWAP_RESISTANCE in strategy:
                print("avwap resistance")
                print(strategy[AVWAP_RESISTANCE])
                if check_for_avwap_breakout(symbol, strategy[AVWAP_RESISTANCE], stock):
                    message = create_avwap_message(message, strategy[AVWAP_RESISTANCE], stock["symbol"])
                    # notify the user
                    print(f"{stock['symbol']} has broken out of avwap resistance {strategy[AVWAP_RESISTANCE]['value']}")

        # if RESISTANCE_LEVEL in stock:
        #     if latest_closing_price > stock[RESISTANCE_LEVEL]:
        #         print(f"{stock['symbol']} has broken out of resistance level {stock[RESISTANCE_LEVEL]}")
        #         message = f"{stock['symbol']} has broken out of resistance level {stock[RESISTANCE_LEVEL]}"
        #
        # elif RESISTANCE_ZONE in stock:
        #     if latest_closing_price > stock[RESISTANCE_ZONE][1]:
        #         # notify the user
        #         print(f"{stock['symbol']} has broken out of resistance zone {stock[RESISTANCE_ZONE]}")
        #         message = f"{stock['symbol']} has broken out of resistance zone {stock[RESISTANCE_ZONE]}"
        #
        #
        #     elif latest_closing_price > stock[RESISTANCE_ZONE][0]:
        #         # notify the user
        #         print(f"{stock['symbol']} is within the resistance zone {stock[RESISTANCE_ZONE]}")
        #         message = f"{stock['symbol']} is within the resistance zone {stock[RESISTANCE_ZONE]}"
        #         stock[CLOSING_PRICE] = latest_closing_price
        #
        # if AVWAP_RESISTANCE in stock:
        #     if check_for_avwap_breakout(symbol, stock[AVWAP_RESISTANCE], stock):
        #         message = create_avwap_message(message, stock[AVWAP_RESISTANCE], stock["symbol"])
        #         # notify the user
        #         print(f"{stock['symbol']} has broken out of avwap resistance {stock[AVWAP_RESISTANCE]['value']}")
        #
        # print("message for user: " + message)
    except Exception as e:
        print(e)


def check(logged_in_users, timeframe):
    try:
        for user in logged_in_users:
            stocks_list = get_watchlist(user)["stocks"]
            # for every stock in the list, loop through the list and check if the conditions are met
            for stock in stocks_list:
                check_for_conditions(stock, timeframe)
                # print(stock)

            update_watchlist(user, stocks_list)
    except Exception as e:
        print(e)


logged_in_users = ["atik"]
check(logged_in_users, "30")
# Set the start and end times for the trading session
# start_time = datetime.time(9, 15)
# end_time = datetime.time(15, 30)
#
# while datetime.datetime.now().time() < end_time:
#     current_time = datetime.datetime.now().time()
#     if current_time >= start_time:
#         print(current_time)
#         check(logged_in_users, "30")
#         time.sleep(1800)
#     else:
#         time_remaining = (datetime.datetime.now().replace(hour=start_time.hour, minute=start_time.minute, second=start_time.second) - datetime.datetime.now()).total_seconds()
#         print(f"Wait for {time_remaining} seconds")
#         time.sleep(time_remaining)
#
