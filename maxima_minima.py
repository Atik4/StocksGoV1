import time
import datetime
from utils import get_historical_data, convert_column_from_epoch_to_date, send_sms
from fyers_api import fyersModel
from main import login, app_id, fyers

fyers = fyersModel.FyersModel(is_async=False, client_id=app_id, token=login(),
                              log_path="/Users/atik.agarwal/Projects/personal/trading/logs/")


def get_candles_data(symbol, timeframe):
    today = datetime.date.today()
    range_from = today.strftime("%Y-%m-%d")
    range_to = today.strftime("%Y-%m-%d")
    print(range_from)
    df = get_historical_data(fyers, symbol, timeframe, range_from, range_to)
    df[0] = convert_column_from_epoch_to_date(df[0])

    print(df)
    return df


def check(symbols, timeframe):
    try:
        for symbol in symbols:
            df = get_candles_data(symbol, timeframe)
            closing_prices = df[4]
            last_index = len(closing_prices) - 1
            local_maxima = 0
            local_minima = 0

            if last_index == 0:
                local_maxima = df[2][last_index]
                local_minima = df[3][last_index]
                continue

            if last_index == 1:
                if df[2] > local_maxima:
                    local_maxima = df[2][last_index]

                if df[3] < local_minima:
                    local_minima = df[3][last_index]
                continue

            prev = last_index - 2
            mid = last_index -1
            curr = last_index

            if df[2][prev] < df[2][mid] > df[2][curr]:
                print("A high has been formed")
                if df[2][mid] > local_maxima:
                    str = f"A higher high has been formed at {df[2][mid]}"
                    print(str)
                    send_sms(str)
                    local_maxima = df[2][mid]
                else:
                    str = f"A lower high has been formed at {df[2][mid]}"
                    print(str)
                    send_sms(str)

            if df[2][prev] > df[2][mid] < df[2][curr]:
                print("A low has been formed")
                if df[2][mid] < local_minima:
                    str = f"A lower low has been formed at {df[2][mid]}"
                    print(str)
                    send_sms(str)
                    local_minima = df[2][mid]
                else:
                    str = f"A higher low has been formed at {df[2][mid]}"
                    print(str)
                    send_sms(str)


    return

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
