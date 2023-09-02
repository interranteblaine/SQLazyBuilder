class JoinClause:
    def __init__(self, join_type, table, *conditions):
        self.join_type = join_type
        self.table = table
        self.conditions = conditions

        if not conditions:
            raise ValueError(
                "At least one condition must be provided for a join clause.")

    def __str__(self):
        conditions_str = " AND ".join(map(str, self.conditions))
        return f"{self.join_type} {self.table} ON {conditions_str}"

    @property
    def params(self):
        parameters = []
        for condition in self.conditions:
            parameters.extend(condition.params)
        return parameters
