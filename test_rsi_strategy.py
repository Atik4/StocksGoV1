import time
import datetime
from fyers_api import fyersModel
from main import login, app_id, fyers
import pandas_ta as pta
from position import Position
from constants import symbols, breakdown_levels, breakout_levels, names, stoploss, target, LONG, SHORT
from utils import generate_order_request, get_historical_data, convert_column_from_epoch_to_date, \
    generate_nearest_thursday_option_symbol, trigger_exit_order, find_nearest_strike_price, create_position, get_existing_position

fyers = fyersModel.FyersModel(is_async=False, client_id=app_id, token=login(),
                              log_path="/Users/atik.agarwal/Projects/personal/trading/logs/")

positions = {}
is_position = {}


# def create_position(closing_price, symbol, option):
#     strike_price = find_nearest_strike_price(closing_price)
#     order_response = fyers.place_order(data=generate_order_request(symbol, strike_price, option))
#
#     print(order_response)
#     id = generate_nearest_thursday_option_symbol(names[symbol], strike_price, option) + "-INTRADAY"
#     return Position(entry_price=closing_price, ltp=None, strike_price=strike_price,
#                     symbol=id, quantity=None, sl=None, sl_underlying=stoploss, target=target, direction="up")


# Function to check if the exit conditions for a strategy are met
def exit_conditions_met(position, closing_price, latest_rsi):
    if position.get_direction() == LONG and latest_rsi < 60:
        print("RSI has closed below 60, exiting")
        return True

    if position.get_direction() == SHORT and latest_rsi > 40:
        print("RSI has closed above 40, exiting")
        return True

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


def get_candles_data(symbol, timeframe):
    today = datetime.date.today()
    range_from = today.strftime("%Y-%m-%d")
    range_to = today.strftime("%Y-%m-%d")

    df = get_historical_data(fyers, symbol, timeframe, range_from, range_to)
    df[0] = convert_column_from_epoch_to_date(df[0])

    df['rsi'] = pta.rsi(df[4], length=14)
    # pta.ema()
    print(df)
    return df


def check(symbols, timeframe):
    for symbol in symbols:
        df = get_candles_data(symbol, timeframe)
        closing_prices = df[4]
        last_index = len(closing_prices) - 1

        # if position exists for that symbol
        position = get_existing_position(symbol, "5EMA")
        if position is not None:
            # check if exit condition is met and then exit
            if exit_conditions_met(position, closing_prices[last_index], df.loc[last_index, 'rsi']):
                # Trigger an exit order for the strategy
                trigger_exit_order(positions[symbol], positions, fyers)
                # is_position = 0
                print(len(positions))
                return

        # elif condition satisfied:
        elif df.loc[last_index - 1, 'rsi'] < 60 < df.loc[last_index, 'rsi']:
            # buy CE
            print(f"Buy CE order placed at {df.loc[last_index, 4]}")
            positions[symbol] = create_position(fyers, closing_prices[last_index], symbol, "CE")
        elif df.loc[last_index - 1, 'rsi'] > 40 > df.loc[last_index, 'rsi']:
            # buy PE
            print(f"Buy PE order placed at {df.loc[last_index, 4]}")
            positions[symbol] = create_position(fyers, closing_prices[last_index], symbol, "PE")
        else:
            print("Order not placed now since price is: " + str(closing_prices[last_index]))


# Set the start and end times for the trading session
start_time = datetime.time(9, 15)
end_time = datetime.time(15, 30)

while datetime.datetime.now().time() < end_time:
    current_time = datetime.datetime.now().time()
    # Check if the current time is within the trading session
    if current_time >= start_time:
        check(symbols, "60")
        print(current_time)
        time.sleep(360)
