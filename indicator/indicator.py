from abc import ABC, abstractmethod

class Indicator(ABC):
    @abstractmethod
    def getName(self):
        pass

    @abstractmethod
    def calculateValue(self, dataframe):
        pass

    @abstractmethod
    def get_data_requirements(self):
        pass