from ..expressions.columns import Column


def create_column(table, column_name):
    return Column(table, column_name)
