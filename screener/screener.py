from abc import ABC, abstractmethod


class Screener(ABC):
    @abstractmethod
    def run(self, df, symbols):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_data_requirements(self):
        pass
