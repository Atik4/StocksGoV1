import datetime
from datetime import datetime, timedelta
import pandas as pd

from dao.position_dao import PositionDAO
from position import Position
from constant_values import names, lot_size, stoploss, target, LONG, SHORT
from twilio.rest import Client
from calendar_utils import get_all_thursdays_of_current_month, months, get_anchor_date, get_start_of_week
from stock_utils import all_stocks_list
import time


def get_preference_for_strike(current_value, strike_interval, preference="ATM"):
    if preference == "ATM":
        return round(current_value / strike_interval)
    elif preference == "ITM":
        return int(current_value / strike_interval)
    elif preference == "OTM":
        return int(current_value / strike_interval) + 1

def find_nearest_strike_price(current_value):
    strike_interval = 100  # Interval between strike prices
    nearest_strike_price = round(current_value / strike_interval) * strike_interval
    return nearest_strike_price


def generate_order_request(symbol, strike_price, direction):
    print(generate_nearest_thursday_option_symbol(names[symbol], strike_price, direction))
    order_request = {
        "symbol": "NSE:" + generate_nearest_thursday_option_symbol(names[symbol], strike_price, direction),
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


def generate_order_request_for_stock(fyers, symbol, strike_price, direction):
    option = "NSE:" + get_monthly_expiry_symbol(symbol, strike_price, direction)
    data = {
        "symbol": option,
        "ohlcv_flag": "1"
    }
    response = fyers.depth(data=data)
    ltp = response['d'][option]['ltp']

    order_request = {
        "symbol": option,
        "qty": lot_size[symbol],
        "type": 1,
        "side": 1,
        "productType": "MARGIN",
        "limitPrice": 1.05 * ltp,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": "False",
    }
    print(order_request)
    return order_request


def create_position_for_stock(fyers, closing_price, symbol, option):
    strike_price = find_nearest_strike_price(closing_price)
    order_response = fyers.place_order(data=generate_order_request_for_stock(fyers, symbol, strike_price, option))

    print(order_response)


def get_direction(option):
    if option == "CE":
        return LONG
    else:
        return SHORT


def create_position(fyers, closing_price, symbol, option, strategy):
    strike_price = find_nearest_strike_price(closing_price)
    order_response = fyers.place_order(data=generate_order_request(symbol, strike_price, option))

    print(order_response)
    send_sms(f"Buy Order has been placed for {symbol} for option: {strike_price}{option}")
    id = generate_nearest_thursday_option_symbol(names[symbol], strike_price, option) + "-INTRADAY"

    position = Position(entry_price=closing_price, ltp=None, strike_price=strike_price,
                    symbol=id, quantity=None, sl=None, sl_underlying=stoploss[symbol], target=target[symbol],
                    direction=get_direction(option), buy_price=get_buy_price_for_option(fyers, symbol, strike_price), sell_price=None, state="open", strategy=strategy)

    with PositionDAO() as position_dao:
        position_dao.insert_position(position)

    return position


def get_buy_price_for_option(fyers, symbol, strike_price):
    current_positions = fyers.positions()["netPositions"]
    for position in current_positions:
        if names[symbol] in position["symbol"] and str(strike_price) in position["symbol"]:
            return position["buyAvg"]


# def generate_nearest_thursday_option_symbol(strike_price, direction):
#     today = datetime.date.today()
#     current_day = today.day
#     current_month = today.strftime("%b").upper()
#     current_year = today.strftime("%y")
#
#     # Calculate the last Thursday of the current month
#     last_day_of_month = today.replace(day=28) + datetime.timedelta(days=4)
#     last_thursday = last_day_of_month - datetime.timedelta(days=last_day_of_month.weekday() + 1)
#
# if current_day >= last_thursday.day: # Monthly expiry expiry_date = last_thursday.strftime("%b").upper()
# option_symbol = f"NIFTY{current_year}{expiry_date}{strike_price}{direction}" else: # Weekly expiry
# weekly_expiry_date = today.replace(day=last_thursday.day) + datetime.timedelta(days=7) expiry_date =
# weekly_expiry_date.strftime("%d%b%Y")[0:5] option_symbol = f"NIFTY{current_year}{expiry_date}{current_month}{
# weekly_expiry_date.strftime('%d')}{strike_price}{direction}"
#
#     return option_symbol

def generate_nearest_thursday_option_symbol(index, strike_price, direction):
    today = datetime.today()
    weekly_expiry_date = None
    if index == "NIFTY":
        nearest_thursday = next_weekday(today, 3)
        weekly_expiry_date = today.replace(day=nearest_thursday.day) + timedelta(days=0)
    elif index == "BANKNIFTY":
        nearest_wednesday = next_weekday(today, 2)
        weekly_expiry_date = today.replace(day=nearest_wednesday.day) + timedelta(days=0)

    # if current_day >= last_thursday.day:
    #     # Monthly expiry
    #     expiry_date = last_thursday.strftime("%b").upper()
    #     option_symbol = f"{index}{current_year}{expiry_date}{strike_price}{direction}"
    # else:
    # Weekly expiry

    print(weekly_expiry_date)
    current_year = today.year % 100
    current_month = today.month
    expiry_date = weekly_expiry_date.strftime("%d%b%Y")[0:5]
    option_symbol = f"{index}{current_year}{current_month}{weekly_expiry_date.strftime('%d')}{strike_price}{direction}"

    return option_symbol


def get_monthly_expiry_symbol(symbol, strike_price, option):
    today = datetime.date.today()
    last_thursday_date = get_all_thursdays_of_current_month()[-1]
    if last_thursday_date - today.day > 2:
        return f"{symbol}{today.year % 100}{months[today.month - 1]}{strike_price}{option}"


# print(get_monthly_expiry_symbol("NIFTY", 20000, "CE"))


def get_historical_data(fyers, symbol, timeframe, range_from, range_to):
    data = {
        "symbol": symbol,
        "resolution": timeframe,
        "date_format": "1",
        "range_from": range_from,
        "range_to": range_to,
        "cont_flag": "1"
    }
    print(data)
    response = fyers.history(data=data)
    # print(response)
    if "candles" in response:
        return pd.DataFrame(response["candles"])
    return pd.DataFrame()


def get_historical_data_v1(fyers, symbol, timeframe, range_from, range_to):
    # if "NIFTY" in symbol:
    #     symbol = f"NSE:{symbol}-INDEX"
    # else:
    #     symbol = f"NSE:{symbol}-EQ"

    nse_symbol = all_stocks_list.get_symbol_for_stock(symbol)

    data = {
        "symbol": nse_symbol,
        "resolution": timeframe,
        "date_format": "1",
        "range_from": range_from,
        "range_to": range_to,
        "cont_flag": "1"
    }
    print(data)
    response = fyers.history(data=data)
    print(response["code"])
    print(response["s"])
    print(response["message"])
    if "candles" in response:
        df = pd.DataFrame(response["candles"])
        if df.empty:
            return pd.DataFrame()
        df[0] = convert_column_from_epoch_to_date(df[0])
        return df
    return pd.DataFrame()


def get_candles_data(fyers, symbol, timeframe, period):
    today = datetime.today()
    range_from = get_anchor_date(period, timeframe)
    range_to = today.strftime("%Y-%m-%d")
    print(range_from)
    df = get_historical_data(fyers, symbol, timeframe, range_from, range_to)
    if df.empty:
        return df

    df[0] = convert_column_from_epoch_to_date(df[0])

    print(df)
    return df


def get_weekly_historical_data(fyers, symbol, upto_date, n):
    start_date = get_start_of_week(datetime.today())
    candles_list = []
    while n > 0:
        data = {
            "symbol": symbol,
            "resolution": "D",
            "date_format": "1",
            "range_from": start_date,
            "range_to": upto_date,
            "cont_flag": "1"
        }
        candle = []
        response = fyers.history(data=data)
        df = pd.DataFrame(response["candles"])
        df[0] = convert_column_from_epoch_to_date(df[0])
        # print(f"Week {start_date}")
        # print(f"open: {df.iloc[0, 1]}")
        # print(f"high: {df[2].max()}")
        # print(f"low: {df[3].min()}")
        # print(f"close: {df.iloc[-1, 4]}")
        # print(f"vol: {df[5].sum()}")
        candle.append(start_date)
        candle.append(df.iloc[0, 1])
        candle.append(df[2].max())
        candle.append(df[3].min())
        candle.append(df.iloc[-1, 4])
        candle.append(df[5].sum())
        candles_list.append(candle)

        upto_date = datetime.strptime(start_date, "%Y-%m-%d") - timedelta(days=1)
        start_date = get_start_of_week(upto_date)
        upto_date = upto_date.strftime("%Y-%m-%d")
        n = n-1
    candles_list.reverse()
    return pd.DataFrame(candles_list)


def convert_column_from_epoch_to_date(df_column):
    converted_times = []
    for epoch_time in df_column:
        timestamp = datetime.fromtimestamp(epoch_time).strftime('%d-%m-%Y %H:%M:%S')
        converted_times.append(timestamp)

    return converted_times


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


def trigger_exit_order(position, positions, fyers):
    id = position.get_symbol()
    data = {
        "id": id
    }
    response = fyers.exit_positions(data=data)
    print(response)
    if response["s"] == "ok":
        positions.pop(position.get_symbol())
        with PositionDAO() as position_dao:
            position_dao.close_position(position.id)


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0:  # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)


def send_sms(text):
    account_sid = 'AC393b2d1c8c597e036a1a2093bb512a3e'
    auth_token = '044474008e1d4ed93d6e83cfdf0bec50'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+12565883088',
        body=text,
        to='+918717892888'
    )

    print(message.sid)


def calculate_vwap_for_candles_dataframe(df):
    max_high_index = df[2].idxmax()

    print(df.iloc[max_high_index:][2])

    sum__of_vol_by_price = (df.iloc[max_high_index:][5] * df.iloc[max_high_index:][2]).sum()
    total_volume = df.iloc[max_high_index:][5].sum()
    return sum__of_vol_by_price / total_volume

def get_anchored_vwap(fyers, symbol, timeframe, period):
    anchor_date = get_anchor_date(period, timeframe)
    print(anchor_date)
    range_from = anchor_date
    today = datetime.today()
    range_to = today.strftime("%Y-%m-%d")
    df = get_historical_data(fyers, symbol, timeframe, range_from, range_to)
    df[0] = convert_column_from_epoch_to_date(df[0])
    max_high_index = df[2].idxmax()

    print(df.iloc[max_high_index:][2])

    sum__of_vol_by_price = (df.iloc[max_high_index:][5] * df.iloc[max_high_index:][2]).sum()
    total_volume = df.iloc[max_high_index:][5].sum()
    return sum__of_vol_by_price / total_volume

def get_previous_anchored_vwap(fyers, symbol, timeframe, period):
    anchor_date = get_anchor_date(period + 1, timeframe)
    print(anchor_date)
    range_from = anchor_date
    today = datetime.today()
    range_to = today.strftime("%Y-%m-%d")
    df = get_historical_data(fyers, symbol, timeframe, range_from, range_to)
    df[0] = convert_column_from_epoch_to_date(df[0])
    df.drop(df.index[-1], inplace=True)

    max_high_index = df[2].idxmax()

    print(df.iloc[max_high_index:][2])

    sum__of_vol_by_price = (df.iloc[max_high_index:][5] * df.iloc[max_high_index:][2]).sum()
    total_volume = df.iloc[max_high_index:][5].sum()
    return sum__of_vol_by_price / total_volume


def get_weekly_anchored_vwap(fyers, symbol, period):
    df = get_weekly_historical_data(fyers, symbol, datetime.today().strftime("%Y-%m-%d"), period)
    df.drop(df.index[-1], inplace=True)
    return calculate_vwap_for_candles_dataframe(df)


def get_previous_resistance_anchored_vwap(df):
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
