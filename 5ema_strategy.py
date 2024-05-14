import time
import datetime
from fyers_api import fyersModel

from dao.position_dao import PositionDAO
from main import login, app_id, fyers
import pandas_ta as pta
from calendar_utils import find_nth_last_working_day
from position import Position
from constants import symbols, names, lot_size
from utils import get_historical_data, convert_column_from_epoch_to_date, \
    generate_nearest_thursday_option_symbol, send_sms, get_preference_for_strike, \
    get_buy_price_for_option, trigger_exit_order

fyers = fyersModel.FyersModel(is_async=False, client_id=app_id, token=login(),
                              log_path="/Users/atik.agarwal/Projects/personal/trading/logs/")

start_time = datetime.time(9, 20)
end_time = datetime.time(15, 30)
positions = {}
is_position = {}
stoploss = 50
target = 100


def get_candles_data(symbol, timeframe):
    today = datetime.date.today()
    range_from = find_nth_last_working_day(2)
    range_to = today.strftime("%Y-%m-%d")

    df = get_historical_data(fyers, symbol, timeframe, range_from, range_to)
    df[0] = convert_column_from_epoch_to_date(df[0])
    df['5ema'] = pta.ema(df[4], 5)

    print(df)
    return df


def find_nearest_strike_price(current_value, preference=None):
    strike_interval = 100  # Interval between strike prices
    nearest_strike_price = get_preference_for_strike(current_value, strike_interval, preference) * strike_interval
    return nearest_strike_price


def test_generate_order_request(symbol, option_symbol):
    order_request = {
        "symbol": option_symbol,
        "qty": lot_size[symbol],
        "type": 2,
        "side": 1,
        "productType": "INTRADAY",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": "False",
    }
    return order_request


def create_position(fyers, symbol, option_symbol, closing_price, strike_price):
    order_request = test_generate_order_request(symbol, option_symbol)
    order_response = fyers.place_order(data=order_request)
    print(order_response)
    send_sms(f"Buy Order has been placed for {symbol} for option: {option_symbol}")

    id = option_symbol + "-INTRADAY"
    position = Position(entry_price=closing_price, ltp=None, strike_price=strike_price,
                    symbol=id, quantity=None, sl=None, sl_underlying=stoploss, target=target,
                    direction="up", buy_price=get_buy_price_for_option(fyers, symbol, strike_price), sell_price=None, strategy="5EMA", state="open")

    with PositionDAO() as position_dao:
        position_dao.insert_position(position)
    return position


def manage_order(fyers, symbol, closing_price, direction, option_preference=None):
    strike_price = find_nearest_strike_price(closing_price, option_preference)
    option_symbol = "NSE:" + generate_nearest_thursday_option_symbol(names[symbol], strike_price, direction)
    print(option_symbol)
    return create_position(fyers, symbol, option_symbol, closing_price, strike_price)


# Function to check if the exit conditions for a strategy are met
def exit_conditions_met(position, closing_price):
    if position.get_entry_price() - closing_price >= target:
        print("target achieved: exit condition met")
        return True

    if closing_price - position.get_entry_price() >= stoploss:
        print("stop loss hit: exit condition met")
        return True

    return False


def get_existing_position(symbol, strategy):
    with PositionDAO() as position_dao:
        position = position_dao.get_position(symbol, strategy, "open")

    if position:
        print("Position Found:")
        print(f"Symbol: {position.symbol}, Strategy: {position.strategy}")
        return position
    else:
        print("No matching position found.")
        return None


def check(symbols, timeframe):
    try:
        for symbol in symbols:
            df = get_candles_data(symbol, timeframe)
            closing_prices = df[4]
            last_index = len(closing_prices) - 1
            prev_candle_low = df.loc[last_index - 1, 3]
            prev_candle_high = df.loc[last_index - 1, 2]
            curr_candle_low = df.loc[last_index, 3]

            position = get_existing_position(symbol, "5EMA")
            if position is not None:
                if exit_conditions_met(position, closing_prices[last_index]):
                    trigger_exit_order(position, positions, fyers)
                continue

            elif df.loc[last_index - 1, '5ema'] < prev_candle_low > curr_candle_low:
                global stoploss
                stoploss = prev_candle_high - prev_candle_low
                global target
                target = 2 * stoploss
                if stoploss <= 10.0:
                    target = 3 * stoploss
                # buy PE
                print(f"Buy PE order placed at {df.loc[last_index, 4]}")
                positions[symbol] = manage_order(fyers, symbol, closing_prices[last_index], "PE", "OTM")

            else:
                print("Order not placed now since price is: " + str(closing_prices[last_index]))
    except Exception as e:
        print(e)

# check(symbols, "5")

while datetime.datetime.now().time() < end_time:
    current_time = datetime.datetime.now().time()
    # Check if the current time is within the trading session
    if current_time >= start_time:
        check(symbols, "5")
        print(current_time)
        time.sleep(15)
    else:
        time_remaining = (datetime.datetime.now().replace(hour=start_time.hour, minute=start_time.minute, second=start_time.second) - datetime.datetime.now()).total_seconds()
        print(f"Wait for {time_remaining} seconds")
        time.sleep(time_remaining)
