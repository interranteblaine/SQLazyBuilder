from ..core.base import BaseQuery
from ..expressions.joins import InnerJoin, LeftJoin, RightJoin, FullJoin
from ..expressions.columns import Column


class SelectQuery(BaseQuery):
    def __init__(self, table_or_subquery, alias=None):
        self._table = table_or_subquery
        self.alias = alias
        self._columns = []
        self._conditions = []
        self._order_by = []
        self._limit = None
        self._offset = None
        self._joins = []
        self._group_by = []
        self._having_conditions = []

    def as_alias(self, alias_name):
        self.alias = alias_name
        return self

    def column(self, column_name):
        return Column(self.alias, column_name) if self.alias else Column(str(self._table), column_name)

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

    def inner_join(self, table_or_subquery, condition):
        self._joins.append(InnerJoin(table_or_subquery, condition))
        return self

    def left_join(self, table_or_subquery, condition):
        self._joins.append(LeftJoin(table_or_subquery, condition))
        return self

    def right_join(self, table_or_subquery, condition):
        self._joins.append(RightJoin(table_or_subquery, condition))
        return self

    def full_join(self, table_or_subquery, condition):
        self._joins.append(FullJoin(table_or_subquery, condition))
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

        # Check if the table is a subquery
        if isinstance(self._table, BaseQuery):
            if not self._table.alias:
                raise ValueError("Alias required for subquery in FROM clause.")
            subquery_sql, subquery_params = self._table.build()
            from_clause = f"FROM ({subquery_sql}) AS {self._table.alias}"
            params = subquery_params
        else:
            from_clause = f"FROM {self._table}"
            params = []

        query_parts = [select_clause, from_clause]

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
