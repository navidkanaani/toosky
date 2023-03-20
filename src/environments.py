import dotenv

class EnvMeta(type):

    def __getattr__(cls, attr):
        return cls._envs_dict[attr]


class Env(metaclass=EnvMeta):

    def __new__(cls, *args, **kwargs):
        raise Exception(
            "This class can not be instantiated."
        )

    @classmethod
    def _init_envs_(cls, env_file_path):
        import pathlib
        if not pathlib.Path(env_file_path).is_file():
            raise FileNotFoundError
        envs = dotenv.dotenv_values(env_file_path)
        cls._envs_dict = {**envs}
