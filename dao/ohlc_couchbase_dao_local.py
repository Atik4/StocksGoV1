from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
import pandas as pd
from datetime import datetime
from dao.ohlc_dao import OhlcDao

class CouchbaseLocal(OhlcDao):
    def __init__(self):
        self.cluster = Cluster('couchbase://localhost', ClusterOptions(
            PasswordAuthenticator('root', 'root1234')))
        self.cb = self.cluster.bucket('stock_ohlc')
        self.collection = self.cb.default_collection()

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
            self.collection.upsert(doc_id, document)
            print(f"Uploaded data for {doc_id}")

    def query_stock_data(self, stock_name: str, start_date: str, end_date: str) -> pd.DataFrame:
        query = f"""
        SELECT `time`, `symbol`, `open`, `high`, `low`, `close`, `volume`
        FROM `stock_ohlc`
        WHERE symbol = "{stock_name}" AND `time` BETWEEN "{start_date}" AND "{end_date}"
        ORDER BY time 
        """
        try:
            result = self.cluster.query(query)
            data = [row for row in result]
            column_order = ['symbol', 'time', 'open', 'high', 'low', 'close', 'volume']
            df = pd.DataFrame(data, columns=column_order)
            return df
        except Exception as e:
            print(f"Error: {e}")
            return pd.DataFrame()

    def query_all_stocks_data_between_time_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        query = f"""
        SELECT `time`, `symbol`, `open`, `high`, `low`, `close`, `volume`
        FROM `stock_ohlc`
        WHERE `time` BETWEEN "{start_date}" AND "{end_date}"
        ORDER BY symbol, time
        """
        try:
            result = self.cluster.query(query)
            data = [row for row in result]
            column_order = ['symbol', 'time', 'open', 'high', 'low', 'close', 'volume']
            df = pd.DataFrame(data, columns=column_order)
            return df
        except Exception as e:
            print(f"Error: {e}")
            return pd.DataFrame()

    def update_stock_data(self, stock_name: str, date: str, new_ohlc_data: dict):
        doc_id = f"{stock_name}_{date}"
        document = self.collection.get(doc_id).content_as[dict]
        document['ohlc'] = new_ohlc_data
        self.collection.upsert(doc_id, document)
