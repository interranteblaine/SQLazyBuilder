import unittest
from src.sqlazybuilder.base import Table
from src.sqlazybuilder.joins import JoinClause
from src.sqlazybuilder.expressions import OrCondition, AndCondition


class TestJoinClause(unittest.TestCase):

    def setUp(self):
        self.table1 = Table("users")
        self.table2 = Table("orders")
        self.column1 = self.table1.column("user_id")
        self.column2 = self.table2.column("user_id")
        self.column3 = self.table1.column("status")
        self.column4 = self.table2.column("order_date")

    def test_inner_join_single_condition(self):
        condition = self.column1.eq(self.column2)
        join_clause = JoinClause("INNER JOIN", self.table2, condition)

        self.assertEqual(str(join_clause),
                         "INNER JOIN orders ON users.user_id = orders.user_id")
        self.assertEqual(join_clause.params, [])

    def test_left_join_single_condition(self):
        condition = self.column1.eq(self.column2)
        join_clause = JoinClause("LEFT JOIN", self.table2, condition)

        self.assertEqual(str(join_clause),
                         "LEFT JOIN orders ON users.user_id = orders.user_id")
        self.assertEqual(join_clause.params, [])

    def test_inner_join_multiple_conditions(self):
        condition1 = self.column1.eq(self.column2)
        condition2 = self.table1.column("status").eq("active")
        join_clause = JoinClause(
            "INNER JOIN", self.table2, condition1, condition2)

        self.assertEqual(str(
            join_clause), "INNER JOIN orders ON users.user_id = orders.user_id AND users.status = %s")
        self.assertEqual(join_clause.params, ["active"])

    def test_left_join_multiple_conditions(self):
        condition1 = self.column1.eq(self.column2)
        condition2 = self.table1.column("status").eq("active")
        join_clause = JoinClause(
            "LEFT JOIN", self.table2, condition1, condition2)

        self.assertEqual(str(
            join_clause), "LEFT JOIN orders ON users.user_id = orders.user_id AND users.status = %s")
        self.assertEqual(join_clause.params, ["active"])

    def test_join_with_no_conditions(self):
        with self.assertRaises(ValueError):
            join_clause = JoinClause("INNER JOIN", self.table2)

    def test_join_with_nested_conditions(self):
        condition1 = self.column1.eq(self.column2)
        condition2 = self.column3.eq("active")
        condition3 = self.column4.ne("2023-01-01")

        and_condition = AndCondition(condition1, condition2)
        or_condition = OrCondition(and_condition, condition3)

        join_clause = JoinClause("INNER JOIN", self.table2, or_condition)

        expected_str = ("INNER JOIN orders ON "
                        "((users.user_id = orders.user_id AND users.status = %s) "
                        "OR orders.order_date != %s)")
        self.assertEqual(str(join_clause), expected_str)
        self.assertEqual(join_clause.params, ["active", "2023-01-01"])


if __name__ == '__main__':
    unittest.main()
