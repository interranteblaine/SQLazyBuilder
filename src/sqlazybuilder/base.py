from .expressions import Column, Count


class BaseQuery:
    def __str__(self):
        raise NotImplementedError

    def build(self):
        return str(self)


class Table:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def column(self, column_name):
        return Column(self, column_name)

    def count_all(self):
        return Count(self, all=True)
