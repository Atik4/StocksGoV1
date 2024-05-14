from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator

# Connect to the Cluster
cluster = Cluster('couchbase://localhost', ClusterOptions(
    PasswordAuthenticator('admin', '123456')))
bucket = cluster.bucket('MovingAveragesInformation')
collection = bucket.default_collection()
collection.upsert

def add_stock_to_moving_averages_info(stock_symbol, moving_averages_info):
    """Add a stock to the moving averages information collection."""
    try:
        # Insert the moving averages information for the stock
        result = collection.upsert(f'stock::{stock_symbol}', moving_averages_info)
        print(f"Moving averages information for stock {stock_symbol} inserted/updated successfully.")
    except Exception as e:
        print(f"Error: {e}")

def get_stock_moving_average_info(stock_symbol):
    """Retrieve the moving averages information for a stock given its symbol."""
    try:
        moving_averages_info = collection.get(f'stock::{stock_symbol}').content_as[dict]
        return moving_averages_info
    except Exception as e:
        # print(f"Error: {e}")
        print(f"Moving averages information for stock {stock_symbol} not found.")
        return None

def update_stock_moving_average_info(stock_symbol, moving_averages_info):
    """Update the moving averages information for a stock given its symbol."""
    add_stock_to_moving_averages_info(stock_symbol, moving_averages_info)


# add_stock_to_moving_averages_info("RELIANCE", {"symbol": "RELIANCE", "moving_averages": {"21ma": {"value": 1234, "date": "2024-02-04"}}})
# update_stock_moving_average_info("RELIANCE", {"moving_averages": {"21ma": {"value": 1234, "date": "2024-02-04"}}})

# print(get_stock_moving_average_info("RELIANCE"))
# ma_info = get_stock_moving_average_info("RELIANCE")
# ma_info["moving_averages"]["21ma"] = {"value": 9851, "date": "2024-02-11"}
# update_stock_moving_average_info("RELIANCE", ma_info)