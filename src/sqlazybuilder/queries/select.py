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
        self._group_by = []
        self._having_conditions = []

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

    def group_by(self, *columns):
        self._group_by.extend(columns)
        return self

    def having(self, *conditions):
        self._having_conditions.extend(conditions)
        return self

    def build(self):
        if not self._columns:
            select_clause = "SELECT *"
        else:
            select_clause = f"SELECT {', '.join(map(str, self._columns))}"

        from_clause = f"FROM {self._table}"

        query_parts = [select_clause, from_clause]
        params = []

        join_clause = " ".join([str(join) for join in self._joins])
        if join_clause:
            query_parts.append(join_clause)
            for join in self._joins:
                params.extend(join.params)

        if self._conditions:
            conditions_str = " AND ".join(map(str, self._conditions))
            where_clause = f"WHERE {conditions_str}"
            query_parts.append(where_clause)
            for condition in self._conditions:
                params.extend(condition.params)

        if self._group_by:
            group_by_str = ", ".join(map(str, self._group_by))
            group_by_clause = f"GROUP BY {group_by_str}"
            query_parts.append(group_by_clause)

        if self._having_conditions:
            having_str = " AND ".join(map(str, self._having_conditions))
            having_clause = f"HAVING {having_str}"
            query_parts.append(having_clause)
            for condition in self._having_conditions:
                params.extend(condition.params)

        if self._order_by:
            order_by_str = ", ".join(
                [f"{col} {dir}" for col, dir in self._order_by])
            order_clause = f"ORDER BY {order_by_str}"
            query_parts.append(order_clause)

        if self._limit:
            limit_clause = f"LIMIT {self._limit}"
            query_parts.append(limit_clause)

        if self._offset:
            offset_clause = f"OFFSET {self._offset}"
            query_parts.append(offset_clause)

        query = " ".join(query_parts)

        return query, params
