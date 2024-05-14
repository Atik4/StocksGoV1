import datetime
from mainV3 import fyers
from utils import get_historical_data, convert_column_from_epoch_to_date

def get_vwap_from_anchor_date(df, anchor_date=None):
    if anchor_date is not None:
        df = df[df.date.dt.date >= anchor_date]
        vol = df['vol'].values
        df['vwap'] = (df['close']*vol).cumsum()/vol.cumsum()
        return df

# fyers = fyersModel.FyersModel(is_async=False, client_id=app_id, token=login(),
#                               log_path="/Users/atik.agarwal/Projects/personal/trading/logs/")


today = datetime.date.today()
range_from = (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d")
range_to = today.strftime("%Y-%m-%d")

df = get_historical_data(fyers, "NSE:LTIM-EQ", "15", "2023-12-22", "2023-12-22")
print(df)
df[0] = convert_column_from_epoch_to_date(df[0])
#
print(df)
# csv_filename = 'stock_data.csv'
# df.to_csv(csv_filename, index=False)

# data = {
#     "symbol":"NSE:NIFTYBANK-INDEX",
#     "resolution":"5",
#     "date_format":"1",
#     "range_from":"2023-12-08",
#     "range_to":"2023-12-08",
#     "cont_flag":"1"
# }
#
# response = fyers.history(data=data)
# print(response)