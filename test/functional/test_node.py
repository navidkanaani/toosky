import sqlite3
import unittest

from src.node import NodeManager
from src.environments import Env


class TestNodeManager(unittest.TestCase):

    rows_to_setup = [
        # (eid, name, description, parent_eid, rule_eid, level)
        ("eid-test-0001", "delete me 0", "hello", None, None, None),
        ("eid-test-0002", "delete me 1", "okay", None, None, None),
        ("eid-test-0003", "delete me 2", "", None, None, None),
        ("eid-test-0004", "delete me 3", "", None, None, 0),
        ("eid-test-0005", "delete me 4", "", "eid-test-0004", None, 1),
        ("eid-test-0006", "delete me 5", "", "eid-test-0004", None, 1),
        ("eid-test-0007", "delete me 6", "", "eid-test-0004", None, 1),
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
            f"INSERT INTO {Env.NODE_TABLE_NAME} VALUES (?, ?, ?, ?, ?, ?);", cls.rows_to_setup
        )

    @classmethod
    def cleanup_table(cls, cursor):
        eids = [(row[0],) for row in cls.rows_to_setup] + [(row[0],) for row in cls.rows_created_in_tests]
        cursor.executemany(
            f"DELETE FROM {Env.NODE_TABLE_NAME} WHERE eid = (?);", eids
        )

    @classmethod
    def tearDownClass(cls):
        cursor = cls.db_connection.cursor()
        cls.cleanup_table(cursor)
        cls.db_connection.commit()
        cls.db_connection.close()


    def test_get_node_01(self):
        node = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).get(eid=self.rows_to_setup[0][0])
        self.assertEqual(node['node_name'], self.rows_to_setup[0][1])

    def test_get_node_02(self):
        node = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).get(eid=self.rows_to_setup[1][0])
        self.assertEqual(node['node_name'], self.rows_to_setup[1][1])

    def test_get_node_03(self):
        node = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).get(eid=self.rows_to_setup[2][0])
        self.assertEqual(node['node_name'], self.rows_to_setup[2][1])

    def test_create_node_01(self):
        row = (..., "Hello this row is created in test 01", "description")
        node_eid = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).create(name=row[1], description="hello")
        row = (node_eid, *row[1:])
        self.rows_created_in_tests.append(row)
        fetched_row = self.get_row(eid=node_eid)
        self.assertEqual(fetched_row[1], row[0])

    def test_create_node_02(self):
        row = (..., "Hello this row is created in test 02", "description")
        node_eid = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).create(name=row[1], description="hello")
        row = (node_eid, *row[1:])
        self.rows_created_in_tests.append(row)
        fetched_row = self.get_row(eid=node_eid)
        self.assertEqual(fetched_row[1], row[0])

    def test_create_node_03(self):
        row = (..., "Hello this row is created in test 03", "description")
        node_eid = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).create(name=row[1], description="hello")
        row = (node_eid, *row[1:])
        self.rows_created_in_tests.append(row)
        fetched_row = self.get_row(eid=node_eid)
        self.assertEqual(fetched_row[1], row[0])

    def test_get_node_children_01(self):
        children = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).get_node_children(eid="eid-test-0004")
        eids = [child['eid'] for child in children]
        assert set(eids) == {"eid-test-0005", "eid-test-0006", "eid-test-0007"}

    def test_get_node_children_02(self):
        children = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).get_node_children(eid="eid-test-0007")
        eids = [child['eid'] for child in children]
        assert set(eids) == set()

    def get_row(self, eid):
        cursor = self.db_connection.cursor()
        cursor.execute(
            f"SELECT rowid, * FROM {Env.NODE_TABLE_NAME} WHERE eid = (?);", (eid,)
        )
        return cursor.fetchone()
