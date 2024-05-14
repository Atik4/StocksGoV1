from _datetime import datetime

class Position:
    def __init__(self, entry_price, ltp, strike_price, symbol, quantity, sl, sl_underlying, target,
                 direction, buy_price, sell_price, strategy, state, id=None):
        self.id = id
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.entry_price = entry_price
        self.ltp = ltp
        self.strike_price = strike_price
        self.symbol = symbol
        self.quantity = quantity
        self.sl = sl
        self.sl_underlying = sl_underlying
        self.target = target
        self.direction = direction
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.strategy = strategy
        self.state = state

    # Getters
    def get_created_at(self):
        return self.created_at

    def get_entry_price(self):
        return self.entry_price

    def get_ltp(self):
        return self.ltp

    def get_strike_price(self):
        return self.strike_price

    def get_symbol(self):
        return self.symbol

    def get_quantity(self):
        return self.quantity

    def get_sl(self):
        return self.sl

    def get_sl_underlying(self):
        return self.sl_underlying

    def get_target(self):
        return self.target

    def get_direction(self):
        return self.direction

    def get_buy_price(self):
        return self.buy_price

    def get_sell_price(self):
        return self.sell_price

    def get_strategy(self):
        return self.strategy

    def get_state(self):
        return self.state

    # Setters
    def set_entry_price(self, entry_price):
        self.entry_price = entry_price

    def set_ltp(self, ltp):
        self.ltp = ltp

    def set_strike_price(self, strike_price):
        self.strike_price = strike_price

    def set_symbol(self, symbol):
        self.symbol = symbol

    def set_quantity(self, quantity):
        self.quantity = quantity

    def set_sl(self, sl):
        self.sl = sl

    def set_sl_underlying(self, sl_underlying):
        self.sl_underlying = sl_underlying

    def set_target(self, target):
        self.target = target

    def set_direction(self, direction):
        self.direction = direction

    def set_buy_price(self, buy_price):
        self.buy_price = buy_price

    def set_sell_price(self, sell_price):
        self.sell_price = sell_price

    def set_strategy(self, strategy):
        self.strategy = strategy

    def set_state(self, state):
        self.state = state

position = Position(entry_price="closing_price", ltp=None, strike_price="strike_price",
                    symbol=id, quantity=None, sl=None, sl_underlying="stoploss", target="target",
                    direction="up", buy_price="", sell_price=None, strategy="5EMA", state="open")
