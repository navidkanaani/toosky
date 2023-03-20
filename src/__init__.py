from src.environments import Env

Env._init_envs_(
    env_file_path='.env'
)  # make sure that everyone is using initialized version of Env class

del Env  # for not exposing Env class in the src scope