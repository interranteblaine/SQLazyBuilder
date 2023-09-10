import unittest
from src.sqlazybuilder.core.table import Table
from src.sqlazybuilder.queries.select import SelectQuery


class TestSelectQuery(unittest.TestCase):
    def setUp(self):
        self.users = Table("users")
        self.username_col = self.users.column("username")
        self.age_col = self.users.column("age")

    def test_basic_select(self):
        query = SelectQuery(self.users).build()
        self.assertEqual(query, ("SELECT * FROM users", []))

    def test_select_columns(self):
        query = SelectQuery(self.users).select(
            self.username_col, self.age_col).build()
        self.assertEqual(
            query, ("SELECT users.username, users.age FROM users", []))

    def test_select_with_condition(self):
        query = SelectQuery(self.users).select(self.username_col).where(
            self.username_col.eq("John")).build()
        self.assertEqual(
            query, ("SELECT users.username FROM users WHERE users.username = %s", ["John"]))

    def test_select_with_multiple_conditions(self):
        query = SelectQuery(self.users).select(self.username_col).where(
            self.username_col.eq("John"), self.age_col.gt(25)).build()
        self.assertEqual(
            query, ("SELECT users.username FROM users WHERE users.username = %s AND users.age > %s", ["John", 25]))

    def test_order_by(self):
        query = SelectQuery(self.users).order_by(self.username_col).build()
        self.assertEqual(
            query, ("SELECT * FROM users ORDER BY users.username ASC", []))

        query = SelectQuery(self.users).order_by(
            self.username_col, "DESC").build()
        self.assertEqual(
            query, ("SELECT * FROM users ORDER BY users.username DESC", []))

        query = SelectQuery(self.users).order_by(
            self.username_col, "DESC").order_by(self.age_col).build()
        self.assertEqual(
            query, ("SELECT * FROM users ORDER BY users.username DESC, users.age ASC", []))

        with self.assertRaises(ValueError):
            SelectQuery(self.users).order_by(self.username_col, "INVALID")

    def test_limit(self):
        query = SelectQuery(self.users).limit(10).build()
        self.assertEqual(query, ("SELECT * FROM users LIMIT 10", []))

    def test_offset(self):
        query = SelectQuery(self.users).offset(5).build()
        self.assertEqual(query, ("SELECT * FROM users OFFSET 5", []))

    def test_limit_with_offset(self):
        query = SelectQuery(self.users).limit(10).offset(5).build()
        self.assertEqual(query, ("SELECT * FROM users LIMIT 10 OFFSET 5", []))

    def test_order_by_with_limit_and_offset(self):
        query = SelectQuery(self.users).order_by(
            self.age_col, "DESC").limit(10).offset(5).build()
        self.assertEqual(
            query, ("SELECT * FROM users ORDER BY users.age DESC LIMIT 10 OFFSET 5", []))


if __name__ == '__main__':
    unittest.main()
