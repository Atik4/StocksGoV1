import datetime
import time
from main import fyers
from utils import generate_order_request, get_historical_data, convert_column_from_epoch_to_date, \
    generate_nearest_thursday_option_symbol
from position import Position
from constants import symbols, breakdown_levels, breakout_levels, names, stoploss, target

positions = {}


# Function to manage a position for a specific strategy
def manage_position(strategy, position):
    # Store the position in the positions dictionary
    if strategy in positions:
        positions[strategy].append(position)
    else:
        positions[strategy] = [position]

    # ... Perform any necessary position management tasks ...

    # Check if the exit conditions for the strategy are met
    if exit_conditions_met(strategy):
        # Trigger an exit order for the strategy
        trigger_exit_order(strategy)


# Function to check if the exit conditions for a strategy are met
def exit_conditions_met(position, closing_price):
    # ... Define the exit conditions for the strategy ...
    # ... Return True if the conditions are met, False otherwise ...
    # if stoploss is hit
    # if target is achieved
    # time stoploss
    if abs(closing_price - position.get_entry_price()) >= position.get_sl_underlying():
        print("stop loss hit: exit condition met")
        return True
    if abs(closing_price - position.get_entry_price()) >= position.get_target():
        print("target achieved: exit condition met")
        return True
    return False


# Function to trigger an exit order for a strategy
def trigger_exit_order(position):
    # ... Place the exit order for the strategy ...
    # ... Remove the position from the positions dictionary ...
    # id = generate_nearest_thursday_option_symbol(index)
    id = position.get_symbol()
    data = {
        "id": id
    }
    response = fyers.exit_positions(data=data)
    print(response)
    if response["code"] == 200:
        positions.pop(position.get_symbol())


def buy_on_breakout(index, breakdown_level, breakout_level, timeframe, symbol, stoploss, target):
    put_strike_price = breakdown_level
    call_strike_price = breakout_level

    # Get today's date
    today = datetime.date.today()
    range_from = today.strftime("%Y-%m-%d")
    range_to = today.strftime("%Y-%m-%d")

    df = get_historical_data(fyers, symbol, timeframe, range_from, range_to)

    df[0] = convert_column_from_epoch_to_date(df[0])
    print(df)

    closing_prices = df[4]

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
                if exit_conditions_met(positions[symbol], closing_prices[last_index]):
                    # Trigger an exit order for the strategy
                    trigger_exit_order(positions[symbol])
                    is_position = 0

            # Check if the closing price is below the breakdown level
            # Buy a put option
            if closing_prices[last_index] < breakdown_level:
                print("placing order for put option")
                order_response = fyers.place_order(data=generate_order_request(index, put_strike_price, "PE"))
                # manage_position(strategy_type, order)
                print(order_response)
                position = Position(entry_price=closing_prices[last_index], ltp=None, strike_price=call_strike_price,
                                    symbol=symbol, quantity=None, sl=None, sl_underlying=stoploss, target=target)
                positions[symbol] = position

            # Check if the closing price is above the breakout level
            # Buy a call option
            elif closing_prices[last_index] >= breakout_level:
                print("placing order for call option")
                order_response = fyers.place_order(data=generate_order_request(index, call_strike_price, "CE"))
                position = Position(entry_price=closing_prices[last_index], ltp=None, strike_price=call_strike_price,
                                    symbol=symbol, quantity=None, sl=None, sl_underlying=stoploss, target=target)
                positions[symbol] = position
                # manage_position(strategy_type, order)
                print(order_response)
            else:
                print("Order not placed now since price is: " + str(closing_prices[last_index]))

        # Wait for 15 minutes before checking again
        time.sleep(900)


timeframe = "15"

for symbol in symbols:
    buy_on_breakout(names[symbol], breakdown_levels[symbol], breakout_levels[symbol], timeframe, symbol, stoploss[symbol], target[symbol])
