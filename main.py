from src.api import app
from src.environments import Env


def main():
    app.run(host=Env.HOST, port=Env.PORT, debug=Env.DEBUG_MODE)

if __name__ == '__main__':
    main()
