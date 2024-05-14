from abc import ABC, abstractmethod
from constants import constants

class Operator(ABC):
    @abstractmethod
    def getName(self):
        pass

    @abstractmethod
    def isSatisfied(self, indicator, value):
        pass

class Above(Operator):
    def __init__(self):
        self.name = "Above"

    def getName(self):
        return self.name

    def isSatisfied(self, indicator, value):
        return value > indicator[constants.CURR]

class Below(Operator):
    def __init__(self):
        self.name = "Below"

    def getName(self):
        return self.name

    def isSatisfied(self, indicator, value):
        return value < indicator[constants.CURR]

class CrossAbove(Operator):
    def __init__(self):
        self.name = "CrossAbove"

    def getName(self):
        return self.name

    def isSatisfied(self, indicator, value):
        return indicator[constants.PREV] < indicator[constants.CURR] and value > indicator[constants.CURR]

class CrossBelow(Operator):
    def __init__(self):
        self.name = "CrossBelow"

    def getName(self):
        return self.name

    def isSatisfied(self, indicator, curr_price):
        # Logic to determine if there was a crossover below the indicator value
        pass


class Between(Operator):
    def __init__(self):
        self.name = "Between"

    def getName(self):
        return self.name

    def isSatisfied(self, value, threshold):
        pass