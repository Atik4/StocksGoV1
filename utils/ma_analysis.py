from data_utils import data_utils
import ma_utils
import time
from stock_utils import all_stocks_list
import ma_dao

stocks_above_21_ema = []

def is_stock_above_ema(symbol, period, interval):
    try:
        ltp = data_utils.get_last_traded_price(symbol)
        if ltp is None:
            return
        df = ma_utils.get_ema(symbol, interval, period)
        if df.empty:
            return

        field = f"{period}ema"
        if ltp > df[field].iloc[-1]:
            stocks_above_21_ema.append(symbol)

        ma_info = ma_dao.get_stock_moving_average_info(symbol)
        if ma_info is not None:
            ma_info["moving_averages"][field] = {
                "value": df[field].iloc[-1],
                "date": df[0].iloc[-1]
            }
            ma_info["ltp"] = ltp
            ma_dao.update_stock_moving_average_info(symbol, ma_info)
        else:
            ma_info = {
                "symbol": symbol,
                "ltp": ltp,
                "moving_averages": {
                    f"{period}ema": {
                        "value": df[f"{period}ema"].iloc[-1],
                        "date": df[0].iloc[-1]
                    }
                }
            }
            ma_dao.add_stock_to_moving_averages_info(symbol, ma_info)
        return
    except Exception as e:
        print(e)

def get_stocks_above_ema(period, interval):
    symbols = all_stocks_list.symbols_list
    for symbol in symbols:
        # is_stock_above_ema(f"NSE:{symbol}-EQ", period, interval)
        is_stock_above_ema(symbol, period, interval)
        time.sleep(0.3)
    return stocks_above_21_ema

print(get_stocks_above_ema(10, "D"))
print(len(stocks_above_21_ema))
