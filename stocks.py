from utils import get_historical_data, convert_column_from_epoch_to_date, get_weekly_historical_data
from fyers_api import fyersModel
import datetime
import time
from main import login, app_id
from constants import stock_symbols, stock_breakout_levels, stock_breakdown_levels
from utils import send_sms, generate_order_request_for_stock, create_position, get_anchored_vwap

fyers = fyersModel.FyersModel(is_async=False, client_id=app_id, token=login(),
                              log_path="/Users/atik.agarwal/Projects/personal/trading/logs/")

today = datetime.date.today()
range_from = (today - datetime.timedelta(days=0)).strftime("%Y-%m-%d")
range_to = today.strftime("%Y-%m-%d")


# get_anchored_vwap(fyers, "NSE:HAL-EQ", "15", 80)
# df = get_historical_data(fyers, f"NSE:HAL-EQ", "W", "", "")

# df = get_weekly_historical_data(fyers, f"NSE:HAL-EQ", "2023-09-09", 14)
#
# print(df)

breakout_list = []
breakdown_list = []

# Set the start and end times for the trading session
start_time = datetime.time(13, 45)
end_time = datetime.time(15, 30)

while datetime.datetime.now().time() < end_time:
    current_time = datetime.datetime.now().time()
    # Check if the current time is within the trading session
    if current_time >= start_time:
        print(current_time)
        message = ""
        for stock_symbol in stock_symbols:
            # print(f"Data for {stock_symbol}")
            data = get_historical_data(fyers, f"NSE:{stock_symbol}-EQ", "60", range_from, range_to)
            closing_prices = data[4]
            last_index = len(closing_prices) - 1

            if stock_symbol in stock_breakout_levels:
                if closing_prices[last_index] >= stock_breakout_levels[stock_symbol]:
                    if stock_symbol not in breakout_list:
                        message += f"Breakout: \n{stock_symbol} > {stock_breakout_levels[stock_symbol]}"
                        breakout_list.append(stock_symbol)

            if stock_symbol in stock_breakdown_levels:
                if closing_prices[last_index] <= stock_breakdown_levels[stock_symbol]:
                    if stock_symbol not in breakdown_list:
                        message += f"Breakdown: \n{stock_symbol} < {stock_breakdown_levels[stock_symbol]}"
                        breakdown_list.append(stock_symbol)

        if message != "":
            send_sms(message)

        time.sleep(900)
    else:
        time_remaining = (datetime.datetime.now().replace(hour=start_time.hour, minute=start_time.minute, second=start_time.second) - datetime.datetime.now()).total_seconds()
        print(f"Wait for {time_remaining} seconds")
        time.sleep(time_remaining)



# generate_order_request_for_stock(fyers, "HAL", 4000, "CE")
# create_position(fyers, 3990, "HAL", "CE")