from ..core.base import BaseQuery
from ..expressions.joins import InnerJoin, LeftJoin, RightJoin, FullJoin


class SelectQuery(BaseQuery):
    def __init__(self, table):
        self._table = table
        self._columns = []
        self._conditions = []
        self._order_by = []
        self._limit = None
        self._offset = None
        self._joins = []

    def select(self, *columns):
        self._columns.extend(columns)
        return self

    def where(self, *conditions):
        self._conditions.extend(conditions)
        return self

    def order_by(self, column, direction="ASC"):
        if direction.upper() not in ['ASC', 'DESC']:
            raise ValueError("Order direction must be 'ASC' or 'DESC'")
        self._order_by.append((str(column), direction.upper()))
        return self

    def limit(self, limit):
        self._limit = limit
        return self

    def offset(self, offset):
        self._offset = offset
        return self

    def inner_join(self, table, condition):
        self._joins.append(InnerJoin(table, condition))
        return self

    def left_join(self, table, condition):
        self._joins.append(LeftJoin(table, condition))
        return self

    def right_join(self, table, condition):
        self._joins.append(RightJoin(table, condition))
        return self

    def full_join(self, table, condition):
        self._joins.append(FullJoin(table, condition))
        return self

    def build(self):
        if not self._columns:
            select_clause = "SELECT *"
        else:
            select_clause = f"SELECT {', '.join(map(str, self._columns))}"

        from_clause = f"FROM {self._table}"

        join_clause = " ".join([str(join) for join in self._joins])

        where_clause = ""
        if self._conditions:
            conditions_str = " AND ".join(map(str, self._conditions))
            where_clause = f"WHERE {conditions_str}"

        order_clause = ""
        if self._order_by:
            order_by_str = ", ".join(
                [f"{col} {dir}" for col, dir in self._order_by])
            order_clause = f"ORDER BY {order_by_str}"

        limit_clause = ""
        if self._limit:
            limit_clause = f"LIMIT {self._limit}"

        offset_clause = ""
        if self._offset:
            offset_clause = f"OFFSET {self._offset}"

        query_parts = [select_clause, from_clause]

        if join_clause:
            query_parts.append(join_clause)
        if where_clause:
            query_parts.append(where_clause)
        if order_clause:
            query_parts.append(order_clause)
        if limit_clause:
            query_parts.append(limit_clause)
        if offset_clause:
            query_parts.append(offset_clause)

        query = " ".join(query_parts)

        params = []
        for condition in self._conditions:
            params.extend(condition.params)
        for join in self._joins:
            params.extend(join.params)

        return query, params
