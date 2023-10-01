from ..core.base import Expression, BaseQuery

from abc import ABC, abstractmethod


class Join(Expression, ABC):
    def __init__(self, table_or_subquery, condition):
        self.table = table_or_subquery
        self.condition = condition

    def __str__(self):
        if isinstance(self.table, BaseQuery):
            if not self.table.alias:
                raise ValueError("Alias required for subquery in JOIN clause.")
            subquery_sql, _ = self.table.build()
            return f"{self._join_type()} JOIN ({subquery_sql}) AS {self.table.alias} ON {self.condition}"
        else:
            return f"{self._join_type()} JOIN {self.table} ON {self.condition}"

    @abstractmethod
    def _join_type(self):
        pass

    @property
    def params(self):
        if isinstance(self.table, BaseQuery):
            _, subquery_params = self.table.build()
            return subquery_params + self.condition.params
        else:
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
