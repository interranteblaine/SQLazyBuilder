import unittest
from src.sqlazybuilder.expressions.columns import Column
from src.sqlazybuilder.expressions.conditions import Condition, AndCondition, OrCondition, NotCondition


class TestCondition(unittest.TestCase):

    def setUp(self):
        self.username_col = Column("users", "username")
        self.age_col = Column("users", "age")

    def test_str_simple_condition(self):
        condition = Condition(self.username_col, "=", "John")
        self.assertEqual(str(condition), "users.username = %s")

    def test_str_expression_value(self):
        other_column = Column("users", "other_username")
        condition = Condition(self.username_col, "=", other_column)
        self.assertEqual(
            str(condition), "users.username = users.other_username")

    def test_params_simple_condition(self):
        condition = Condition(self.username_col, "=", "John")
        self.assertEqual(condition.params, ["John"])

    def test_and_combination(self):
        condition1 = Condition(self.username_col, "=", "John")
        condition2 = Condition(self.age_col, ">", 25)
        combined = condition1 & condition2
        self.assertEqual(
            str(combined), "(users.username = %s AND users.age > %s)")
        self.assertEqual(combined.params, ["John", 25])

    def test_or_combination(self):
        condition1 = Condition(self.username_col, "=", "John")
        condition2 = Condition(self.age_col, ">", 25)
        combined = condition1 | condition2
        self.assertEqual(
            str(combined), "(users.username = %s OR users.age > %s)")
        self.assertEqual(combined.params, ["John", 25])

    def test_not_condition(self):
        condition = Condition(self.username_col, "=", "John")
        negated = ~condition
        self.assertEqual(str(negated), "NOT (users.username = %s)")
        self.assertEqual(negated.params, ["John"])

    def test_combined_conditon(self):
        condition1 = Condition(self.username_col, "=", "John")
        condition2 = Condition(self.username_col, "=", "Jane")
        condition3 = Condition(self.age_col, ">", 25)
        condition4 = ~(Condition(self.age_col, ">", 20))

        username_combined = condition1 | condition2
        age_combined = condition3 | condition4

        final_combined = username_combined & age_combined

        self.assertEqual(str(final_combined),
                         "((users.username = %s OR users.username = %s) AND "
                         "(users.age > %s OR NOT (users.age > %s)))")
        self.assertEqual(final_combined.params, ["John", "Jane", 25, 20])

    def test_between_condition(self):
        condition = Condition(self.age_col, "BETWEEN", (20, 30))
        self.assertEqual(str(condition), "users.age BETWEEN %s AND %s")
        self.assertEqual(condition.params, [20, 30])

    def test_in_condition_with_non_expression(self):
        with self.assertRaises(ValueError):
            Condition(self.username_col, "IN", "John")

    def test_not_in_condition_with_non_expression(self):
        with self.assertRaises(ValueError):
            Condition(self.username_col, "NOT IN", "John")


if __name__ == '__main__':
    unittest.main()
