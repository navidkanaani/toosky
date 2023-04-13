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

        ("eid-test-0009", "delete me 7", "", "eid-test-0011", None, 1),
        ("eid-test-0010", "delete me 8", "", "eid-test-0009", None, 1),
        ("eid-test-0011", "delete me 9", "", None, None, 1),

        ("eid-test-0012", "delete me 10", "", "eid-test-0013", None, 1),
        ("eid-test-0013", "delete me 11", "", None, None, 1),
        ("eid-test-0014", "delete me 12", "", None, None, 1),

        ("eid-test-0015", "delete me 13", "", "eid-test-0016", None, 1),
        ("eid-test-0016", "delete me 14", "", None, None, 1),

    ]

    rows_created_in_tests = []

    @property
    def node_manager(self):
        return NodeManager(
            db=Env.TEST_DB_NAME,
            table_name=Env.NODE_TABLE_NAME
        )

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
        node = self.node_manager.get(eid=self.rows_to_setup[0][0])
        self.assertEqual(node['node_name'], self.rows_to_setup[0][1])

    def test_get_node_02(self):
        node = self.node_manager.get(eid=self.rows_to_setup[1][0])
        self.assertEqual(node['node_name'], self.rows_to_setup[1][1])

    def test_get_node_03(self):
        node = NodeManager(db=Env.TEST_DB_NAME, table_name=Env.NODE_TABLE_NAME).get(eid=self.rows_to_setup[2][0])
        self.assertEqual(node['node_name'], self.rows_to_setup[2][1])

    def test_create_node_01(self):
        row = (..., "Hello this row is created in test 01", "description")
        node_eid = self.node_manager.create(name=row[1], description="hello")
        row = (node_eid, *row[1:])
        self.rows_created_in_tests.append(row)
        fetched_row = self.get_row(eid=node_eid)
        self.assertEqual(fetched_row[1], row[0])

    def test_create_node_02(self):
        row = (..., "Hello this row is created in test 02", "description")
        node_eid = self.node_manager.create(name=row[1], description="hello")
        row = (node_eid, *row[1:])
        self.rows_created_in_tests.append(row)
        fetched_row = self.get_row(eid=node_eid)
        self.assertEqual(fetched_row[1], row[0])

    def test_create_node_03(self):
        row = (..., "Hello this row is created in test 03", "description")
        node_eid = self.node_manager.create(name=row[1], description="hello")
        row = (node_eid, *row[1:])
        self.rows_created_in_tests.append(row)
        fetched_row = self.get_row(eid=node_eid)
        self.assertEqual(fetched_row[1], row[0])

    def test_get_node_children_01(self):
        children = self.node_manager.get_node_children(eid="eid-test-0004")
        eids = [child['eid'] for child in children]
        assert set(eids) == {"eid-test-0005", "eid-test-0006", "eid-test-0007"}

    def test_get_node_children_02(self):
        children = self.node_manager.get_node_children(eid="eid-test-0007")
        eids = [child['eid'] for child in children]
        assert set(eids) == set()

    def test_check_cyclic_relation_01(self):
        assert self.node_manager._is_cyclic_relation(
            child_eid="eid-test-0011", parent_eid="eid-test-0010"
        )

    def test_check_cyclic_relation_02(self):
        assert not self.node_manager._is_cyclic_relation(
            child_eid="eid-test-0014", parent_eid="eid-test-0012"
        )
        assert not self.node_manager._is_cyclic_relation(
            child_eid="eid-test-0014", parent_eid="eid-test-0013"
        )
        assert not self.node_manager._is_cyclic_relation(
            child_eid="eid-test-0013", parent_eid="eid-test-0014"
        )

    def test_check_cyclic_relation_03(self):
        assert self.node_manager._is_cyclic_relation(
            child_eid="eid-test-0016", parent_eid="eid-test-0015"
        )
        assert not self.node_manager._is_cyclic_relation(
            child_eid="eid-test-0015", parent_eid="eid-test-0016"
        )

    def get_row(self, eid):
        cursor = self.db_connection.cursor()
        cursor.execute(
            f"SELECT rowid, * FROM {Env.NODE_TABLE_NAME} WHERE eid = (?);", (eid,)
        )
        return cursor.fetchone()
