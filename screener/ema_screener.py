from screener.screener import Screener
import pandas_ta as ta

class EMAScreener(Screener):
    def __init__(self, period, timeframe):
        self.period = period
        self.timeframe = timeframe

        def run(self, df, symbols):
            print('Running EMA screener')
            results = {}

            for symbol in symbols:
                # Filter DataFrame for the current symbol
                symbol_df = df[df['symbol'] == symbol]

                # Ensure the DataFrame is sorted by time in ascending order
                symbol_df = symbol_df.sort_values(by='time')

                # Calculate EMA for the 'close' prices with the default period (14)
                symbol_df['EMA'] = symbol_df['close'].ewm(span=self.period, adjust=False).mean().round(2)

                # Get the last EMA value for the symbol
                last_ema = symbol_df['EMA'].iloc[-1]

                # Store the result
                results[symbol] = last_ema

            return results