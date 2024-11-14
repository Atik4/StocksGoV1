from datetime import timedelta, datetime
import traceback
from couchbase.exceptions import CouchbaseException
from couchbase.auth import PasswordAuthenticator
import pandas as pd
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from dao.ohlc_dao import OhlcDao


class CouchbaseCloud(OhlcDao):
    def __init__(self):
        endpoint = "couchbases://cb.cinqviaqklro586a.cloud.couchbase.com"
        username = "root"
        password = "Root@1234"
        bucket_name = "stocksGo"
        scope_name = "stocksGo"
        collection_name = "stock_ohlc"

        auth = PasswordAuthenticator(username, password)
        options = ClusterOptions(auth)
        options.apply_profile("wan_development")

        self.cluster = Cluster(endpoint, options)
        self.cluster.wait_until_ready(timedelta(seconds=5))
        self.cb = self.cluster.bucket(bucket_name)
        self.cb_coll = self.cb.scope(scope_name).collection(collection_name)

    def upload_data_from_dataframe(self, df: pd.DataFrame):
        for index, row in df.iterrows():
            date_str = row['time']
            dt = datetime.strptime(date_str, "%d-%m-%Y %H:%M:%S")
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
            self.cb_coll.upsert(doc_id, document)
            print(f"Uploaded data for {doc_id}")

    def query_stock_data(self, stock_name: str, start_date: str, end_date: str) -> pd.DataFrame:
        query = f"""
        SELECT * FROM stocksGo.stocksGo.stock_ohlc s 
        WHERE s.stock_ohlc.symbol = "{stock_name}" 
          AND s.stock_ohlc.time BETWEEN "{start_date}" AND "{end_date}" 
        ORDER BY s.stock_ohlc.time
        """
        try:
            result = self.cluster.query(query)
            data = [row['s']['stock_ohlc'] for row in result.rows()]
            column_order = ['symbol', 'time', 'open', 'high', 'low', 'close', 'volume']
            df = pd.DataFrame(data, columns=column_order)
            return df
        except Exception as e:
            print(f"Error querying stock data: {e}")
            return pd.DataFrame()

    def query_all_stocks_data_between_time_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        query = f"""
        SELECT * FROM stocksGo.stocksGo.stock_ohlc s 
        WHERE s.stock_ohlc.time BETWEEN "{start_date}" AND "{end_date}" 
        ORDER BY s.stock_ohlc.symbol, s.stock_ohlc.time
        """
        try:
            result = self.cluster.query(query)
            data = [row['s']['stock_ohlc'] for row in result.rows()]
            column_order = ['symbol', 'time', 'open', 'high', 'low', 'close', 'volume']
            df = pd.DataFrame(data, columns=column_order)
            return df
        except Exception as e:
            print(f"Error querying stock data: {e}")
            return pd.DataFrame()

    def update_stock_data(self, stock_name: str, date: str, new_ohlc_data: dict):
        doc_id = f"{stock_name}_{date}"
        document = self.cb_coll.get(doc_id).content_as[dict]
        document['ohlc'] = new_ohlc_data
        self.cb_coll.upsert(doc_id, document)
