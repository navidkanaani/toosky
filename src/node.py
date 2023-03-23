from src.db.sqlite import NodeSQLiteWrapper


class NodeManager:
    def __init__(self):
        self.db_wrapper = NodeSQLiteWrapper()

    def create(self, name: str):
        node_id = self.db_wrapper.insert(name, commit=True)
        return node_id

    def get(self, node_id):
        return self.db_wrapper.fetch(id_=node_id)

    def delete(self, node_id):
        return self.db_wrapper.delete(id_=node_id, commit=True)

    def search(self):
        return self.db_wrapper.filter()

    def __del__(self):
        self.db_wrapper.__del__()

