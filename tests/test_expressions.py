import unittest
from src.sqlazybuilder.base import Table
from src.sqlazybuilder.expressions import Condition, AndCondition, OrCondition


class TestColumn(unittest.TestCase):

    def setUp(self):
        self.table = Table("mock_table")
        self.column = self.table.column("name")

    def test_column_str(self):
        self.assertEqual(str(self.column), "mock_table.name")

    def test_condition_eq(self):
        condition = self.column.eq("John")
        self.assertEqual(str(condition), "mock_table.name = %s")
        self.assertEqual(condition.params, ["John"])

    def test_condition_eq_with_column(self):
        another_column = self.table.column("another_name")
        condition = self.column.eq(another_column)
        self.assertEqual(
            str(condition), "mock_table.name = mock_table.another_name")
        self.assertEqual(condition.params, [])

    def test_condition_ne(self):
        condition = self.column.ne("John")
        self.assertEqual(str(condition), "mock_table.name != %s")
        self.assertEqual(condition.params, ["John"])

    def test_condition_lt(self):
        condition = self.column.lt(10)
        self.assertEqual(str(condition), "mock_table.name < %s")
        self.assertEqual(condition.params, [10])

    def test_condition_gt(self):
        condition = self.column.gt(10)
        self.assertEqual(str(condition), "mock_table.name > %s")
        self.assertEqual(condition.params, [10])

    def test_condition_lte(self):
        condition = self.column.lte(10)
        self.assertEqual(str(condition), "mock_table.name <= %s")
        self.assertEqual(condition.params, [10])

    def test_condition_gte(self):
        condition = self.column.gte(10)
        self.assertEqual(str(condition), "mock_table.name >= %s")
        self.assertEqual(condition.params, [10])

    def test_condition_in(self):
        condition = self.column.in_([1, 2, 3])
        self.assertEqual(str(condition), "mock_table.name IN (%s, %s, %s)")
        self.assertEqual(condition.params, [1, 2, 3])

    def test_condition_like(self):
        condition = self.column.like("%John%")
        self.assertEqual(str(condition), "mock_table.name LIKE %s")
        self.assertEqual(condition.params, ["%John%"])

    def test_condition_between(self):
        condition = self.column.between(5, 10)
        self.assertEqual(str(condition), "mock_table.name BETWEEN %s AND %s")
        self.assertEqual(condition.params, [5, 10])

    def test_condition_is_null(self):
        condition = self.column.is_null()
        self.assertEqual(str(condition), "mock_table.name IS NULL")
        self.assertEqual(condition.params, [])

    def test_condition_is_not_null(self):
        condition = self.column.is_not_null()
        self.assertEqual(str(condition), "mock_table.name IS NOT NULL")
        self.assertEqual(condition.params, [])

    def test_aggregate_count(self):
        count = self.column.count()
        self.assertEqual(str(count), "COUNT(mock_table.name)")

    def test_aggregate_sum(self):
        sum_ = self.column.sum()
        self.assertEqual(str(sum_), "SUM(mock_table.name)")

    def test_aggregate_avg(self):
        avg = self.column.avg()
        self.assertEqual(str(avg), "AVG(mock_table.name)")

    def test_aggregate_min(self):
        min_ = self.column.min()
        self.assertEqual(str(min_), "MIN(mock_table.name)")

    def test_aggregate_max(self):
        max_ = self.column.max()
        self.assertEqual(str(max_), "MAX(mock_table.name)")

    def test_coalesce(self):
        coalesce = self.column.coalesce("Default", "Alternative")
        self.assertEqual(str(coalesce), "COALESCE(mock_table.name, %s, %s)")
        self.assertEqual(coalesce.build(), ("COALESCE(mock_table.name, %s, %s)", [
                         "Default", "Alternative"]))

    def test_coalesce_with_column(self):
        another_column = self.table.column("another_name")
        coalesce = self.column.coalesce(another_column, "Default")
        self.assertEqual(
            str(coalesce), "COALESCE(mock_table.name, mock_table.another_name, %s)")
        self.assertEqual(coalesce.build(
        ), ("COALESCE(mock_table.name, mock_table.another_name, %s)", ["Default"]))


class TestCondition(unittest.TestCase):

    def setUp(self):
        self.mock_column = Table("mock_table").column("mock_column")

    def test_condition_str_representation(self):
        condition = Condition(self.mock_column, "=", "value")
        self.assertEqual(str(condition), "mock_table.mock_column = %s")

    def test_condition_params(self):
        condition = Condition(self.mock_column, "=", "value")
        self.assertEqual(condition.params, ["value"])

    def test_condition_with_column(self):
        another_column = Table("another_table").column("another_name")
        condition = Condition(self.mock_column, "=", another_column)
        self.assertEqual(
            str(condition), "mock_table.mock_column = another_table.another_name")
        self.assertEqual(condition.params, [])

    def test_in_operator_single_value(self):
        with self.assertRaises(ValueError):
            condition = Condition(self.mock_column, "IN", "value")


class TestCombinedCondition(unittest.TestCase):

    def setUp(self):
        self.column1 = Table("mock_table1").column("column1")
        self.column2 = Table("mock_table2").column("column2")
        self.column3 = Table("mock_table3").column("column3")

    def test_and_condition_with_two_conditions(self):
        condition1 = self.column1.eq("value1")
        condition2 = self.column2.eq("value2")
        combined_condition = AndCondition(condition1, condition2)

        self.assertEqual(str(combined_condition),
                         "(mock_table1.column1 = %s AND mock_table2.column2 = %s)")
        self.assertEqual(combined_condition.params, ["value1", "value2"])

    def test_or_condition_with_two_conditions(self):
        condition1 = self.column1.eq("value1")
        condition2 = self.column2.eq("value2")
        combined_condition = OrCondition(condition1, condition2)

        self.assertEqual(str(combined_condition),
                         "(mock_table1.column1 = %s OR mock_table2.column2 = %s)")
        self.assertEqual(combined_condition.params, ["value1", "value2"])

    def test_and_condition_with_multiple_conditions(self):
        condition1 = self.column1.eq("value1")
        condition2 = self.column2.eq("value2")
        condition3 = self.column1.ne("value3")
        combined_condition = AndCondition(condition1, condition2, condition3)

        self.assertEqual(str(combined_condition),
                         "(mock_table1.column1 = %s AND mock_table2.column2 = %s AND mock_table1.column1 != %s)")
        self.assertEqual(combined_condition.params, [
                         "value1", "value2", "value3"])

    def test_or_condition_with_multiple_conditions(self):
        condition1 = self.column1.eq("value1")
        condition2 = self.column2.eq("value2")
        condition3 = self.column1.ne("value3")
        combined_condition = OrCondition(condition1, condition2, condition3)

        self.assertEqual(str(combined_condition),
                         "(mock_table1.column1 = %s OR mock_table2.column2 = %s OR mock_table1.column1 != %s)")
        self.assertEqual(combined_condition.params, [
                         "value1", "value2", "value3"])

    def test_combined_condition_with_columns(self):
        condition1 = self.column1.eq("value1")
        condition2 = self.column2.eq(self.column3)  # column2 equals column3
        combined_condition = AndCondition(condition1, condition2)

        self.assertEqual(str(combined_condition),
                         "(mock_table1.column1 = %s AND mock_table2.column2 = mock_table3.column3)")
        self.assertEqual(combined_condition.params, ["value1"])

    def test_nested_and_conditions(self):
        condition1 = self.column1.eq("value1")
        condition2 = self.column2.eq("value2")
        inner_combined = AndCondition(condition1, condition2)

        condition3 = self.column3.ne("value3")
        outer_combined = AndCondition(inner_combined, condition3)

        self.assertEqual(str(
            outer_combined), "((mock_table1.column1 = %s AND mock_table2.column2 = %s) AND mock_table3.column3 != %s)")
        self.assertEqual(outer_combined.params, ["value1", "value2", "value3"])

    def test_nested_or_conditions(self):
        condition1 = self.column1.eq("value1")
        condition2 = self.column2.eq("value2")
        inner_combined = OrCondition(condition1, condition2)

        condition3 = self.column3.ne("value3")
        outer_combined = OrCondition(inner_combined, condition3)

        self.assertEqual(str(
            outer_combined), "((mock_table1.column1 = %s OR mock_table2.column2 = %s) OR mock_table3.column3 != %s)")
        self.assertEqual(outer_combined.params, ["value1", "value2", "value3"])

    def test_mixed_nested_conditions(self):
        condition1 = self.column1.eq("value1")
        condition2 = self.column2.eq("value2")
        and_combined = AndCondition(condition1, condition2)

        condition3 = self.column3.ne("value3")
        or_combined = OrCondition(and_combined, condition3)

        self.assertEqual(str(
            or_combined), "((mock_table1.column1 = %s AND mock_table2.column2 = %s) OR mock_table3.column3 != %s)")
        self.assertEqual(or_combined.params, ["value1", "value2", "value3"])


if __name__ == '__main__':
    unittest.main()
