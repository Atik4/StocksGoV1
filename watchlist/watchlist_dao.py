from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator

# Connect to the Cluster
cluster = Cluster('couchbase://localhost', ClusterOptions(
    PasswordAuthenticator('root', 'root1234')))
bucket = cluster.bucket('watchlist')
collection = bucket.default_collection()
collection.upsert

def create_watchlist(user_id, stocks):
    """Insert data into the Watchlist collection."""
    watchlist_document = {
        "userId": user_id,
        "stocks": stocks
    }
    result = collection.upsert(f'user::{user_id}', watchlist_document)
    print(f"Document for user {user_id} inserted/updated successfully.")


def get_watchlist(user_id):
    """Retrieve the watchlist of a user given their user ID."""
    try:
        watchlist = collection.get(f'user::{user_id}').content_as[dict]
        return watchlist
    except Exception as e:
        print(f"Error: {e}")
        return None


def add_stock_to_watchlist(user_id, new_stock):
    """Add a stock to the user's watchlist given the userId and new stock details."""
    try:
        # Retrieve the current watchlist document for the user
        watchlist = collection.get(f'user::{user_id}').content_as[dict]

        # Add the new stock to the watchlist
        watchlist['stocks'].append(new_stock)

        # Update the watchlist document in the database
        collection.upsert(f'user::{user_id}', watchlist)
        print(f"Stock {new_stock['symbol']} added to user {user_id}'s watchlist.")
    except Exception as e:
        print(f"Error: {e}")


def update_watchlist(user_id, stocks_list):
    """Update the watchlist of a user given their user ID and new stock list."""
    create_watchlist(user_id, stocks_list)


def delete_stock_from_watchlist(user_id, stock_symbol):
    """Delete a stock from the user's watchlist given the userId and stock symbol."""
    try:
        # Retrieve the current watchlist document for the user
        watchlist = collection.get(f'user::{user_id}').content_as[dict]

        # Remove the stock with the given symbol
        watchlist['stocks'] = [stock for stock in watchlist['stocks'] if stock['symbol'] != stock_symbol]

        # Update the watchlist document in the database
        collection.upsert(f'user::{user_id}', watchlist)
        print(f"Stock {stock_symbol} removed from user {user_id}'s watchlist.")
    except Exception as e:
        print(f"Error: {e}")


# Sample Data
stocks = [
    {"symbol": "LTIM"},
    {"symbol": "MUKANDLTD"},
    {"symbol": "MANINFRA"}
]
# Insert Data
# create_watchlist("atik", stocks)

# Add a new stock to the watchlist
# add_stock_to_watchlist("atik", {"symbol": "TCS"})

# Delete a stock from the watchlist
# delete_stock_from_watchlist("atik", "LTIM")

# Retrieve and print watchlist
# user_watchlist = get_watchlist("atik")
# print("User Watchlist:", user_watchlist)
