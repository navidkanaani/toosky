from src.db.sqlite import NodeSQLiteWrapper


class NodeManager:
    def __init__(self):
        self.db_wrapper = NodeSQLiteWrapper()

    def create(self, name: str):
        node_id = self.db_wrapper.insert(name, commit=True)
        return node_id

    def get(self, node_id):
        return self.db_wrapper.fetch(id_=node_id)
