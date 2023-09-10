from ..utils.factory import create_column


class Table:
    def __init__(self, name, alias=None):
        self.name = name
        self.alias = alias

    def __str__(self):
        table_representation = self.name
        if self.alias:
            table_representation += f" AS {self.alias}"
        return table_representation

    def column(self, column_name):
        return create_column(self, column_name)

    def as_alias(self, alias_name):
        self.alias = alias_name
        return self
