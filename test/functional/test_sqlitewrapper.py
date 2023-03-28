import unittest

from src.db.sqlite import SQLiteWrapper


class TestSQLiteWrapper(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(cls): ...

    def test_make_insert_query_01(self):
        query = SQLiteWrapper._make_insert_query("name", "body", "head", table="Data")
        self.assertEqual(query, "INSERT INTO Data VALUES (?, ?, ?);")

    def test_make_insert_query_02(self):
        query = SQLiteWrapper._make_insert_query("name", table="Data")
        self.assertEqual(query, "INSERT INTO Data VALUES (?);")
