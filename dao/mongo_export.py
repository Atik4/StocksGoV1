from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import BulkWriteError

from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
import json

cluster = Cluster('couchbase://localhost', ClusterOptions(PasswordAuthenticator('root', 'root1234')))
bucket = cluster.bucket('stock_alerts')
collection = bucket.default_collection()

bucket_name = 'stock_ohlc'

query = "SELECT meta().id AS doc_id, * FROM `stock_ohlc`"

# Execute the query
result = cluster.query(query)

# Prepare to write to file
data_to_write = []


def transform_row(row):
    stock_ohlc = row['stock_ohlc']
    document_data = {
        "_id": row['doc_id'],
        "time": stock_ohlc['time'],
        "symbol": stock_ohlc['symbol'],
        "open": stock_ohlc['open'],
        "high": stock_ohlc['high'],
        "low": stock_ohlc['low'],
        "close": stock_ohlc['close'],
        "volume": stock_ohlc['volume']
    }
    return document_data


# Loop through the results and store them in a list
for row in result:
    # Append a dictionary with both the document ID and the content
    document_data = transform_row(row)
    data_to_write.append(document_data)

uri = "mongodb+srv://atik4:atik1234@serverlessinstance0.kwkyme9.mongodb.net/?retryWrites=true&w=majority&appName=ServerlessInstance0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), tlsAllowInvalidCertificates=True)
db = client['StocksGo']
collection = db['stock_ohlc']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# try:
#     # collection.insert_one(data_to_write[0])
#     collection.insert_many(data_to_write)
#     print("DataFrame data inserted successfully!")
# except BulkWriteError as e:
#     print("Error occurred:", e.details)
