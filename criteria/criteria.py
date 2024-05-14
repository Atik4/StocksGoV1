from abc import ABC, abstractmethod
import pandas as pd

class Criteria(ABC):
    @abstractmethod
    def getName(self):
        pass

    @abstractmethod
    def isSatisfied(self, df):
        pass

    @abstractmethod
    def get_data_requirements(self):
        pass