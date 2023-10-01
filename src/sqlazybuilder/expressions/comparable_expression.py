from src.sqlazybuilder.core.base import Expression
from src.sqlazybuilder.expressions.conditions import Condition


class ComparableExpression(Expression):
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

    def not_in(self, values):
        return Condition(self, "NOT IN", values)

    def like(self, pattern):
        return Condition(self, "LIKE", pattern)

    def not_like(self, pattern):
        return Condition(self, "NOT LIKE", pattern)

    def between(self, value1, value2):
        return Condition(self, "BETWEEN", (value1, value2))

    def is_null(self):
        return Condition(self, "IS", "NULL")

    def is_not_null(self):
        return Condition(self, "IS NOT", "NULL")
