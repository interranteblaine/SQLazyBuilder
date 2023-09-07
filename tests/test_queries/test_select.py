import unittest
from src.sqlazybuilder.base import Table
from src.sqlazybuilder.queries.select import SelectQuery


class TestSelectQuery(unittest.TestCase):

    def setUp(self):
        self.users_table = Table("users")
        self.orders_table = Table("orders")
        self.user_id_col = self.users_table.column("user_id")
        self.order_user_id_col = self.orders_table.column("user_id")

    def test_basic_select(self):
        query = SelectQuery().select(self.user_id_col).from_table(self.users_table)
        self.assertEqual(str(query), "SELECT users.user_id FROM users")
        self.assertEqual(query.params, [])

    def test_select_without_from_raises_error(self):
        query = SelectQuery().select(self.user_id_col)
        with self.assertRaises(ValueError):
            str(query)

    def test_basic_select_with_multiple_columns(self):
        another_column = self.users_table.column("another_column")
        query = SelectQuery().select(
            self.user_id_col, another_column).from_table(self.users_table)
        self.assertEqual(
            str(query), "SELECT users.user_id, users.another_column FROM users")
        self.assertEqual(query.params, [])

    def test_select_with_distinct(self):
        query = SelectQuery().select(self.user_id_col).distinct().from_table(self.users_table)
        self.assertEqual(
            str(query), "SELECT DISTINCT users.user_id FROM users")
        self.assertEqual(query.params, [])

    def test_select_with_where(self):
        condition = self.user_id_col.eq("12345")
        query = SelectQuery().select(self.user_id_col).from_table(
            self.users_table).where(condition)
        self.assertEqual(
            str(query), "SELECT users.user_id FROM users WHERE users.user_id = %s")
        self.assertEqual(query.params, ["12345"])

    def test_select_with_inner_join(self):
        condition = self.user_id_col.eq(self.order_user_id_col)
        query = SelectQuery().select(self.user_id_col).from_table(
            self.users_table).inner_join(self.orders_table, condition)
        self.assertEqual(str(
            query), "SELECT users.user_id FROM users INNER JOIN orders ON users.user_id = orders.user_id")
        self.assertEqual(query.params, [])

    def test_complex_select(self):
        condition1 = self.user_id_col.eq("12345")
        condition2 = self.user_id_col.eq(self.order_user_id_col)
        query = (SelectQuery().select(self.user_id_col)
                 .distinct()
                 .from_table(self.users_table)
                 .where(condition1)
                 .inner_join(self.orders_table, condition2))
        expected_str = ("SELECT DISTINCT users.user_id FROM users INNER JOIN orders ON users.user_id = orders.user_id "
                        "WHERE users.user_id = %s")
        self.assertEqual(str(query), expected_str)
        self.assertEqual(query.params, ["12345"])

    def test_group_by_single_column(self):
        query = (SelectQuery().select(self.order_user_id_col)
                 .from_table(self.orders_table)
                 .group_by(self.order_user_id_col))
        expected_str = (
            "SELECT orders.user_id FROM orders GROUP BY orders.user_id")
        self.assertEqual(str(query), expected_str)
        self.assertEqual(query.params, [])

    def test_group_by_multiple_columns(self):
        orders_total_amount = self.orders_table.column("total_amount")
        query = (SelectQuery().select(self.order_user_id_col, orders_total_amount)
                 .from_table(self.orders_table)
                 .group_by(self.order_user_id_col, orders_total_amount))
        expected_str = (
            "SELECT orders.user_id, orders.total_amount FROM orders GROUP BY orders.user_id, orders.total_amount")
        self.assertEqual(str(query), expected_str)
        self.assertEqual(query.params, [])

    def test_group_by_count_all(self):
        query = (SelectQuery().select(self.order_user_id_col, self.orders_table.count_all())
                 .from_table(self.orders_table)
                 .group_by(self.order_user_id_col))
        expected_str = (
            "SELECT orders.user_id, COUNT(*) FROM orders GROUP BY orders.user_id")
        self.assertEqual(str(query), expected_str)
        self.assertEqual(query.params, [])

    def test_having_condition(self):
        total_amount_col = self.orders_table.column("total_amount")
        avg_amount = total_amount_col.avg()
        having_condition = avg_amount.gt(100)
        query = (SelectQuery().select(self.order_user_id_col, avg_amount)
                 .from_table(self.orders_table)
                 .group_by(self.order_user_id_col)
                 .having(having_condition))
        expected_str = ("SELECT orders.user_id, AVG(orders.total_amount) FROM orders "
                        "GROUP BY orders.user_id HAVING AVG(orders.total_amount) > %s")
        self.assertEqual(str(query), expected_str)
        self.assertEqual(query.params, [100])

    def test_order_by_single_column(self):
        query = (SelectQuery().select(self.order_user_id_col)
                 .from_table(self.orders_table)
                 .order_by(self.order_user_id_col, "DESC"))
        expected_str = "SELECT orders.user_id FROM orders ORDER BY orders.user_id DESC"
        self.assertEqual(str(query), expected_str)
        self.assertEqual(query.params, [])

    def test_order_by_multiple_columns(self):
        total_amount_col = self.orders_table.column("total_amount")
        query = (SelectQuery().select(self.order_user_id_col, total_amount_col)
                 .from_table(self.orders_table)
                 .order_by(self.order_user_id_col, "DESC")
                 .order_by(total_amount_col, "ASC"))
        expected_str = ("SELECT orders.user_id, orders.total_amount FROM orders "
                        "ORDER BY orders.user_id DESC, orders.total_amount ASC")
        self.assertEqual(str(query), expected_str)
        self.assertEqual(query.params, [])

    def test_limit(self):
        query = (SelectQuery().select(self.order_user_id_col)
                 .from_table(self.orders_table)
                 .limit(10))
        expected_str = "SELECT orders.user_id FROM orders LIMIT 10"
        self.assertEqual(str(query), expected_str)
        self.assertEqual(query.params, [])

    def test_offset(self):
        query = (SelectQuery().select(self.order_user_id_col)
                 .from_table(self.orders_table)
                 .offset(5))
        expected_str = "SELECT orders.user_id FROM orders OFFSET 5"
        self.assertEqual(str(query), expected_str)
        self.assertEqual(query.params, [])

    def test_limit_and_offset(self):
        query = (SelectQuery().select(self.order_user_id_col)
                 .from_table(self.orders_table)
                 .limit(10)
                 .offset(5))
        expected_str = "SELECT orders.user_id FROM orders LIMIT 10 OFFSET 5"
        self.assertEqual(str(query), expected_str)
        self.assertEqual(query.params, [])

    def test_clause_order(self):
        users_username_col = self.users_table.column("username")
        orders_total_amount_col = self.orders_table.column("total_amount")
        orders_date_col = self.orders_table.column("date")

        orders_avg_amount = orders_total_amount_col.avg()
        orders_count = self.orders_table.count_all()

        join_conditon = self.user_id_col.eq(self.order_user_id_col)
        where_conditon = orders_date_col.between("2023-08-01", "2023-08-31")
        having_conditon = orders_avg_amount.ge(100)

        query = (SelectQuery()
                 .select(self.user_id_col, users_username_col, orders_avg_amount, orders_count)
                 .from_table(self.users_table)
                 .inner_join(self.orders_table, join_conditon)
                 .where(where_conditon)
                 .group_by(self.user_id_col, users_username_col)
                 .having(having_conditon)
                 .order_by(orders_avg_amount, "DESC")
                 .limit(10)
                 .offset(5))

        expected_str = ("SELECT users.user_id, users.username, AVG(orders.total_amount), COUNT(*) "
                        "FROM users "
                        "INNER JOIN orders ON users.user_id = orders.user_id "
                        "WHERE orders.date BETWEEN %s AND %s "
                        "GROUP BY users.user_id, users.username "
                        "HAVING AVG(orders.total_amount) >= %s "
                        "ORDER BY AVG(orders.total_amount) DESC "
                        "LIMIT 10 "
                        "OFFSET 5")

        self.assertEqual(str(query), expected_str)
        self.assertEqual(query.params, ["2023-08-01", "2023-08-31", 100])

    def test_subquery_select_users_with_more_than_five_orders(self):
        subquery = (SelectQuery()
                    .select(self.order_user_id_col)
                    .from_table(self.orders_table)
                    .group_by(self.order_user_id_col)
                    .having(self.orders_table.count_all().gt(5)))

        condition = self.user_id_col.in_(subquery)
        query = (SelectQuery()
                 .select(self.users_table.column("email"))
                 .from_table(self.users_table)
                 .where(condition))

        expected_str = ("SELECT users.email FROM users "
                        "WHERE users.user_id IN ("
                        "SELECT orders.user_id FROM orders "
                        "GROUP BY orders.user_id "
                        "HAVING COUNT(*) > %s"
                        ")")
        self.assertEqual(str(query), expected_str)
        self.assertEqual(query.params, [5])


if __name__ == '__main__':
    unittest.main()
