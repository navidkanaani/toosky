from uuid import uuid4

from src.db.sqlite import SQLiteWrapper


class NodeManager:
    def __init__(self, db, table_name):
        self.node_db_wrapper = SQLiteWrapper(db=db, table_name=table_name)

    def create(self, name: str, description: str):
        token = uuid4().hex
        self.node_db_wrapper.insert(token, name, description, commit=True)
        return token

    def get(self, node_id):
        return self.node_db_wrapper.fetch(id_=node_id)

    def delete(self, node_id):
        return self.node_db_wrapper.delete(id_=node_id, commit=True)

    def search(self):
        return self.node_db_wrapper.filter()

    def __del__(self):
        self.node_db_wrapper.__del__()

