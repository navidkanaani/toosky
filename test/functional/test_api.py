import multiprocessing
import sqlite3
import time
import unittest

import requests

from src.api import app
from src.environments import Env


class TestPingAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.shutup_logs()
        cls.app = app
        Env._init_envs_(env_file_path='.env')
        cls.app_process = multiprocessing.Process(
            target=cls.app.run, 
            kwargs={'host': Env.TEST_HOST, 'port': Env.TEST_PORT, 'debug': False}
        )
        cls.app_process.daemon = True
        cls.app_process.start()
        cls.host = f'http://{Env.TEST_HOST}:{Env.TEST_PORT}'
        cls.db_connection = sqlite3.connect(Env.TEST_DB_NAME)
        crs = cls.db_connection.cursor()
        time.sleep(.2)

    @staticmethod
    def shutup_logs():
        import logging
        log = logging.getLogger('werkzeug')
        log.disabled = True

    def test_ping_01(self):
        response = requests.get(f'{self.host}/ping')
        self.assertEqual(response.json()['content'], 'pong')
        self.assertEqual(response.status_code, 200)




class TestCreateNode(unittest.TestCase):
    
    garbage_tokens = []

    @classmethod
    def setUpClass(cls):
        cls.shutup_logs()
        cls.app = app
        Env._init_envs_(env_file_path='.env')
        cls.app_process = multiprocessing.Process(
            target=cls.app.run, 
            kwargs={'host': Env.TEST_HOST, 'port': Env.TEST_PORT, 'debug': False}
        )
        cls.db_connection = sqlite3.connect(Env.TEST_DB_NAME)
        cls.app_process.daemon = True
        cls.app_process.start()
        cls.host = f'http://{Env.TEST_HOST}:{Env.TEST_PORT}'
        time.sleep(.2)

    @staticmethod
    def shutup_logs():
        import logging
        log = logging.getLogger('werkzeug')
        log.disabled = True


    def test_create_node_01(self):
        import json
        request = {
            "name": "unusable-node-1",
            "description": "It's actually an unusable node."
        }
        response = requests.post(f'{self.host}/node', json=request)
        token = response.json()["token"]
        self.garbage_tokens.append(token)
        row = self.get_row(token=token)
        self.assertEqual(row[1], token)

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
        cursor.executemany(
            f"DELETE FROM {Env.NODE_TABLE_NAME} WHERE token = (?);", 
            [(token,) for token in cls.garbage_tokens]
        )

    def get_row(self, token):
        cursor = self.db_connection.cursor()
        cursor.execute(
            f"SELECT rowid, * FROM {Env.NODE_TABLE_NAME} WHERE token = (?);", (token,)
        )
        return cursor.fetchone()


class TestGetNode(unittest.TestCase):
    ...


class TestDeleteNode(unittest.TestCase):
    ...


if __name__ == '__main__':
    unittest.main()