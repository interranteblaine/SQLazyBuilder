from ..core.base import Expression

from abc import ABC, abstractmethod


class Join(Expression, ABC):
    def __init__(self, table, condition):
        self.table = table
        self.condition = condition

    def __str__(self):
        return f"{self._join_type()} JOIN {self.table} ON {self.condition}"

    @abstractmethod
    def _join_type(self):
        pass

    @property
    def params(self):
        return self.condition.params


class InnerJoin(Join):
    def _join_type(self):
        return "INNER"


class LeftJoin(Join):
    def _join_type(self):
        return "LEFT"


class RightJoin(Join):
    def _join_type(self):
        return "RIGHT"


class FullJoin(Join):
    def _join_type(self):
        return "FULL"
