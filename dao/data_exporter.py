from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
import json

def write_data(bucket_name, data_to_write, index):
    with open(f'{bucket_name}{index+1}.json', 'w') as f:
        f.write('[')  # Start of the JSON array
        first = True  # Flag to check if it's the first element in the loop
        for row in data_to_write:
            if not first:
                f.write(',')  # Write a comma before every new JSON object except the first
            json.dump(row, f)  # Dump the JSON row to the file
            first = False  # Set first to False after the first iteration
        f.write(']')  # End of the JSON array



cluster = Cluster('couchbase://localhost', ClusterOptions(PasswordAuthenticator('root', 'root1234')))
bucket = cluster.bucket('stock_alerts')
collection = bucket.default_collection()

bucket_name = 'stock_ohlc'

query = "SELECT meta().id AS doc_id, * FROM `stock_ohlc`"

# Execute the query
result = cluster.query(query)

# Prepare to write to file
data_to_write = []

# Loop through the results and store them in a list
for row in result:
    # Append a dictionary with both the document ID and the content
    stock_ohlc = row['stock_ohlc']
    document_data = {
        "id": row['doc_id'],
        "time": stock_ohlc['time'],
        "symbol": stock_ohlc['symbol'],
        "open": stock_ohlc['open'],
        "high": stock_ohlc['high'],
        "low": stock_ohlc['low'],
        "close": stock_ohlc['close'],
        "volume": stock_ohlc['volume']
    }
    data_to_write.append(document_data)


def split_list(lst, chunk_size):
    """Split the list into chunks of specified size."""
    # Loop through the list in steps of chunk_size
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]



chunk_size = 100000
chunks = split_list(data_to_write, chunk_size)

# Verify the result
# print(f"Total chunks created: {len(chunks)}")
# for index, chunk in enumerate(chunks):
#     print(f"Chunk {index+1} size: {len(chunk)}")
#

# print(len(data_to_write))

for index, chunk in enumerate(chunks):
    write_data(bucket_name, chunk, index)

# Open a file to write
# with open(f'{bucket_name}.json', 'w') as f:
#     f.write('[')  # Start of the JSON array
#     first = True  # Flag to check if it's the first element in the loop
#     for row in data_to_write:
#         if not first:
#             f.write(',')  # Write a comma before every new JSON object except the first
#         json.dump(row, f)  # Dump the JSON row to the file
#         first = False  # Set first to False after the first iteration
#     f.write(']')  # End of the JSON array