from src.db.sqlite import SQLiteWrapper
from src.utility import gen_token


class NodeManager:
    def __init__(self, db, table_name):
        self.node_db_wrapper = SQLiteWrapper(db=db, table_name=table_name)

    def create(self, name: str, description: str, rule_token=None, parent_token=None):
        token = gen_token()
        self.node_db_wrapper.insert(
            token, name, description, parent_token, rule_token, 0, commit=True
        )  
        return token

    def get(self, token):
        return self.node_db_wrapper.fetch(token=token)

    def delete(self, token):
        return self.node_db_wrapper.delete(token=token, commit=True)

    def search(self):
        return self.node_db_wrapper.filter()

    def update(self, token, name, description, parent_token, level):
        values = {}
        if name:
            values['node_name'] = name
        if description:
            values['description'] = description
        if parent_token:
            values['parent_token'] = parent_token
        if level is not None:
            values['level'] = level
        self.node_db_wrapper.update(token, values=values, commit=True)


    def __del__(self):
        self.node_db_wrapper.__del__()

