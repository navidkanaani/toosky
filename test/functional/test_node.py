import sqlite3
import unittest

from src.node import NodeManager
from src.environments import Env


class TestNodeManager(unittest.TestCase):

    rows_to_setup = [
        ("token-test-0001", "delete me 0", "hello"),
        ("token-test-0002", "delete me 1", "okay"),
        ("token-test-0003", "delete me 2", ""),
    ]

    rows_created_in_tests = []

    @classmethod
    def setUpClass(cls):
        Env._init_envs_(env_file_path='.env')
        cls.db_connection = sqlite3.connect(Env.TEST_DB_NAME)
        crs = cls.db_connection.cursor()
        cls.setup_table_records(cursor=crs)
        cls.db_connection.commit()

    @classmethod
    def setup_table_records(cls, cursor):
        cursor.executemany(
            f"INSERT INTO {Env.NODE_TABLE_NAME} VALUES (?, ?, ?);", cls.rows_to_setup
        )

    @classmethod
    def cleanup_table(cls, cursor):
        tokens = [(row[0],) for row in cls.rows_to_setup] + [(row[0],) for row in cls.rows_created_in_tests]
        cursor.executemany(
            f"DELETE FROM {Env.NODE_TABLE_NAME} WHERE token = (?);", tokens
        )

    @classmethod
    def tearDownClass(cls):
        cursor = cls.db_connection.cursor()
        cls.cleanup_table(cursor)
        cls.db_connection.commit()
        cls.db_connection.close()


    def test_get_node_01(self):
        node = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).get(node_id=1)
        self.assertEqual(node['node_name'], self.rows_to_setup[0][1])

    def test_get_node_02(self):
        node = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).get(node_id=2)
        self.assertEqual(node['node_name'], self.rows_to_setup[1][1])

    def test_get_node_03(self):
        node = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).get(node_id=3)
        self.assertEqual(node['node_name'], self.rows_to_setup[2][1])

    def test_create_node_01(self):
        row = (..., "Hello this row is created in test 01", "description")
        node_token = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).create(name=row[1], description="hello")
        row = (node_token, *row[1:])
        self.rows_created_in_tests.append(row)
        fetched_row = self.get_row(token=node_token)
        self.assertEqual(fetched_row[1], row[0])

    def test_create_node_02(self):
        row = (..., "Hello this row is created in test 02", "description")
        node_token = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).create(name=row[1], description="hello")
        row = (node_token, *row[1:])
        self.rows_created_in_tests.append(row)
        fetched_row = self.get_row(token=node_token)
        self.assertEqual(fetched_row[1], row[0])

    def test_create_node_03(self):
        row = (..., "Hello this row is created in test 03", "description")
        node_token = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).create(name=row[1], description="hello")
        row = (node_token, *row[1:])
        self.rows_created_in_tests.append(row)
        fetched_row = self.get_row(token=node_token)
        self.assertEqual(fetched_row[1], row[0])

    def get_row(self, token):
        cursor = self.db_connection.cursor()
        cursor.execute(
            f"SELECT rowid, * FROM {Env.NODE_TABLE_NAME} WHERE token = (?);", (token,)
        )
        return cursor.fetchone()
