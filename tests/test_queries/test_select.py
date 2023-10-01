import unittest
from src.sqlazybuilder.core.table import Table
from src.sqlazybuilder.queries.select import SelectQuery
from src.sqlazybuilder.expressions.functions import CountAll


class TestSelectQuery(unittest.TestCase):
    def setUp(self):
        self.users = Table("users")
        self.username_col = self.users.column("username")
        self.age_col = self.users.column("age")

        self.orders = Table("orders")
        self.order_id_col = self.orders.column("order_id")
        self.user_id_col = self.orders.column("user_id")

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

    def test_inner_join(self):
        query = (SelectQuery(self.users)
                 .select(self.username_col)
                 .inner_join(self.orders, self.users.column("id").eq(self.user_id_col))
                 .build())
        self.assertEqual(
            query, ("SELECT users.username FROM users INNER JOIN orders ON users.id = orders.user_id", []))

    def test_left_join(self):
        query = (SelectQuery(self.users)
                 .select(self.username_col)
                 .left_join(self.orders, self.users.column("id").eq(self.user_id_col))
                 .build())
        self.assertEqual(
            query, ("SELECT users.username FROM users LEFT JOIN orders ON users.id = orders.user_id", []))

    def test_right_join(self):
        query = (SelectQuery(self.users)
                 .select(self.username_col)
                 .right_join(self.orders, self.users.column("id").eq(self.user_id_col))
                 .build())
        self.assertEqual(
            query, ("SELECT users.username FROM users RIGHT JOIN orders ON users.id = orders.user_id", []))

    def test_full_join(self):
        query = (SelectQuery(self.users)
                 .select(self.username_col)
                 .full_join(self.orders, self.users.column("id").eq(self.user_id_col))
                 .build())
        self.assertEqual(
            query, ("SELECT users.username FROM users FULL JOIN orders ON users.id = orders.user_id", []))

    def test_join_with_conditions(self):
        query = (SelectQuery(self.users)
                 .select(self.username_col)
                 .inner_join(self.orders, self.users.column("id").eq(self.user_id_col))
                 .where(self.username_col.eq("John"))
                 .build())
        self.assertEqual(
            query, ("SELECT users.username FROM users INNER JOIN orders ON users.id = orders.user_id WHERE users.username = %s", ["John"]))

    def test_group_by(self):
        query = (SelectQuery(self.users)
                 .select(self.age_col, CountAll())
                 .group_by(self.age_col)
                 .build())
        self.assertEqual(
            query, ("SELECT users.age, COUNT(*) FROM users GROUP BY users.age", []))

    def test_group_by_with_conditions(self):
        query = (SelectQuery(self.users)
                 .select(self.age_col, CountAll())
                 .where(self.age_col.gt(20))
                 .group_by(self.age_col)
                 .build())
        self.assertEqual(
            query, ("SELECT users.age, COUNT(*) FROM users WHERE users.age > %s GROUP BY users.age", [20]))

    def test_having(self):
        query = (SelectQuery(self.users)
                 .select(self.age_col, CountAll())
                 .group_by(self.age_col)
                 .having(CountAll().gt(5))
                 .build())
        self.assertEqual(
            query, ("SELECT users.age, COUNT(*) FROM users GROUP BY users.age HAVING COUNT(*) > %s", [5]))


if __name__ == '__main__':
    unittest.main()
