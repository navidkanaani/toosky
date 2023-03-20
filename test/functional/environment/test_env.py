import unittest

from src.environments import Env

class TestEnv(unittest.TestCase):
    def test_read_env_01(self):
        Env._init_envs_(env_file_path="test/functional/environment/.env.test.1")
        self.assertEqual(Env.TEST_ENV_VARIABLE_1, "hello")

    def test_read_env_02(self):
        Env._init_envs_(env_file_path="test/functional/environment/.env.test.1")
        with self.assertRaises(KeyError):
            self.assertEqual(Env.TEST_ENV_VARIABLE_2, "hello")

    def test_read_env_03(self):
        with self.assertRaises(Exception):
                Env()  #  trying to instantiating the class

    def test_read_env_04(self):
        Env._init_envs_(env_file_path="test/functional/environment/.env.test.1")
        self.assertEqual(Env.TEST_DB_NAME, "dbname")

    def test_read_env_05(self):
        with self.assertRaises(FileNotFoundError):
            Env._init_envs_(env_file_path="DoesNotExistFile")


if __name__ == '__main__':
    unittest.main()
