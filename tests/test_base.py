import unittest
from src.sqlazybuilder.base import BaseQuery, Table
from src.sqlazybuilder.expressions import Column, Count


class TestBaseQuery(unittest.TestCase):
    def test_str_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            str(BaseQuery())


class TestTable(unittest.TestCase):
    def setUp(self):
        self.table = Table("test_table")

    def test_init(self):
        self.assertEqual(self.table.name, "test_table")

    def test_str(self):
        self.assertEqual(str(self.table), "test_table")

    def test_column(self):
        col = self.table.column("col_name")
        self.assertIsInstance(col, Column)
        self.assertEqual(str(col), "test_table.col_name")

    def test_count_all(self):
        count_all_expr = self.table.count_all()
        self.assertIsInstance(count_all_expr, Count)
        self.assertEqual(str(count_all_expr), "COUNT(*)")


if __name__ == '__main__':
    unittest.main()
