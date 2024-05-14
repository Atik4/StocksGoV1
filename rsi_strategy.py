from fyers_api import fyersModel
from main import login, app_id, fyers
import pandas as pd
import time
import datetime
import pandas_ta as pta
from position import Position
from constants import symbols, breakdown_levels, breakout_levels, names, stoploss, target
from utils import generate_order_request, get_historical_data, convert_column_from_epoch_to_date, \
    generate_nearest_thursday_option_symbol, trigger_exit_order, find_nearest_strike_price

fyers = fyersModel.FyersModel(is_async=False, client_id=app_id, token=login(),
                              log_path="/Users/atik.agarwal/Projects/personal/trading/logs/")

positions = {}


# Function to check if the exit conditions for a strategy are met
def exit_conditions_met(position, closing_price, direction, latest_rsi):
    # ... Define the exit conditions for the strategy ...
    # ... Return True if the conditions are met, False otherwise ...
    # if stoploss is hit
    # if target is achieved
    # time stoploss
    # rsi has crossed under
    return True

    if direction == "up" and latest_rsi < 60:
        print("RSI has closed below 60, exiting")
        return True

    if direction == "down" and latest_rsi > 40:
        print("RSI has closed above 40, exiting")
        return True

    if abs(closing_price - position.get_entry_price()) >= position.get_sl_underlying():
        print("stop loss hit: exit condition met")
        return True

    if latest_rsi >= 80:
        print("target achieved: exiting")
        return True

    if abs(closing_price - position.get_entry_price()) >= position.get_target():
        print("target achieved: exit condition met")
        return True
    return False


def get_start_date(timeframe, today):
    d = 0
    if timeframe == "D":
        d = 30
    elif timeframe == "60":
        d = 5
    elif timeframe == "15":
        d = 3
    reference_day = today - datetime.timedelta(days=d)
    return reference_day.strftime("%Y-%m-%d")


def buy_on_breakout(index, timeframe, symbol, stoploss, target):
    today = datetime.date.today()
    range_from = get_start_date(timeframe, today)
    range_to = today.strftime("%Y-%m-%d")

    df = get_historical_data(fyers, symbol, timeframe, range_from, range_to)

    df[0] = convert_column_from_epoch_to_date(df[0])
    print(df)

    closing_prices = df[4]
    df['rsi'] = pta.rsi(closing_prices, length=14)

    print(df)

    # Get the index of the last row in the DataFrame
    last_index = df.index[-1]

    # Set the start and end times for the trading session
    start_time = datetime.time(9, 15)
    end_time = datetime.time(15, 30)

    is_position = 0

    # Loop until the current time is after the end time
    while datetime.datetime.now().time() < end_time:
        # Get the current time
        current_time = datetime.datetime.now().time()

        # Check if the current time is within the trading session
        if current_time >= start_time:
            # Get the index of the last closing price in the dataframe
            last_index = len(closing_prices) - 1

            if is_position == 1:
                if exit_conditions_met(positions[symbol], closing_prices[last_index], "down", df.loc[last_index, 'rsi']):
                    # Trigger an exit order for the strategy
                    trigger_exit_order(positions[symbol], positions, fyers)
                    is_position = 0
                    print(len(positions))
                    return

            print("Current rsi: ", df.loc[last_index, 'rsi'])
            # Check if RSI has crossed above 60
            # Check if the previous RSI was below 60 and the current RSI crosses above 60
            if df.loc[last_index - 1, 'rsi'] < 60 < df.loc[last_index, 'rsi']:
                # Place a buy order
                # Add your code here to place the buy order using your preferred trading platform or API
                print(f"Buy order placed at {df.loc[last_index, 4]}")
                strike_price = find_nearest_strike_price(closing_prices[last_index])
                # order_response = fyers.place_order(data=generate_order_request(index, strike_price, "CE"))
                # manage_position(strategy_type, order)
                # print(order_response)
                id = generate_nearest_thursday_option_symbol(index, strike_price, "CE") + "-INTRADAY"
                position = Position(entry_price=closing_prices[last_index], ltp=None, strike_price=strike_price,
                                    symbol=id, quantity=None, sl=None, sl_underlying=stoploss, target=target)
                print(position)
                positions[symbol] = position

            # Check if the closing price is above the breakout level
            # Buy a put option
            # elif df.loc[last_index - 1, 'rsi'] > 40 > df.loc[last_index, 'rsi']:
            elif True:
                print(f"Sell order placed at {df.loc[last_index, 4]}")
                strike_price = find_nearest_strike_price(closing_prices[last_index])
                order_response = fyers.place_order(data=generate_order_request(index, strike_price, "PE"))
                print(order_response)

                id = generate_nearest_thursday_option_symbol(index, strike_price, "PE") + "-INTRADAY"
                position = Position(entry_price=closing_prices[last_index], ltp=None, strike_price=strike_price,
                                    symbol=id, quantity=None, sl=None, sl_underlying=stoploss, target=target)
                print(position)
                positions[symbol] = position
                is_position = 1
                # manage_position(strategy_type, order)
                # print(order_response)
            # else:
            #     print("Order not placed now since price is: " + str(closing_prices[last_index]))

        # Wait for 15 minutes before checking again
        time.sleep(15)


timeframe = "15"

# for symbol in symbols:
#     buy_on_breakout(names[symbol], timeframe, symbol, stoploss[symbol], target[symbol])



# def place_order():
#     order_request = {
#         "symbol": "NSE:NIFTY23JUN18700CE",
#         "qty": 1,
#         "type": 2,
#         "side": 1,
#         "productType": "CNC",
#         "limitPrice": 0,
#         "stopPrice": 0,
#         "validity": "DAY",
#         "disclosedQty": 0,
#         "offlineOrder": "False",
#     }
#
#     order_response = fyers.place_order(data=order_request)
#     print(order_response)
#
#
# data = {
#     "symbol": "NSE:NIFTY50-INDEX",
#     "resolution": "60",
#     "date_format": "1",
#     "range_from": "2023-05-19",
#     "range_to": "2023-06-23",
#     "cont_flag": "1"
# }
#
# response = fyers.history(data=data)
# # print(response)
# df = pd.DataFrame(response["candles"])
# converted_times = []
# for epoch_time in df[0]:
#     timestamp = datetime.datetime.fromtimestamp(epoch_time).strftime('%d-%m-%Y %H:%M:%S')
#     converted_times.append(timestamp)
#
# df[0] = converted_times
# # print(df)
# closing_prices = df[4]
# # print(closing_prices)
#
# df['rsi'] = pta.rsi(closing_prices, length=14)
# print(df)
#
# # Get the index of the last row in the DataFrame
# last_index = df.index[-1]
#
# # Check if the previous RSI was below 60 and the current RSI crosses above 60
# if df.loc[last_index - 1, 'rsi'] < 60 < df.loc[last_index, 'rsi']:
#     # Place a buy order
#     # Add your code here to place the buy order using your preferred trading platform or API
#
#     print(f"Buy order placed at {df.loc[last_index, 4]}")
# else:
#     print("No buy order")
#
# # Check if the previous RSI was below 60 and the current RSI crosses above 60
# if df.loc[last_index - 1, 'rsi'] > 40 > df.loc[last_index, 'rsi']:
#     # Place a sell order
#     # Add your code here to place the buy order using your preferred trading platform or API
#
#     print(f"Sell order placed at {df.loc[last_index, 4]}")
# else:
#     print("No sell order")
#
#
# # find nearest strike price
# # generate symbol for that strike price
# # get ltp of that strike price
# # place order
#
