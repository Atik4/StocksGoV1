import sqlite3
from datetime import datetime
from position import Position


class PositionDAO:
    def __init__(self, db_name='/Users/atik.agarwal/Projects/personal/trading/dao/trading.db'):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()

    def insert_position(self, position):
        self.cursor.execute('''
            INSERT INTO positions (
                created_at, entry_price, ltp, strike_price, symbol, quantity, 
                sl, sl_underlying, target, direction, buy_price, sell_price, strategy, state
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            position.created_at, position.entry_price, position.ltp, position.strike_price,
            position.symbol, position.quantity, position.sl, position.sl_underlying,
            position.target, position.direction, position.buy_price, position.sell_price,
            position.strategy, position.state
        ))

    def get_position(self, symbol, strategy, state):
        self.cursor.execute('''
            SELECT * FROM positions
            WHERE date(created_at) = date(?) 
                AND state = ? 
                AND symbol LIKE ? 
                AND strategy = ?
        ''', (datetime.now().strftime('%Y-%m-%d'), state, f'{symbol}%', strategy))

        data = self.cursor.fetchone()

        if data:
            position = Position(
                id=data[0], entry_price=data[2], ltp=data[3], strike_price=data[4], symbol=data[5],
                quantity=data[6], sl=data[7], sl_underlying=data[8], target=data[9],
                direction=data[10], buy_price=data[11], sell_price=data[12],
                strategy=data[13], state=data[14]
            )
            return position
        else:
            return None

    def close_position(self, position_id):
        self.cursor.execute('''
            UPDATE positions
            SET state = ?
            WHERE id = ?
        ''', ('open', position_id))
        self.conn.commit()


# position_id = 10  # Replace with the actual position ID you want to update
# with PositionDAO() as position_dao:
#     position_dao.close_position(position_id)

# from datetime import datetime
#
symbol = 'XY'
strategy = 'Option'


with PositionDAO() as position_dao:
    position = position_dao.get_position(symbol, strategy, "open")

    if position:
        print("Position Found:")
        print(f"Symbol: {position.symbol}, Strategy: {position.strategy}, id: {position.id}")
    else:
        print("No matching position found.")

# test()
# Create a Position object
# pos = Position(
#     entry_price=100, ltp=110, strike_price=105, symbol='XYZ', quantity=10,
#     sl=90, sl_underlying=95, target=120, direction='Long', buy_price=102,
#     sell_price=108, strategy='Option', state='Active'
# )
#
# # Use the DAO with a context manager
# with PositionDAO() as position_dao:
#     position_dao.insert_position(pos)

# # Define a function to create the table
# def create_position_table():
#     conn = sqlite3.connect('trading.db')  # Connect to or create the database file
#     cursor = conn.cursor()
#
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS positions (
#         id INTEGER PRIMARY KEY,
#         created_at TEXT,
#         entry_price REAL,
#         ltp REAL,
#         strike_price REAL,
#         symbol TEXT,
#         quantity INTEGER,
#         sl REAL,
#         sl_underlying REAL,
#         target REAL,
#         direction TEXT,
#         buy_price REAL,
#         sell_price REAL,
#         strategy TEXT,
#         state TEXT
#     )
# ''')
#
#     # Commit and close the connection
#     conn.commit()
#     conn.close()

# Call the function to create the table
# create_position_table()
