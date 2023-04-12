from src.db.sqlite import SQLiteWrapper
from src.utility import gen_eid


class RuleManager:
    def __init__(self, db, table_name):
        self.sql_wrapper = SQLiteWrapper(db=db, table_name=table_name)
    
    def create(self, name: str):
        eid = gen_eid()
        self.sql_wrapper.insert(eid, name, commit=True)
        return eid
    
    def get(self, eid: str):
        return self.sql_wrapper.fetch(eid=eid)
    
    def search(self):
        return self.sql_wrapper.filter()
        
    def update(self, eid: str):
        ...
        
    def delete(self, eid):
        ...