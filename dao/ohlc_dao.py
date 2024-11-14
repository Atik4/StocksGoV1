from abc import ABC, abstractmethod
import pandas as pd


class OhlcDao(ABC):
    @abstractmethod
    def upload_data_from_dataframe(self, df: pd.DataFrame):
        pass

    @abstractmethod
    def query_stock_data(self, stock_name: str, start_date: str, end_date: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def query_all_stocks_data_between_time_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def update_stock_data(self, stock_name: str, date: str, new_ohlc_data: dict):
        pass
