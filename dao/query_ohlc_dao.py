from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
import pandas as pd

# Connect to the Cluster
cluster = Cluster('couchbase://localhost', ClusterOptions(
    PasswordAuthenticator('root', 'root1234')))
cb = cluster.bucket('stock_ohlc')
collection = cb.default_collection()

def query_stocks(start_date, end_date):
    query = f"""
    SELECT symbol, date, open, high, low, close, volume
    FROM `stock_ohlc`
    WHERE date BETWEEN $start_date AND $end_date
    ORDER BY symbol, date
    """
    result = cluster.query(query, start_date=start_date, end_date=end_date)

    # Extracting rows into a list of dictionaries
    rows = [row for row in result]

    # Converting the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(rows)

    # Reordering the columns as specified
    df = df[['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']]

    return df

# Example usage
# if __name__ == "__main__":
#     start_date = "2023-03-01"
#     end_date = "2023-04-03"
#     stock_data_df = query_stocks(start_date, end_date)
#     print(stock_data_df)


def query_single_stock(stock_symbol, start_date, end_date):
    """
    Queries stock data for a single stock based on its symbol and a date range.

    :param stock_symbol: The stock symbol (str).
    :param start_date: Start date in 'YYYY-MM-DD' format (str).
    :param end_date: End date in 'YYYY-MM-DD' format (str).
    :return: Pandas DataFrame containing the queried data for the specified stock.
    """
    query = f"""
    SELECT symbol, date, open, high, low, close, volume
    FROM `stock_ohlc`
    WHERE symbol = $stock_symbol AND date BETWEEN $start_date AND $end_date
    ORDER BY date
    """
    result = cluster.query(query, stock_symbol=stock_symbol, start_date=start_date, end_date=end_date)

    # Extracting rows into a list of dictionaries
    rows = [row for row in result]

    # Converting the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(rows)

    # Reordering the columns as specified
    df = df[['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']]

    return df

# Example usage
if __name__ == "__main__":
    stock_symbol = "AAPL"
    start_date = "2023-04-01"
    end_date = "2023-04-03"
    single_stock_data_df = query_single_stock(stock_symbol, start_date, end_date)
    print(single_stock_data_df)

