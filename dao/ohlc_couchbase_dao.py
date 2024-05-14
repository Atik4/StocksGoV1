from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
from dateutil import parser
import pandas as pd
from datetime import datetime
from calendar_utils import convert_date_string_to_standard_format

# Connect to the Cluster
cluster = Cluster('couchbase://localhost', ClusterOptions(
    PasswordAuthenticator('root', 'root1234')))
cb = cluster.bucket('stock_ohlc')
collection = cb.default_collection()


def upload_data_from_dataframe(df):
    for index, row in df.iterrows():

        date_str = row['time']
        # Parse the original string to a datetime object
        dt = datetime.strptime(date_str, "%d-%m-%Y %H:%M:%S")

        # Format the datetime object into the new string format
        new_date_str = dt.strftime("%Y-%m-%d %H:%M:%S")

        doc_id = f"{row['symbol']}_{new_date_str.replace(' ', '_').replace(':', '')}"
        document = {
            "time": new_date_str,
            "symbol": row['symbol'],
            "open": row['open'],
            "high": row['high'],
            "low": row['low'],
            "close": row['close'],
            "volume": row['volume']
        }
        collection.upsert(doc_id, document)
        print(f"Uploaded data for {doc_id}")



def query_stock_data(cluster, stock_name, start_date, end_date):
    query = f"""
    SELECT `time`, `symbol`, `open`, `high`, `low`, `close`, `volume`
    FROM `stock_ohlc`
    WHERE symbol = "{stock_name}" AND `time` BETWEEN "{start_date}" AND "{end_date}"
    ORDER BY time 
"""

    try:
        # When executing the query, the parameters are passed directly, not wrapped in another dict or list.
        result = cluster.query(query)
        data = [row for row in result]
        column_order = ['symbol', 'time', 'open', 'high', 'low', 'close', 'volume']
        df = pd.DataFrame(data, columns=column_order)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

def query_all_stocks_data_between_time_range(start_date, end_date):
    query = f"""
    SELECT `time`, `symbol`, `open`, `high`, `low`, `close`, `volume`
    FROM `stock_ohlc`
    WHERE `time` BETWEEN "{start_date}" AND "{end_date}"
    ORDER BY symbol, time
    """

    try:
        result = cluster.query(query)
        data = [row for row in result]
        column_order = ['symbol', 'time', 'open', 'high', 'low', 'close', 'volume']
        df = pd.DataFrame(data, columns=column_order)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()


def update_stock_data(stock_name, date, new_ohlc_data):
    """
    Updates the OHLC data for a given stock on a given date.
    :param stock_name: The name of the stock (str).
    :param date: The date in 'YYYY-MM-DD' format (str).
    :param new_ohlc_data: A dict containing the new OHLC data.
    """
    doc_id = f"{stock_name}_{date}"
    document = collection.get(doc_id).content_as[dict]
    document['ohlc'] = new_ohlc_data
    collection.upsert(doc_id, document)



if __name__ == "__main__":
    # Example DataFrame
    # print(query_stock_data("NESTLEIND", "01-04-2024", "08-04-2024"))
    # print(query_stock_data("AAPL", "01-04-2024", "04-04-2024"))
    # Example usage:
    stock_name = 'RELIANCE'
    start_date = convert_date_string_to_standard_format('2024-04-01')
    end_date = convert_date_string_to_standard_format('2024-04-04')
    # results = query_stock_data(cluster, stock_name, start_date, end_date)
    results = query_all_stocks_data_between_time_range(start_date, end_date)
    print(results)

    # for result in results:
    #     print(result)