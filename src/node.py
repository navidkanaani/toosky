from src.db.sqlite import NodeSQLiteWrapper


class NodeManager:
    def __init__(self):
        self.node_db_wrapper = NodeSQLiteWrapper()

    def create(self, name: str):
        self.node_db_wrapper.insert(name, commit=True)
