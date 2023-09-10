from abc import ABC, abstractmethod


class BaseQuery(ABC):
    @abstractmethod
    def build(self):
        pass


class Expression(ABC):
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def params(self):
        pass
