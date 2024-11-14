
from dao.ohlc_dao import OhlcDao
import pandas as pd
from pymongo.errors import DuplicateKeyError
from pymongo.mongo_client import MongoClient
from pymongo import ASCENDING
from pymongo.server_api import ServerApi
from pymongo.errors import BulkWriteError
from datetime import datetime
import time


class MongoOhlcDao(OhlcDao):
    def __init__(self, client: MongoClient, database: str, collection: str):
        self.client = client
        self.db = self.client[database]
        self.collection = self.db[collection]

    def upload_data_from_dataframe(self, df: pd.DataFrame):
        records = df.to_dict('records')
        self.collection.insert_many(records)

    def query_stock_data(self, stock_name: str, start_date: str, end_date: str) -> pd.DataFrame:
        query = {
            "symbol": stock_name,
            "time": {
                "$gte": start_date,
                "$lte": end_date
            }
        }
        cursor = self.collection.find(query).sort("date", ASCENDING)
        data = list(cursor)
        # print(data)
        return pd.DataFrame(data)

    def query_all_stocks_data_between_time_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        query = {
            "time": {
                "$gte": start_date,
                "$lte": end_date
            }
        }
        cursor = self.collection.find(query).sort([("symbol", ASCENDING), ("time", ASCENDING)])
        data = list(cursor)
        return pd.DataFrame(data)

    def update_stock_data(self, stock_name: str, date: str, new_ohlc_data: dict):
        query = {"symbol": stock_name, "date": date}
        update = {"$set": new_ohlc_data}
        self.collection.update_one(query, update)


# Example usage:
uri = "mongodb+srv://atik4:atik1234@serverlessinstance0.kwkyme9.mongodb.net/?retryWrites=true&w=majority&appName=ServerlessInstance0"

# Create a new client and connect to the server
mongo_client = MongoClient(uri, server_api=ServerApi('1'), tlsAllowInvalidCertificates=True)
# db = client['StocksGo']
# collection = db['stock_ohlc']

# Send a ping to confirm a successful connection
# try:
#     mongo_client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

dao = MongoOhlcDao(mongo_client, "StocksGo", "stock_ohlc")
# print(dao.query_stock_data("ASIANPAINT", "2023-01-01", "2024-01-05"))
start_time = time.time()
# print(dao.query_stock_data("ASIANPAINT", "2023-01-01", "2024-01-05"))
print(dao.query_all_stocks_data_between_time_range("2023-06-01", "2024-01-05"))
print("time spent: ", time.time() - start_time)


# dao.upload_data_from_dataframe(df)
# print(dao.query_stock_data("AAPL", "2024-01-01", "2024-01-02"))
# print(dao.query_all_stocks_data_between_time_range("2024-01-01", "2024-01-02"))
# dao.update_stock_data("AAPL", "2024-01-01", {"open": 101})
