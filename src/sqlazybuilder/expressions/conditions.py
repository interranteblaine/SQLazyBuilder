from abc import ABC, abstractmethod
from ..core.base import Expression


class Condition(Expression):
    def __init__(self, column, operator, value):
        self.column = column
        self.operator = operator
        self.value = value

        if self.operator in ["IN", "NOT IN"] and not isinstance(self.value, (list, tuple, Expression)):
            raise ValueError(
                "Values for 'IN' or 'NOT IN' condition must be in a list, tuple or an Expression.")

    def __str__(self):
        if isinstance(self.value, Expression):
            return f"{self.column} {self.operator} {self.value}"
        elif self.operator == "BETWEEN":
            return f"{self.column} {self.operator} %s AND %s"
        elif self.operator in ["IS", "IS NOT"] and self.value == "NULL":
            return f"{self.column} {self.operator} NULL"
        elif isinstance(self.value, (list, tuple)):
            placeholders = ", ".join(["%s"] * len(self.value))
            return f"{self.column} {self.operator} ({placeholders})"
        else:
            return f"{self.column} {self.operator} %s"

    @property
    def params(self):
        if isinstance(self.value, Expression):
            return self.value.params
        elif self.operator in ["IS", "IS NOT"] and self.value == "NULL":
            return []
        elif isinstance(self.value, (list, tuple)):
            return list(self.value)
        else:
            return [self.value]

    def __and__(self, other):
        return AndCondition(self, other)

    def __or__(self, other):
        return OrCondition(self, other)

    def __invert__(self):
        return NotCondition(self)


class CombinedCondition(Expression, ABC):
    def __init__(self, *conditions):
        self.conditions = conditions

    @abstractmethod
    def __str__(self):
        pass

    @property
    def params(self):
        params = []
        for condition in self.conditions:
            params.extend(condition.params)
        return params

    def __and__(self, other):
        return AndCondition(self, other)

    def __or__(self, other):
        return OrCondition(self, other)

    def __invert__(self):
        return NotCondition(self)


class AndCondition(CombinedCondition):
    def __str__(self):
        return "(" + " AND ".join(map(str, self.conditions)) + ")"


class OrCondition(CombinedCondition):
    def __str__(self):
        return "(" + " OR ".join(map(str, self.conditions)) + ")"


class NotCondition(Expression):
    def __init__(self, condition):
        self.condition = condition

    def __str__(self):
        return "NOT (" + str(self.condition) + ")"

    @property
    def params(self):
        return self.condition.params
