from constants.constants import STRATEGIES, SUPPORT_LEVEL, SUPPORT_ZONE, AVWAP_SUPPORT, SYMBOL, CLOSING_PRICE
from mainV3 import fyers
import portfolio_dao
from utils import get_historical_data_v1, get_candles_data, get_previous_resistance_anchored_vwap
from calendar_utils import get_today_in_yyyy_mm_dd

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
            if SUPPORT_LEVEL in strategy:
                print("support level: ")
                print(strategy[SUPPORT_LEVEL])
                if latest_closing_price < strategy[SUPPORT_LEVEL]:
                    print(f"{stock['symbol']} has broken out of resistance level {strategy[SUPPORT_LEVEL]}")
                    message = f"{stock['symbol']} has broken out of resistance level {strategy[SUPPORT_LEVEL]}"
            elif SUPPORT_ZONE in strategy:
                print("support zone: ")
                print(strategy[SUPPORT_ZONE])
                if latest_closing_price < strategy[SUPPORT_ZONE][0]:
                    # notify the user
                    print(f"{stock['symbol']} has broken down from support zone {strategy[SUPPORT_ZONE]}")
                    message = f"{stock['symbol']} has broken down from support zone {strategy[SUPPORT_ZONE]}"

                elif latest_closing_price < strategy[SUPPORT_ZONE][1]:
                    # notify the user
                    print(f"{stock['symbol']} is within the support zone {strategy[SUPPORT_ZONE]}")
                    message = f"{stock['symbol']} is within the support zone {strategy[SUPPORT_ZONE]}"
                    stock[CLOSING_PRICE] = latest_closing_price
            if AVWAP_SUPPORT in strategy:
                print("avwap resistance")
                print(strategy[AVWAP_SUPPORT])
                if check_for_avwap_breakout(symbol, strategy[AVWAP_SUPPORT], stock):
                    message = create_avwap_message(message, strategy[AVWAP_SUPPORT], stock["symbol"])
                    # notify the user
                    print(f"{stock['symbol']} has broken down from avwap support {strategy[AVWAP_SUPPORT]['value']}")

        # print("message for user: " + message)
    except Exception as e:
        print(e)

def check(logged_in_users, timeframe):
    try:
        for user in logged_in_users:
            stocks_list = portfolio_dao.get_portfolio(user)["stocks"]
            # for every stock in the list, loop through the list and check if the conditions are met
            for stock in stocks_list:
                check_for_conditions(stock, timeframe)
                # print(stock)

            portfolio_dao.update_portfolio(user, stocks_list)
    except Exception as e:
        print(e)


logged_in_users = ["atik"]
check(logged_in_users, "30")