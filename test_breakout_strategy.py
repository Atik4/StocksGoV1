import time
import datetime
from fyers_api import fyersModel
from main import login, app_id, fyers
from constants import symbols, breakdown_levels, breakout_levels, names, LONG, SHORT, stoploss, target
from utils import generate_order_request, get_historical_data, convert_column_from_epoch_to_date, \
    generate_nearest_thursday_option_symbol, trigger_exit_order, find_nearest_strike_price, create_position, get_existing_position


fyers = fyersModel.FyersModel(is_async=False, client_id=app_id, token=login(),
                              log_path="/Users/atik.agarwal/Projects/personal/trading/logs/")

positions = {}
is_position = {}
strategy = "breakout"

# Function to check if the exit conditions for a strategy are met
def exit_conditions_met(position, closing_price):
    if position.get_direction() == LONG and position.get_entry_price() - closing_price >= position.get_sl_underlying():
        print("stop loss hit: exit condition met")
        return True

    if position.get_direction() == LONG and closing_price - position.get_entry_price() >= position.get_target():
        print("target achieved: exit condition met")
        return True

    if position.get_direction() == SHORT and closing_price - position.get_entry_price() >= position.get_sl_underlying():
        print("stop loss hit: exit condition met")
        return True

    if position.get_direction() == SHORT and position.get_entry_price() - closing_price >= position.get_target():
        print("target achieved: exit condition met")
        return True

    return False


def get_candles_data(symbol, timeframe):
    today = datetime.date.today()
    range_from = today.strftime("%Y-%m-%d")
    range_to = today.strftime("%Y-%m-%d")
    print(range_from)
    df = get_historical_data(fyers, symbol, timeframe, range_from, range_to)
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


def check_for_breakout(symbol, closing_price, breakout_level, breakdown_level):
    if closing_price > breakout_level:
        print(f"Buy CE order placed at {closing_price}")
        positions[symbol] = create_position(fyers, closing_price, symbol, "CE", strategy)
        return True
    elif closing_price < breakdown_level:
        print(f"Buy PE order placed at {closing_price}")
        positions[symbol] = create_position(fyers, closing_price, symbol, "PE", strategy)
        return True
    else:
        return False


def check(symbols, timeframe):
    try:
        for symbol in symbols:
            df = get_candles_data(symbol, timeframe)
            closing_prices = df[4]
            last_index = len(closing_prices) - 1

            position = get_existing_position(names[symbol], strategy)

            if position is not None:
                if exit_conditions_met(position, closing_prices[last_index]):
                    trigger_exit_order(position, positions, fyers)
                continue
            if check_for_breakout(symbol, closing_prices[last_index], breakout_levels[symbol], breakdown_levels[symbol]):
                continue
            else:
                print("Order not placed now since price is: " + str(closing_prices[last_index]))
    except Exception as e:
        print(e)

# Set the start and end times for the trading session
start_time = datetime.time(14, 30)
end_time = datetime.time(15, 30)

while datetime.datetime.now().time() < end_time:
    current_time = datetime.datetime.now().time()
    if current_time >= start_time:
        print(current_time)
        check(symbols, "15")
        time.sleep(900)
    else:
        time_remaining = (datetime.datetime.now().replace(hour=start_time.hour, minute=start_time.minute, second=start_time.second) - datetime.datetime.now()).total_seconds()
        print(f"Wait for {time_remaining} seconds")
        time.sleep(time_remaining)
