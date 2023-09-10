import unittest
from src.sqlazybuilder.core.table import Table
from src.sqlazybuilder.expressions.columns import Column


class TestTable(unittest.TestCase):

    def setUp(self):
        self.table = Table("users")

    def test_table_initialization(self):
        self.assertEqual(self.table.name, "users")

    def test_table_string_representation(self):
        self.assertEqual(str(self.table), "users")

    def test_table_column_creation(self):
        column = self.table.column("username")
        self.assertIsInstance(column, Column)
        self.assertEqual(str(column), "users.username")

    def test_alias(self):
        orders = Table("orders", "myOrders")
        users = self.table.as_alias("myUsers")
        self.assertEqual(str(orders), "orders AS myOrders")
        self.assertEqual(str(users), "users AS myUsers")


if __name__ == '__main__':
    unittest.main()
