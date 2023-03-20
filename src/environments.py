import dotenv

class Env:
    env_file_path = ".env"
    keys = (
        'TEST_DB_NAME'
    )

    @classmethod
    def _init_envs_(cls, env_file_path=None):
        envs = dotenv.dotenv_values(env_file_path or cls.env_file_path)
        cls._envs_dict = {}
        for key in cls.keys:
            cls._envs_dict[key] = envs[key]

