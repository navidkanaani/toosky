import sqlite3
import unittest

from src.node import NodeManager
from src.environments import Env


class TestNodeManager(unittest.TestCase):

    rows_to_setup = [
        ("delete me 0",),
        ("delete me 1",),
        ("delete me 2",),
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
            f"INSERT INTO {Env.NODE_TABLE_NAME} VALUES (?);", cls.rows_to_setup
        )

    @classmethod
    def cleanup_table(cls, cursor):
        cursor.executemany(
            f"DELETE FROM {Env.NODE_TABLE_NAME} WHERE node_name = (?);", cls.rows_to_setup + cls.rows_created_in_tests
        )

    @classmethod
    def tearDownClass(cls):
        cursor = cls.db_connection.cursor()
        cls.cleanup_table(cursor)
        cls.db_connection.commit()
        cls.db_connection.close()


    def test_get_node_01(self):
        node = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).get(node_id=1)
        self.assertEqual(node['node_name'], self.rows_to_setup[0][0])

    def test_get_node_02(self):
        node = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).get(node_id=2)
        self.assertEqual(node['node_name'], self.rows_to_setup[1][0])

    def test_get_node_03(self):
        node = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).get(node_id=3)
        self.assertEqual(node['node_name'], self.rows_to_setup[2][0])

    def test_create_node_01(self):
        row = ("Hello this row is created in test 01",)
        self.rows_created_in_tests.append(row)
        node_id = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).create(name=row[0])
        fetched_row = self.get_row(id_=node_id)
        self.assertEqual(fetched_row[1], row[0])

    def test_create_node_02(self):
        row = ("Hello this row is created in test 02",)
        self.rows_created_in_tests.append(row)
        node_id = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).create(name=row[0])
        fetched_row = self.get_row(id_=node_id)
        self.assertEqual(fetched_row[1], row[0])

    def test_create_node_03(self):
        row = ("Hello this row is created in test 03",)
        self.rows_created_in_tests.append(row)
        node_id = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).create(name=row[0])
        fetched_row = self.get_row(id_=node_id)
        self.assertEqual(fetched_row[1], row[0])

    def get_row(self, id_):
        cursor = self.db_connection.cursor()
        cursor.execute(
            f"SELECT rowid, * FROM {Env.NODE_TABLE_NAME} WHERE rowid = (?);", (id_,)
        )
        return cursor.fetchone()
