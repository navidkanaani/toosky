import dotenv

class EnvMeta(type):

    def __getattr__(cls, attr):
        return cls._envs_dict[attr]


class Env(metaclass=EnvMeta):
    env_file_path = ".env"
    keys = (
        'TEST_DB_NAME',
    )

    def __new__(cls, *args, **kwargs):
        raise Exception(
            "This class must not be instantiated."
        )

    @classmethod
    def _init_envs_(cls, env_file_path=None, keys=None):
        envs = dotenv.dotenv_values(env_file_path or cls.env_file_path)
        cls._envs_dict = {}
        for key in keys or cls.keys:
            cls._envs_dict[key] = envs[key]

