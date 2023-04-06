from src.node import NodeManager
from src.environments import Env


class Manager:
    def __init__(self, db=None):
        self.node_manager = NodeManager(db=(db or Env.DB_NAME), table_name=Env.NODE_TABLE_NAME)

    def create_node(self, name: str, description: str):
        return self.node_manager.create(name=name, description=description)

    def get_node(self, token: str) -> dict:
        return self.node_manager.get(token=token)

    def delete_node(self, token: str):
        self.node_manager.delete(token=token)

    def search_node(self):
        return self.node_manager.search()

    def update_node(self, token: str, name: str, description: str, parent_token: str):
        self.node_manager.update(
            token=token, name=name, 
            description=description, 
            parent_token=parent_token,
            level=None
        )

    def __del__(self):
        self.node_manager.__del__()
