from src.db.sqlite import NodeSQLiteWrapper


class NodeManager:
    def __init__(self):
        self.node_db_wrapper = NodeSQLiteWrapper()

    def create(self, name: str):
        node_id = self.node_db_wrapper.insert(name, commit=True)
        return node_id

    def get(self, node_id):
        return self.node_db_wrapper.fetch(id_=node_id)
