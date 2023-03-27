from src.db.sqlite import SQLiteWrapper


class NodeManager:
    def __init__(self, db, table_name):
        self.node_db_wrapper = SQLiteWrapper(db=db, table_name=table_name)

    def create(self, name: str):
        node_id = self.node_db_wrapper.insert(name, commit=True)
        return node_id

    def get(self, node_id):
        return self.node_db_wrapper.fetch(id_=node_id)

    def delete(self, node_id):
        return self.node_db_wrapper.delete(id_=node_id, commit=True)

    def search(self):
        return self.node_db_wrapper.filter()

    def __del__(self):
        self.node_db_wrapper.__del__()

