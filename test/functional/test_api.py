import threading
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
        cls.app_thread = threading.Thread(
            target=cls.app.run, 
            kwargs={'host': Env.TEST_HOST, 'port': Env.TEST_PORT, 'debug': False}
        )
        cls.app_thread.daemon = True
        cls.app_thread.start()
        cls.host = f'http://{Env.TEST_HOST}:{Env.TEST_PORT}'
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

    @classmethod
    def tearDownClass(cls):
        ...


if __name__ == '__main__':
    unittest.main()