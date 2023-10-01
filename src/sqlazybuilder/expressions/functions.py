from src.sqlazybuilder.core.base import Expression
from src.sqlazybuilder.expressions.comparable_expression import ComparableExpression


class Function(ComparableExpression):
    def __init__(self, function_name, *args):
        self.function_name = function_name
        self.args = args
        self.alias = None

    def __str__(self):
        arguments = ', '.join([str(arg) if isinstance(
            arg, Expression) else "%s" for arg in self.args])
        function_representation = f"{self.function_name}({arguments})"
        if self.alias:
            function_representation += f" AS {self.alias}"
        return function_representation

    def as_alias(self, alias_name):
        self.alias = alias_name
        return self

    @property
    def params(self):
        params = []
        for arg in self.args:
            if isinstance(arg, Expression):
                params.extend(arg.params)
            else:
                params.append(arg)
        return params


class Count(Function):
    def __init__(self, *args):
        super().__init__("COUNT", *args)


class CountAll(Function):
    def __init__(self):
        pass

    def __str__(self):
        return "COUNT(*)"

    @property
    def params(self):
        return []


class Sum(Function):
    def __init__(self, *args):
        super().__init__("SUM", *args)


class Avg(Function):
    def __init__(self, *args):
        super().__init__("AVG", *args)


class Min(Function):
    def __init__(self, *args):
        super().__init__("MIN", *args)


class Max(Function):
    def __init__(self, *args):
        super().__init__("MAX", *args)


class Coalesce(Function):
    def __init__(self, *args):
        super().__init__("COALESCE", *args)


class Cast(Function):
    def __init__(self, expression, data_type):
        self.expression = expression
        self.data_type = data_type

    def __str__(self):
        expression_str = str(self.expression) if isinstance(
            self.expression, Expression) else "%s"
        return f"CAST({expression_str} AS {self.data_type})"

    @property
    def params(self):
        if isinstance(self.expression, Expression):
            return self.expression.params
        return [self.expression]


class CountDistinct(Function):
    def __init__(self, column):
        self.column = column

    def __str__(self):
        column_str = str(self.column) if isinstance(
            self.column, Expression) else "%s"
        return f"COUNT(DISTINCT {column_str})"

    @property
    def params(self):
        if isinstance(self.column, Expression):
            return self.column.params
        return [self.column]


class Substring(Function):
    def __init__(self, column, start, length=None):
        if length:
            super().__init__("SUBSTRING", column, start, length)
        else:
            super().__init__("SUBSTRING", column, start)
