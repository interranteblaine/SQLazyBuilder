from ..registry import register_query_class
from ..base import BaseQuery
from ..joins import JoinClause


@register_query_class
class SelectQuery(BaseQuery):
    def __init__(self):
        super().__init__()
        self._columns = []
        self._from_table = None
        self._distinct = False
        self._where_conditions = []
        self._joins = []
        self._group_by_columns = []
        self._having_conditions = []
        self._order_by = []
        self._limit = None
        self._offset = None

    def select(self, *columns):
        self._columns.extend(columns)
        return self

    def from_table(self, table):
        self._from_table = table
        return self

    def distinct(self):
        self._distinct = True
        return self

    def where(self, *conditions):
        self._where_conditions.extend(conditions)
        return self

    def inner_join(self, table, *conditions):
        self._joins.append(JoinClause("INNER JOIN", table, *conditions))
        return self

    def group_by(self, *columns):
        self._group_by_columns.extend(columns)
        return self

    def having(self, *conditions):
        self._having_conditions.extend(conditions)
        return self

    def order_by(self, column, direction="ASC"):
        self._order_by.append((column, direction))
        return self

    def limit(self, value):
        self._limit = value
        return self

    def offset(self, value):
        self._offset = value
        return self

    @property
    def params(self):
        parameters = []

        for condition in self._where_conditions:
            parameters.extend(condition.params)

        for join_clause in self._joins:
            parameters.extend(join_clause.params)

        for having_condition in self._having_conditions:
            parameters.extend(having_condition.params)

        return parameters

    def build(self):
        return str(self), self.params

    def __str__(self):
        if not self._from_table:
            raise ValueError(
                "A table must be specified using the 'from_table' method.")

        distinct_str = "DISTINCT " if self._distinct else ""
        query_parts = [
            f"SELECT {distinct_str}{', '.join(map(str, self._columns))} FROM {self._from_table}"
        ]

        if self._joins:
            join_str = " ".join(map(str, self._joins))
            query_parts.append(join_str)

        if self._where_conditions:
            conditions_str = " AND ".join(map(str, self._where_conditions))
            query_parts.append(f"WHERE {conditions_str}")

        if self._group_by_columns:
            group_by_str = ", ".join(map(str, self._group_by_columns))
            query_parts.append(f"GROUP BY {group_by_str}")

        if self._having_conditions:
            having_str = " AND ".join(map(str, self._having_conditions))
            query_parts.append(f"HAVING {having_str}")

        if self._order_by:
            order_by_str = ", ".join(
                [f"{col} {dir}" for col, dir in self._order_by])
            query_parts.append(f"ORDER BY {order_by_str}")

        if self._limit is not None:
            query_parts.append(f"LIMIT {self._limit}")

        if self._offset is not None:
            query_parts.append(f"OFFSET {self._offset}")

        return " ".join(query_parts)
