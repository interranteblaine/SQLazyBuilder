import unittest
from src.sqlazybuilder.expressions.columns import Column
from src.sqlazybuilder.expressions.functions import Coalesce, Cast, CountDistinct, Substring, Count, CountAll, Sum, Avg, Max, Min


class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.column = Column("users", "username")
        self.age_column = Column("users", "age")

    def test_count(self):
        function = Count(self.age_column)
        self.assertEqual(str(function), "COUNT(users.age)")
        self.assertEqual(function.params, [])

    def test_count_all(self):
        function = CountAll()
        self.assertEqual(str(function), "COUNT(*)")
        self.assertEqual(function.params, [])

    def test_sum(self):
        function = Sum(self.age_column)
        self.assertEqual(str(function), "SUM(users.age)")
        self.assertEqual(function.params, [])

    def test_avg(self):
        function = Avg(self.age_column)
        self.assertEqual(str(function), "AVG(users.age)")
        self.assertEqual(function.params, [])

    def test_min(self):
        function = Min(self.age_column)
        self.assertEqual(str(function), "MIN(users.age)")
        self.assertEqual(function.params, [])

    def test_max(self):
        function = Max(self.age_column)
        self.assertEqual(str(function), "MAX(users.age)")
        self.assertEqual(function.params, [])

    def test_coalesce(self):
        function = Coalesce(self.column, "Unknown")
        self.assertEqual(str(function), "COALESCE(users.username, %s)")
        self.assertEqual(function.params, ["Unknown"])

    def test_cast(self):
        function = Cast(self.column, "TEXT")
        self.assertEqual(str(function), "CAST(users.username AS TEXT)")
        self.assertEqual(function.params, [])

        function = Cast("5", "INT")
        self.assertEqual(str(function), "CAST(%s AS INT)")
        self.assertEqual(function.params, ["5"])

    def test_count_distinct(self):
        function = CountDistinct(self.column)
        self.assertEqual(str(function), "COUNT(DISTINCT users.username)")
        self.assertEqual(function.params, [])

    def test_count_distinct_non_expression(self):
        function = CountDistinct("username")
        self.assertEqual(str(function), "COUNT(DISTINCT %s)")
        self.assertEqual(function.params, ["username"])

    def test_substring(self):
        function = Substring(self.column, 1)
        self.assertEqual(str(function), "SUBSTRING(users.username, %s)")
        self.assertEqual(function.params, [1])

        function = Substring(self.column, 1, 5)
        self.assertEqual(str(function), "SUBSTRING(users.username, %s, %s)")
        self.assertEqual(function.params, [1, 5])

    def test_nested_functons(self):
        discounted_price = Column("products", "discounted_price")
        price = Column("products", "price")
        coalesce_func = Coalesce(discounted_price, price)
        cast_func = Cast(coalesce_func, "FLOAT")
        avg_func = Avg(cast_func)
        self.assertEqual(str(
            avg_func), "AVG(CAST(COALESCE(products.discounted_price, products.price) AS FLOAT))")
        self.assertEqual(avg_func.params, [])


if __name__ == '__main__':
    unittest.main()
