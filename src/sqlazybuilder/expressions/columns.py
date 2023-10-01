from src.sqlazybuilder.expressions.comparable_expression import ComparableExpression


class Column(ComparableExpression):
    def __init__(self, table, name, alias=None):
        self.table = table
        self.name = name
        self.alias = alias

    def __str__(self):
        column_representation = f"{self.table}.{self.name}"
        if self.alias:
            column_representation += f" AS {self.alias}"
        return column_representation

    @property
    def params(self):
        return []

    def as_alias(self, alias_name):
        self.alias = alias_name
        return self
