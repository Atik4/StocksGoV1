from datetime import timedelta
import traceback
from couchbase.exceptions import CouchbaseException
from couchbase.auth import PasswordAuthenticator
import pandas as pd
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions

# Define connection parameters
endpoint = "couchbases://cb.cinqviaqklro586a.cloud.couchbase.com"
username = "root"
password = "Root@1234"
bucket_name = "stocksGo"
scope_name = "stocksGo"
collection_name = "stock_ohlc"

# Static cluster connection setup
auth = PasswordAuthenticator(username, password)
options = ClusterOptions(auth)
options.apply_profile("wan_development")

def get_cluster_connection():
    try:
        cluster = Cluster(endpoint, options)
        cluster.wait_until_ready(timedelta(seconds=5))
        return cluster
    except Exception as e:
        print("Failed to connect to Couchbase cluster.")
        traceback.print_exc()
        return None

# Initialize cluster connection
cluster = get_cluster_connection()

if cluster:
    try:
        cb = cluster.bucket(bucket_name)
        cb_coll = cb.scope(scope_name).collection(collection_name)

        def fetch_document(doc_id):
            try:
                result = cb_coll.get(doc_id)
                print("\nFetch document success. Result: ", result.content_as[dict])
            except CouchbaseException as e:
                print(f"Failed to fetch document: {e}")

        def query_stock_data(symbol, start_date, end_date):
            query = f"""
            SELECT * FROM stocksGo.stocksGo.stock_ohlc s 
            WHERE s.stock_ohlc.symbol = "{symbol}" 
              AND s.stock_ohlc.time BETWEEN "{start_date}" AND "{end_date}" 
            ORDER BY s.stock_ohlc.time"""

            try:
                result = cluster.query(query)
                data = [row['s']['stock_ohlc'] for row in result.rows()]
                column_order = ['symbol', 'time', 'open', 'high', 'low', 'close', 'volume']
                df = pd.DataFrame(data, columns=column_order)
                return df
            except Exception as e:
                print(f"Error querying stock data: {e}")
                return pd.DataFrame()

        def query_all_stocks_data_between_time_range(start_date, end_date):
            query = f"""
            SELECT * FROM stocksGo.stocksGo.stock_ohlc s 
            WHERE s.stock_ohlc.time BETWEEN "{start_date}" AND "{end_date}" 
            ORDER BY s.stock_ohlc.symbol, s.stock_ohlc.time"""

            try:
                result = cluster.query(query)
                data = [row['s']['stock_ohlc'] for row in result.rows()]
                column_order = ['symbol', 'time', 'open', 'high', 'low', 'close', 'volume']
                df = pd.DataFrame(data, columns=column_order)
                return df
            except Exception as e:
                print(f"Error querying stock data: {e}")
                return pd.DataFrame()


        # Fetch a specific document
        # fetch_document("3MINDIA_2016-07-20_000000")

        # Query stock data
        df = query_stock_data("ASIANPAINT", "2024-01-01", "2024-01-20")
        print(df)

        #Query all data
        df = query_all_stocks_data_between_time_range("2024-01-01", "2024-01-20")
        print(df)

    except Exception as e:
        traceback.print_exc()
else:
    print("Cluster connection is not established.")
