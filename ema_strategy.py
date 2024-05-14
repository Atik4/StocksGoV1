"""
strategy entry exit condition:-

Long Entry:
    - signal candle is high price is below the EMA and should not touch EMA and next candle should cross the signal candle high price
    - long: stoploss is signal candle low price

Short Entry:
    - signal candle is low price is above the EMA and should not touch EMA and next candle should cross the signal candle low price
    - short: stoploss is signal candle high price
"""

import os
import sys
import datetime
import logging
import numpy as np
import pandas as pd
import time

import warnings

warnings.filterwarnings("ignore")

current_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(current_dir)

# from data_handler import ya_fin as yd
# from data_handler import fetch_data as fd
from data_handler import fetch_shiny as fs

from calc import calc_ind

# symbol = "ES_15Min_2020"
symbol = "mnq_data_15Min"
file_name = symbol

logging.basicConfig(
    filename="./bt_strategy/bt_cs_ema_strategy/cs_ema_log/" + file_name + ".log",
    # format="%(asctime)s : %(name)s : %(levelname)s => %(message)s",
    format="%(levelname)s => %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    filemode="w",
)

log = logging.getLogger(file_name)
log.setLevel(logging.INFO)


def get_data(path):
    raw_data = pd.read_csv(path)
    data = raw_data.copy()
    data["Datetime"] = pd.to_datetime(data["Date"] + " " + data[" Time"])
    data.rename(
        columns={" Open": "Open", " High": "High", " Low": "Low", " Last": "Close"},
        inplace=True,
    )
    data.set_index("Datetime", inplace=True)

    return data


def calc_trailing_SL(entry_price, current_price, trailing_point=0):
    if trailing_point == 0:
        return 0
    trailSL = 0
    profit_points = int(current_price - entry_price)
    initial_SL = entry_price - trailing_point
    if profit_points >= trailing_point:
        factor = int(profit_points / trailing_point)
        trailSL = initial_SL + factor * trailing_point
    if profit_points < trailing_point:
        trailSL = initial_SL
    return trailSL


def ema_strategy(
        data, length, target_point, stoploss_point=None, tick_size=1, tick_value=1
):
    ind_col = "EMA_" + str(length)
    data["long_entry_price"] = np.nan
    data["long_exit_price"] = np.nan
    data["short_entry_price"] = np.nan
    data["short_exit_price"] = np.nan
    data["position"] = np.nan
    data["PnL"] = np.nan
    data["pnl_perc"] = np.nan

    long_trigger = False
    long_signal = False
    position = 0
    for i in range(1, len(data)):
        # dt = data.index[i].strftime("%Y-%m-%d %H:%M:%S")
        dt = data.index[i]
        Open = data["Open"].iloc[i]
        High = data["High"].iloc[i]
        Low = data["Low"].iloc[i]
        Close = data["Close"].iloc[i]
        ema = data[ind_col].iloc[i]
        prev_ema = data[ind_col].iloc[i - 1]

        prev_Open = data["Open"].iloc[i - 1]
        prev_High = data["High"].iloc[i - 1]
        prev_Low = data["Low"].iloc[i - 1]
        prev_Close = data["Close"].iloc[i - 1]

        # print(f"{dt}| {Close:<4.2f}| pos: {position}")

        if position == 0:
            # long entry
            # (prev_High < ema) and (High > ema)
            if (prev_High < ema) and (High > prev_High):
                position = 1
                entry_price = prev_High
                if stoploss_point is not None:
                    stoploss = (entry_price - prev_Low) * stoploss_point
                    sl_price = prev_Low + stoploss
                else:
                    sl_price = prev_Low
                sl_price = prev_Low
                target = (entry_price - prev_Low) * target_point
                target_price = target + entry_price
                long_mtm = Close - entry_price
                long_pnl = (long_mtm / tick_size) * tick_value
                pnl_perc = (long_mtm / abs(entry_price)) * 100
                data["long_entry_price"].iloc[i] = entry_price
                data["position"].iloc[i] = "Long Entry"
                long_trigger = f"Long Entry: {dt}|High: {High:<4.4f} |Low: {Low:<4.4f} |Close: {Close:<4.4f} |EMA: {ema:<4.4f}| EntryPrice: {entry_price:<4.4f}| SLP: {sl_price:<4.4f}| TP: {target_price:<4.4f}|MTM: {long_mtm:<4.4f}| PnL: {long_pnl:<4.4f}| PnL(%): {pnl_perc:<4.4f}| Target: {target:<4.4f}"
                log.warning(long_trigger)
                # log.info(long_trigger)
                print(long_trigger)
                continue

            # short entry
            if (prev_Low > ema) and (Low < prev_Low):
                position = -1
                short_entry_price = prev_Low
                if stoploss_point is not None:
                    short_stoploss = (short_entry_price - prev_High) * stoploss_point
                    short_sl_price = prev_High - short_stoploss
                else:
                    sl_price = prev_High
                short_sl_price = prev_High
                short_target = (short_entry_price - prev_High) * target_point
                short_target_price = short_target + short_entry_price

                # short_sl_price = prev_High
                # short_target = target_point * ((short_sl_price - short_entry_price) / 2)
                # short_target_price = short_entry_price - short_target

                short_mtm = short_entry_price - Close
                short_pnl = (short_mtm / tick_size) * tick_value
                short_pnl_perc = (short_mtm / abs(short_entry_price)) * 100
                data["short_entry_price"].iloc[i] = short_entry_price
                data["position"].iloc[i] = "Short Entry"
                short_trigger = f"Short Entry: {dt}|High: {High:<4.4f} |Low: {Low:<4.4f} |Close: {Close:<4.4f} |EMA: {ema:<4.4f}| EntryPrice: {short_entry_price:<4.4f}| SLP: {short_sl_price:<4.4f}| TP: {short_target_price:<4.4f}|MTM: {short_mtm:<4.4f}| PnL: {short_pnl:<4.4f}| PnL(%): {short_pnl_perc:<4.4f}| Target: {short_target:<4.4f}"
                log.warning(short_trigger)
                # log.info(short_trigger)
                print(short_trigger)
                continue

            elif position == 0:
                no_trade = f"No Trade: {dt} |High: {High:<4.4f} |Low: {Low:<4.4f} |Close: {Close:<4.4f} |EMA: {ema:<4.4f}"
                log.info(no_trade)
                print(no_trade)
                continue

        if position == 1:
            long_mtm = Close - entry_price
            long_pnl = long_mtm * tick_size
            pnl_perc = long_mtm / abs(entry_price)
            # target hit
            if High >= target_price:
                position = 0
                long_mtm = High - entry_price
                long_pnl = (long_mtm / tick_size) * tick_value
                pnl_perc = long_mtm / abs(entry_price)
                data["pnl_perc"].iloc[i] = pnl_perc
                data["long_exit_price"].iloc[i] = High
                data["PnL"].iloc[i] = long_pnl
                data["position"].iloc[i] = "Long Target Hit"
                long_target_hit = f"Long Target Hit: {dt}|High: {High:<4.4f} |Low: {Low:<4.4f} |Close: {Close:<4.4f} |EMA: {ema:<4.4f}|MTM: {long_mtm:<4.4f}| PnL: {long_pnl:<4.4f}| PnL(%): {pnl_perc:<4.4f}\n"
                log.warning(long_target_hit)
                # log.info(long_target_hit)
                print(long_target_hit)
                continue
            # stoploss hit
            if Low <= sl_price:
                position = 0
                long_mtm = Low - entry_price
                long_pnl = (long_mtm / tick_size) * tick_value
                pnl_perc = long_mtm / abs(entry_price)
                data["pnl_perc"].iloc[i] = pnl_perc
                data["long_exit_price"].iloc[i] = Low
                data["PnL"].iloc[i] = long_pnl
                data["position"].iloc[i] = "Long Stoploss Hit"
                long_stoploss_hit = f"Long Stoploss Hit: {dt}|High: {High:<4.4f} |Low: {Low:<4.4f} |Close: {Close:<4.4f} |EMA: {ema:<4.4f}|MTM: {long_mtm:<4.4f}| PnL: {long_pnl:<4.4f}| PnL(%): {pnl_perc:<4.4f}\n"
                log.warning(long_stoploss_hit)
                print(long_stoploss_hit)
                continue
            else:
                long_carry = f"Long carry: {dt}|High: {High:<4.4f} |Low: {Low:<4.4f} |Close: {Close:<4.4f} |EMA: {ema:<4.4f}|MTM: {long_mtm:<4.4f}| PnL: {long_pnl:<4.4f}| PnL(%): {pnl_perc:<4.4f}"
                log.info(long_carry)
                print(long_carry)
                continue

        if position == -1:
            short_mtm = short_entry_price - Close
            short_pnl = short_mtm * tick_size
            short_pnl_perc = short_mtm / abs(short_entry_price)

            # target hit
            if Low <= short_target_price:
                position = 0
                short_mtm = short_entry_price - Low
                short_pnl = (short_mtm / tick_size) * tick_value
                short_pnl_perc = short_mtm / abs(short_entry_price)
                data["pnl_perc"].iloc[i] = short_pnl_perc
                data["short_exit_price"].iloc[i] = Low
                data["PnL"].iloc[i] = short_pnl
                data["position"].iloc[i] = "Short Target Hit"
                short_target_hit = f"Short Target Hit: {dt}|High: {High:<4.4f} |Low: {Low:<4.4f} |Close: {Close:<4.4f} |EMA: {ema:<4.4f}|MTM: {short_mtm:<4.4f}| PnL: {short_pnl:<4.4f}| PnL(%): {short_pnl_perc:<4.4f}\n"
                log.warning(short_target_hit)
                # log.info(long_target_hit)
                print(short_target_hit)
                continue

            # stoploss hit
            if High >= short_sl_price:
                position = 0
                short_mtm = short_entry_price - High
                short_pnl = (short_mtm / tick_size) * tick_value
                short_pnl_perc = short_mtm / abs(short_entry_price)
                data["pnl_perc"].iloc[i] = short_pnl_perc
                data["short_exit_price"].iloc[i] = High
                data["PnL"].iloc[i] = short_pnl
                data["position"].iloc[i] = "Short Stoploss Hit"
                short_stoploss_hit = f"Short Stoploss Hit: {dt}|High: {High:<4.4f} |Low: {Low:<4.4f} |Close: {Close:<4.4f} |EMA: {ema:<4.4f}|MTM: {short_mtm:<4.4f}| PnL: {short_pnl:<4.4f}| PnL(%): {short_pnl_perc:<4.4f}\n"
                log.warning(short_stoploss_hit)
                # log.info(long_target_hit)
                print(short_stoploss_hit)
                continue
            else:
                short_carry = f"Short carry: {dt}|High: {High:<4.4f} |Low: {Low:<4.4f} |Close: {Close:<4.4f} |EMA: {ema:<4.4f}| PnL: {short_pnl:<4.4f}| PnL(%): {short_pnl_perc:<4.4f}"
                log.info(short_carry)
                print(short_carry)
                continue
    return data


# res_df = ema_strategy(path + "/" + file_name + ".csv", length=15)
# res_df.to_csv("./bt_strategy/result_csv/pk_2/" + file_name + ".csv")

path = "./data/pratik_data/"
data = get_data(path=path + symbol + ".csv")
print(data)

length = 5
stoploss_point = 0.5
target_point = 1
tick_size = 0.25
tick_value = 0.5

df = calc_ind.ema_ind(data=data, length=length)
res_df = ema_strategy(
    df,
    length=length,
    target_point=target_point,
    stoploss_point=stoploss_point,
    tick_size=tick_size,
    tick_value=tick_value,
)
result_path = (
        "./bt_strategy/bt_cs_ema_strategy/cs_ema_result_csv/res_"
        + str(stoploss_point)
        + "_"
        + str(target_point)
        + "_"
        + symbol
        + ".csv"
)
print(result_path)
res_df.to_csv(result_path)