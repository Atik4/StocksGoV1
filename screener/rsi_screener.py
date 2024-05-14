import pandas as pd
import pandas_ta as ta
from screener.screener import Screener
class RSI(Screener):
    def __init__(self, period, timeframe):
        self.period = period
        self.timeframe = timeframe

    def run(self, df, symbols):
        print('Running RSI screener')
        results = {}

        for symbol in symbols:
            # Filter DataFrame for the current symbol
            print(symbol)
            symbol_df = df[df['symbol'] == symbol]

            if symbol_df.empty:
                continue
            print(symbol_df)
            # Ensure the DataFrame is sorted by time in ascending order
            symbol_df = symbol_df.sort_values(by='time')

            # Calculate RSI for the 'close' prices with the default period (14)
            symbol_df['RSI'] = ta.rsi(symbol_df['close']).round(2)

            # Get the last RSI value for the symbol
            last_rsi = symbol_df['RSI'].iloc[-1]

            print("RSI for ", symbol, " is ", last_rsi)
            # Store the result
            if last_rsi > 70:
                results[symbol] = last_rsi

        return results
