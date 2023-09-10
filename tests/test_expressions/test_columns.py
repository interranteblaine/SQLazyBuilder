import unittest
from src.sqlazybuilder.expressions.columns import Column


class TestColumn(unittest.TestCase):

    def setUp(self):
        self.username_col = Column("users", "username")
        self.username = "John"
        self.age_col = Column("users", "age")
        self.age = 21

    def test_str(self):
        self.assertEqual(str(self.username_col), "users.username")

    def test_params(self):
        self.assertEqual(self.username_col.params, [])

    def test_eq(self):
        condition = self.username_col.eq(self.username)
        self.assertEqual(str(condition), "users.username = %s")
        self.assertEqual(condition.params, [self.username])

    def test_ne(self):
        condition = self.username_col.ne(self.username)
        self.assertEqual(str(condition), "users.username != %s")
        self.assertEqual(condition.params, [self.username])

    def test_lt(self):
        condition = self.age_col.lt(self.age)
        self.assertEqual(str(condition), "users.age < %s")
        self.assertEqual(condition.params, [self.age])

    def test_gt(self):
        condition = self.age_col.gt(self.age)
        self.assertEqual(str(condition), "users.age > %s")
        self.assertEqual(condition.params, [self.age])

    def test_lte(self):
        condition = self.age_col.lte(self.age)
        self.assertEqual(str(condition), "users.age <= %s")
        self.assertEqual(condition.params, [self.age])

    def test_gte(self):
        condition = self.age_col.gte(self.age)
        self.assertEqual(str(condition), "users.age >= %s")
        self.assertEqual(condition.params, [self.age])

    def test_in(self):
        condition = self.username_col.in_([self.username, "Ally", "Douglas"])
        self.assertEqual(str(condition), "users.username IN (%s, %s, %s)")
        self.assertEqual(condition.params, [self.username, "Ally", "Douglas"])

    def test_not_in(self):
        condition = self.username_col.not_in(
            [self.username, "Ally", "Douglas"])
        self.assertEqual(str(condition), "users.username NOT IN (%s, %s, %s)")
        self.assertEqual(condition.params, [self.username, "Ally", "Douglas"])

    def test_like(self):
        pattern = f"%{self.username}%"
        condition = self.username_col.like(pattern)
        self.assertEqual(str(condition), "users.username LIKE %s")
        self.assertEqual(condition.params, [pattern])

    def test_not_like(self):
        pattern = f"%{self.username}%"
        condition = self.username_col.not_like(pattern)
        self.assertEqual(str(condition), "users.username NOT LIKE %s")
        self.assertEqual(condition.params, [pattern])

    def test_between(self):
        condition = self.age_col.between(20, 22)
        self.assertEqual(str(condition), "users.age BETWEEN %s AND %s")
        self.assertEqual(condition.params, [20, 22])

    def test_is_null(self):
        condition = self.username_col.is_null()
        self.assertEqual(str(condition), "users.username IS NULL")
        self.assertEqual(condition.params, [])

    def test_is_not_null(self):
        condition = self.username_col.is_not_null()
        self.assertEqual(str(condition), "users.username IS NOT NULL")
        self.assertEqual(condition.params, [])

    def test_alias(self):
        user = self.username_col.as_alias("user")
        email = Column("users", "email_address", "email")
        self.assertEqual(str(user), "users.username AS user")
        self.assertEqual(str(email), "users.email_address AS email")


if __name__ == '__main__':
    unittest.main()
