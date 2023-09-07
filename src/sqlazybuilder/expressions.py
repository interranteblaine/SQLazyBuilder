from .registry import is_registered_query_class


class Column:
    def __init__(self, table, name):
        self.table = table
        self.name = name

    def __str__(self):
        return f"{self.table}.{self.name}"

    def eq(self, value):
        return Condition(self, "=", value)

    def ne(self, value):
        return Condition(self, "!=", value)

    def lt(self, value):
        return Condition(self, "<", value)

    def gt(self, value):
        return Condition(self, ">", value)

    def lte(self, value):
        return Condition(self, "<=", value)

    def gte(self, value):
        return Condition(self, ">=", value)

    def in_(self, values):
        return Condition(self, "IN", values)

    def like(self, pattern):
        return Condition(self, "LIKE", pattern)

    def between(self, value1, value2):
        return Condition(self, "BETWEEN", (value1, value2))

    def is_null(self):
        return Condition(self, "IS", "NULL")

    def is_not_null(self):
        return Condition(self, "IS NOT", "NULL")

    def count(self, distinct=False):
        return Count(self, distinct=distinct)

    def sum(self, distinct=False):
        return Sum(self, distinct=distinct)

    def avg(self, distinct=False):
        return Avg(self, distinct=distinct)

    def min(self, distinct=False):
        return Min(self, distinct=distinct)

    def max(self, distinct=False):
        return Max(self, distinct=distinct)

    def coalesce(self, *values):
        return Coalesce(self, *values)


class Condition:
    def __init__(self, column, operator, value):
        self.column = column
        self.operator = operator
        self.value = value

        if self.operator == "IN" and not isinstance(self.value, (list, tuple)) and not is_registered_query_class(self.value):
            raise ValueError(
                "Values for 'IN' condition must be in a list, tuple or a sub query.")

    def __str__(self):
        if isinstance(self.value, Column):
            return f"{self.column} {self.operator} {self.value}"
        elif self.operator == "BETWEEN":
            return f"{self.column} {self.operator} %s AND %s"
        elif self.operator in ["IS", "IS NOT"] and self.value == "NULL":
            return f"{self.column} {self.operator} NULL"
        elif isinstance(self.value, (list, tuple)):
            placeholders = ", ".join(["%s"] * len(self.value))
            return f"{self.column} {self.operator} ({placeholders})"
        elif is_registered_query_class(self.value):
            subquery_str, _ = self.value.build()
            return f"{self.column} {self.operator} ({subquery_str})"
        else:
            return f"{self.column} {self.operator} %s"

    @property
    def params(self):
        if isinstance(self.value, Column):
            return []
        elif self.operator in ["IS", "IS NOT"] and self.value == "NULL":
            return []
        elif isinstance(self.value, (list, tuple)):
            return list(self.value)
        elif is_registered_query_class(self.value):
            _, subquery_params = self.value.build()
            return subquery_params
        else:
            return [self.value]


class CombinedCondition(Condition):
    """
    Represents a combined condition (e.g., combining multiple conditions with AND/OR).

    This class inherits from Condition primarily for polymorphism, allowing both simple
    and combined conditions to be treated interchangeably. However, unlike simple conditions,
    it doesn't utilize attributes like `column`, `operator`, or `value`. Instead, it focuses
    on combining other Condition (or CombinedCondition) instances.
    """

    def __init__(self, *conditions):
        self.conditions = conditions

    @property
    def params(self):
        parameters = []
        for condition in self.conditions:
            parameters.extend(condition.params)
        return parameters


class AndCondition(CombinedCondition):
    def __str__(self):
        return "(" + " AND ".join(map(str, self.conditions)) + ")"


class OrCondition(CombinedCondition):
    def __str__(self):
        return "(" + " OR ".join(map(str, self.conditions)) + ")"


class AggregateFunction:
    def __init__(self, column, distinct=False):
        self.column = column
        self.distinct = distinct

    def __str__(self):
        distinct_str = "DISTINCT " if self.distinct else ""
        return f"{self.FUNC_NAME}({distinct_str}{self.column})"

    def eq(self, value):
        return Condition(self, "=", value)

    def ne(self, value):
        return Condition(self, "!=", value)

    def gt(self, value):
        return Condition(self, ">", value)

    def ge(self, value):
        return Condition(self, ">=", value)

    def lt(self, value):
        return Condition(self, "<", value)

    def le(self, value):
        return Condition(self, "<=", value)


class Count(AggregateFunction):
    FUNC_NAME = "COUNT"

    def __init__(self, column, all=False, distinct=False):
        super().__init__(column, distinct=distinct)
        self.all = all

    def __str__(self):
        if self.all:
            return "COUNT(*)"
        return super().__str__()


class Sum(AggregateFunction):
    FUNC_NAME = "SUM"


class Avg(AggregateFunction):
    FUNC_NAME = "AVG"


class Min(AggregateFunction):
    FUNC_NAME = "MIN"


class Max(AggregateFunction):
    FUNC_NAME = "MAX"


class Coalesce:
    def __init__(self, *values):
        self.values = values

    def __str__(self):
        query_string, _ = self.build()
        return query_string

    def build(self):
        # Distinguish between column references and static values
        query_parts = []
        params = []
        for value in self.values:
            if isinstance(value, Column):
                query_parts.append(str(value))
            else:
                query_parts.append("%s")
                params.append(value)

        query_string = f"COALESCE({', '.join(query_parts)})"
        return query_string, params
