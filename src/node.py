from src.db.sqlite import SQLiteWrapper
from src.utility import gen_eid


class NodeManager:
    def __init__(self, db, table_name):
        self.node_db_wrapper = SQLiteWrapper(db=db, table_name=table_name)

    def create(self, name: str, description: str, rule_eid=None, parent_eid=None):
        eid = gen_eid()
        self.node_db_wrapper.insert(
            eid, name, description, parent_eid, rule_eid, 0, commit=True
        )  
        return eid

    def get(self, eid):
        return self.node_db_wrapper.fetch(eid=eid)

    def delete(self, eid):
        return self.node_db_wrapper.delete(eid=eid, commit=True)

    def search(self):
        return self.node_db_wrapper.filter()

    def update(self, eid, name, description, parent_eid, level):
        values = {}
        if name:
            values['node_name'] = name
        if description:
            values['description'] = description
        if parent_eid:
            values['parent_eid'] = parent_eid
        if level is not None:
            values['level'] = level
        self.node_db_wrapper.update(eid, values=values, commit=True)


    def __del__(self):
        self.node_db_wrapper.__del__()

