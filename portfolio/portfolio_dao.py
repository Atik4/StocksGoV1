from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator

# Connect to the Cluster
cluster = Cluster('couchbase://localhost', ClusterOptions(
    PasswordAuthenticator('root', 'root1234')))
bucket = cluster.bucket('Portfolio')
collection = bucket.default_collection()
collection.upsert


def create_portfolio(user_id, stocks):
    """Insert data into the Portfolio collection."""
    watchlist_document = {
        "userId": user_id,
        "stocks": stocks
    }
    result = collection.upsert(f'user::{user_id}', watchlist_document)
    print(f"Document for user {user_id} inserted/updated successfully.")


def get_portfolio(user_id):
    """Retrieve the watchlist of a user given their user ID."""
    try:
        portfolio = collection.get(f'user::{user_id}').content_as[dict]
        return portfolio
    except Exception as e:
        print(f"Error: {e}")
        return None

def add_stock_to_portfolio(user_id, new_stock):
    """Add a stock to the user's portfolio given the userId and new stock details."""
    try:
        # Retrieve the current watchlist document for the user
        watchlist = collection.get(f'user::{user_id}').content_as[dict]

        # Add the new stock to the watchlist
        watchlist['stocks'].append(new_stock)

        # Update the watchlist document in the database
        collection.upsert(f'user::{user_id}', watchlist)
        print(f"Stock {new_stock['symbol']} added to user {user_id}'s portfolio.")
    except Exception as e:
        print(f"Error: {e}")


def update_portfolio(user_id, stocks_list):
    """Update the watchlist of a user given their user ID and new stock list."""
    create_portfolio(user_id, stocks_list)

def delete_stock_from_portfolio(user_id, stock_symbol):
    """Delete a stock from the user's portfolio given the userId and stock symbol."""
    try:
        # Retrieve the current portfolio document for the user
        portfolio = collection.get(f'user::{user_id}').content_as[dict]

        # Remove the stock with the given symbol
        portfolio['stocks'] = [stock for stock in portfolio['stocks'] if stock['symbol'] != stock_symbol]

        # Update the watchlist document in the database
        collection.upsert(f'user::{user_id}', portfolio)
        print(f"Stock {stock_symbol} removed from user {user_id}'s portfolio.")
    except Exception as e:
        print(f"Error: {e}")



data = {
    "userId": "atik",
    "stocks": [
        {
            "symbol": "MANINFRA",
            "qty": 200,
            "buy_price": 165.98,
            "total_investment": 33196,
            "observe": [
                {
                    "support_level": 220
                },
                {
                    "avwap_support": {
                        "period": 100,
                        "timeframe": "D"
                    }
                },
                {
                    "moving_averages": {
                        "type": "ema",
                        "period": 21,
                        "timeframe": "D"
                    }
                }
            ]
        },
        {
            "symbol": "INOXGREEEN",
            "qty": 200,
            "buy_price": 70.5,
            "total_investment": 14100,
            "observe": [
                {
                    "support_zone": [
                        120, 125
                    ]
                },
                {
                    "avwap_support": {
                        "period": 100,
                        "timeframe": "D"
                    }
                },
                {
                    "moving_averages": {
                        "type": "ema",
                        "period": 10,
                        "timeframe": "D"
                    }
                }
            ]
        }
    ]
}

create_portfolio("atik", data)