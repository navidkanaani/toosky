import multiprocessing
import sqlite3
import time
import unittest

import requests

from src.api import app
from src.environments import Env

class BaseAPITest:

    @classmethod
    def _setUpClass(cls):
        cls.shutup_logs()
        cls.app = app
        Env._init_envs_(env_file_path='.env')
        cls.app_process = multiprocessing.Process(
            target=cls.app.run, 
            kwargs={'host': Env.TEST_HOST, 'port': Env.TEST_PORT, 'debug': False}
        )
        cls.db_connection = sqlite3.connect(Env.TEST_DB_NAME)
        cls.db_connection.row_factory = lambda cursor, row: {
            k: v for k, v in zip([c[0] for c in cursor.description], row)
        }
        cls.app_process.daemon = True
        cls.app_process.start()
        cls.host = f'http://{Env.TEST_HOST}:{Env.TEST_PORT}'
        time.sleep(.2)


    @staticmethod
    def shutup_logs():
        import logging
        log = logging.getLogger('werkzeug')
        log.disabled = True


    @classmethod
    def _tearDownClass(cls):
        cls.db_connection.close()
        cls.app_process.terminate()
        cls.app_process.join()


class TestPingAPI(unittest.TestCase, BaseAPITest):

    @classmethod
    def setUpClass(cls):
        cls._setUpClass()

    @staticmethod
    def shutup_logs():
        import logging
        log = logging.getLogger('werkzeug')
        log.disabled = True

    def test_ping_01(self):
        response = requests.get(f'{self.host}/ping')
        self.assertEqual(response.json()['content'], 'pong')
        self.assertEqual(response.status_code, 200)


    @classmethod
    def tearDownClass(cls):
        cls._tearDownClass()


class TestCreateNode(unittest.TestCase, BaseAPITest):
    
    garbage_eids = []

    @classmethod
    def setUpClass(cls):
        cls._setUpClass()

    def test_create_node_01(self):
        import json
        request = {
            "name": "unusable-node-1",
            "description": "It's actually an unusable node."
        }
        response = requests.post(f'{self.host}/node', json=request)
        eid = response.json()["eid"]
        self.garbage_eids.append(eid)
        row = self.get_row(eid=eid)
        self.assertEqual(row["eid"], eid)
        self.assertEqual(row["node_name"], request["name"])
        self.assertEqual(row["description"], request["description"])


    def test_create_node_02(self):
        import json
        request = {
            "name": "unusable-node-2",
            "description": ""
        }
        response = requests.post(f'{self.host}/node', json=request)
        eid = response.json()["eid"]
        self.garbage_eids.append(eid)
        row = self.get_row(eid=eid)
        self.assertEqual(row["eid"], eid)
        self.assertEqual(row["node_name"], request["name"])
        self.assertEqual(row["description"], request["description"])


    def test_create_node_03(self):
        import json
        request = {
            "name": "unusable-node-3",
            "description": "Its okay to be description"
        }
        response = requests.post(f'{self.host}/node', json=request)
        eid = response.json()["eid"]
        self.garbage_eids.append(eid)
        row = self.get_row(eid=eid)
        self.assertEqual(row["eid"], eid)
        self.assertEqual(row["node_name"], request["name"])
        self.assertEqual(row["description"], request["description"])


    @classmethod
    def tearDownClass(cls):
        cursor = cls.db_connection.cursor()
        cls.cleanup_table(cursor)
        cls.db_connection.commit()
        cls._tearDownClass()

    @classmethod
    def cleanup_table(cls, cursor):
        cursor.executemany(
            f"DELETE FROM {Env.NODE_TABLE_NAME} WHERE eid = (?);", 
            [(eid,) for eid in cls.garbage_eids]
        )

    def get_row(self, eid):
        cursor = self.db_connection.cursor()
        cursor.execute(
            f"SELECT rowid, * FROM {Env.NODE_TABLE_NAME} WHERE eid = (?);", (eid,)
        )
        return cursor.fetchone()


class TestGetNode(unittest.TestCase, BaseAPITest):
    rows_to_setup = [
        ("eid-test-0001", "delete me 0", "hello", None, None, None),
        ("eid-test-0002", "delete me 1", "okay", None, None, None),
        ("eid-test-0003", "delete me 2", "", None, None, None),
    ]

    @classmethod
    def setUpClass(cls):
        cls._setUpClass()
        crs = cls.db_connection.cursor()
        cls.setup_table_records(cursor=crs)
        cls.db_connection.commit()


    @classmethod
    def setup_table_records(cls, cursor):
        cursor.executemany(
            f"INSERT INTO {Env.NODE_TABLE_NAME} VALUES (?, ?, ?, ?, ?, ?);", cls.rows_to_setup
        )

    def test_get_node_01(self):
        row = self.rows_to_setup[0]
        response = requests.get(f'{self.host}/node/{row[0]}')
        node = response.json()["node"]
        self.assertEqual(node["eid"], row[0])
        self.assertEqual(node["node_name"], row[1])
        self.assertEqual(node["description"], row[2])

    def test_get_node_02(self):
        row = self.rows_to_setup[1]
        response = requests.get(f'{self.host}/node/{row[0]}')
        node = response.json()["node"]
        self.assertEqual(node["eid"], row[0])
        self.assertEqual(node["node_name"], row[1])
        self.assertEqual(node["description"], row[2])

    def test_get_node_03(self):
        row = self.rows_to_setup[2]
        response = requests.get(f'{self.host}/node/{row[0]}')
        node = response.json()["node"]
        self.assertEqual(node["eid"], row[0])
        self.assertEqual(node["node_name"], row[1])
        self.assertEqual(node["description"], row[2])


    @classmethod
    def cleanup_table(cls, cursor):
        cursor.executemany(
            f"DELETE FROM {Env.NODE_TABLE_NAME} WHERE eid = (?);", 
            [(row[0],) for row in cls.rows_to_setup]
        )

    def get_row(self, eid):
        cursor = self.db_connection.cursor()
        cursor.execute(
            f"SELECT rowid, * FROM {Env.NODE_TABLE_NAME} WHERE eid = (?);", (eid,)
        )
        return cursor.fetchone()

    @classmethod
    def tearDownClass(cls):
        cursor = cls.db_connection.cursor()
        cls.cleanup_table(cursor)
        cls.db_connection.commit()
        cls._tearDownClass()


class TestDeleteNode(unittest.TestCase, BaseAPITest):
    rows_to_setup = [
        ("eid-test-0001", "delete me 0", "hello", None, None, None),
        ("eid-test-0002", "delete me 1", "okay", None, None, None),
        ("eid-test-0003", "delete me 2", "", None, None, None),
    ]

    @classmethod
    def setUpClass(cls):
        cls._setUpClass()
        crs = cls.db_connection.cursor()
        cls.setup_table_records(cursor=crs)
        cls.db_connection.commit()


    @classmethod
    def setup_table_records(cls, cursor):
        cursor.executemany(
            f"INSERT INTO {Env.NODE_TABLE_NAME} VALUES (?, ?, ?, ?, ?, ?);", cls.rows_to_setup
        )

    def test_delete_node_01(self):
        row = self.rows_to_setup[0]
        response = requests.delete(f'{self.host}/node/{row[0]}')
        self.assertIsNone(self.get_row(self.db_connection.cursor(), row[0]))

    def test_delete_node_02(self):
        row = self.rows_to_setup[1]
        response = requests.delete(f'{self.host}/node/{row[0]}')
        self.assertIsNone(self.get_row(self.db_connection.cursor(), row[0]))

    def test_delete_node_03(self):
        row = self.rows_to_setup[2]
        response = requests.delete(f'{self.host}/node/{row[0]}')
        self.assertIsNone(self.get_row(self.db_connection.cursor(), row[0]))


    @classmethod
    def cleanup_table(cls, cursor):
        cursor.executemany(
            f"DELETE FROM {Env.NODE_TABLE_NAME} WHERE eid = (?);", 
            list(
                filter(
                    lambda r: cls.get_row(cursor, r[0]), 
                    [(row[0],) for row in cls.rows_to_setup]
                )
            )
        )

    @staticmethod
    def get_row(cursor, eid):
        cursor.execute(
            f"SELECT rowid, * FROM {Env.NODE_TABLE_NAME} WHERE eid = (?);", (eid,)
        )
        return cursor.fetchone()

    @classmethod
    def tearDownClass(cls):
        cursor = cls.db_connection.cursor()
        cls.cleanup_table(cursor)
        cls.db_connection.commit()
        cls._tearDownClass()


class TestUpdateNode(unittest.TestCase, BaseAPITest):
    rows_to_setup = [
        ("eid-test-0001", "delete me 0", "hello", None, None, None),
        ("eid-test-0002", "delete me 1", "okay", None, None, None),
        ("eid-test-0003", "delete me 2", "", None, None, None),
    ]

    @classmethod
    def setUpClass(cls):
        cls._setUpClass()
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
        cursor.executemany(
            f"DELETE FROM {Env.NODE_TABLE_NAME} WHERE eid = (?);", 
            list(
                filter(
                    lambda r: cls.get_row(cursor, r[0]), 
                    [(row[0],) for row in cls.rows_to_setup]
                )
            )
        )

    @staticmethod
    def get_row(cursor, eid):
        cursor.execute(
            f"SELECT rowid, * FROM {Env.NODE_TABLE_NAME} WHERE eid = (?);", (eid,)
        )
        return cursor.fetchone()

    @classmethod
    def tearDownClass(cls):
        cursor = cls.db_connection.cursor()
        cls.cleanup_table(cursor)
        cls.db_connection.commit()
        cls._tearDownClass()

    def test_update_description_01(self):
        row = self.rows_to_setup[0]
        new_description01 = "newly generated one"
        request = {
            "description": new_description01
        }
        response = requests.put(f'{self.host}/node/{row[0]}', json=request)
        updated_row01 = self.get_row(self.db_connection.cursor(), row[0])
        self.assertEqual(updated_row01['description'], new_description01)

        new_description02 = "another newly generated one"
        request = {
            "description": new_description02
        }
        response = requests.put(f'{self.host}/node/{row[0]}', json=request)
        updated_row02 = self.get_row(self.db_connection.cursor(), row[0])
        self.assertEqual(updated_row02['description'], new_description02)

    def test_update_name_01(self):
        row = self.rows_to_setup[0]
        new_name01 = "new name number one"
        request = {
            "name": new_name01
        }
        response = requests.put(f'{self.host}/node/{row[0]}', json=request)
        updated_row01 = self.get_row(self.db_connection.cursor(), row[0])
        self.assertEqual(updated_row01['node_name'], new_name01)

        new_name02 = "new name number two"
        request = {
            "name": new_name02
        }
        response = requests.put(f'{self.host}/node/{row[0]}', json=request)
        updated_row02 = self.get_row(self.db_connection.cursor(), row[0])
        self.assertEqual(updated_row02['node_name'], new_name02)

    def test_update_parent_eid_01(self):
        row0 = self.rows_to_setup[0]  # child
        row1 = self.rows_to_setup[1]  # parent
        request = {
            "parent_eid": row1[0]
        }
        response = requests.put(f'{self.host}/node/{row0[0]}', json=request)
        updated_row0 = self.get_row(self.db_connection.cursor(), row0[0])
        self.assertEqual(updated_row0['parent_eid'], row1[0])

        row2 = self.rows_to_setup[2]  # parent
        request = {
            "parent_eid": row2[0]
        }
        response = requests.put(f'{self.host}/node/{row0[0]}', json=request)
        updated_row0 = self.get_row(self.db_connection.cursor(), row0[0])
        self.assertEqual(updated_row0['parent_eid'], row2[0])

        
class TestCreateRule(unittest.TestCase): 
    garbage_eids = []
    @classmethod
    def setUpClass(cls):
        cls.app = app
        Env._init_envs_(env_file_path=".env")
        cls.app_process = multiprocessing.Process(target=cls.app.run, kwargs={"host": Env.TEST_HOST,
                                                                              "port": Env.TEST_PORT,
                                                                              "debug": False})
        cls.db_connection = sqlite3.connect(Env.TEST_DB_NAME)
        cls.db_connection.row_factory = lambda cursor, row: {k: v for k, v in zip([c[0] for c in cursor.description], row)}
        cls.app_process.daemon = True
        cls.app_process.start()
        cls.host = f"http://{Env.TEST_HOST}:{Env.TEST_PORT}"
        time.sleep(.2)
        
    @staticmethod
    def disable_logs():
        import logging
        log = logging.getLogger("werkzeug")
        log.disabled = True
    
    def test_create_rule_01(self):
        import json
        request = {
            "name": "Rule one"
        }
        response = requests.post(f"{self.host}/rule", json=request)
        eid = response.json()["eid"]
        rule_entity = self.retrieve_rule(eid=eid)
        self.assertEqual(rule_entity["eid"], eid)
        
    def retrieve_rule(self, eid):
        cursor = self.db_connection.cursor()
        row = cursor.execute(f"SELECT * FROM {Env.RULE_TABLE_NAME} WHERE eid = (?)", (eid, ))
        return row
    
    @classmethod
    def tearDownClass(cls):
        cursor = cls.db_connection.cursor()
        cls.cleanup_table(cursor)
        cls.db_connection.commit()
        cls.db_connection.close()
        cls.app_process.terminate()
        cls.app_process.join()

    @classmethod
    def cleanup_table(cls, cursor):
        cursor.executemany(f"DELETE FROM {Env.RULE_TABLE_NAME} WHERE eid = (?)", [(eid, ) for eid in cls.garbage_eids])

if __name__ == '__main__':
    unittest.main()