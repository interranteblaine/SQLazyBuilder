from ..base import BaseQuery
from ..joins import JoinClause


class SelectQuery(BaseQuery):
    def __init__(self):
        super().__init__()
        self._columns = []
        self._from_table = None
        self._distinct = False
        # Placeholders for future methods
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

    @property
    def params(self):
        parameters = []

        for condition in self._where_conditions:
            parameters.extend(condition.params)

        for join_clause in self._joins:
            parameters.extend(join_clause.params)

        return parameters

    def build(self):
        return str(self), self.params

    def __str__(self):
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

        return " ".join(query_parts)
