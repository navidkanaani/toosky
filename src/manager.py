from src.node import NodeManager
from src.rule import RuleManager
from src.environments import Env


class Manager:
    def __init__(self, db=None):
        self.node_manager = NodeManager(db=(db or Env.DB_NAME), table_name=Env.NODE_TABLE_NAME)
        self.rule_manager = RuleManager(db=(db or Env.DB_NAME), table_name=Env.RULE_TABLE_NAME)

    def create_node(self, name: str, description: str):
        return self.node_manager.create(name=name, description=description)

    def get_node(self, eid: str) -> dict:
        return self.node_manager.get(eid=eid)

    def delete_node(self, eid: str):
        self.node_manager.delete(eid=eid)

    def search_node(self):
        return self.node_manager.search()

    def update_node(self, eid: str, name: str, description: str, parent_eid: str):
        self.node_manager.update(
            eid=eid, name=name, 
            description=description, 
            parent_eid=parent_eid,
            level=None
        )
    
    def create_rule(self, name: str):
        return self.rule_manager.create(name=name)
    
    def get_rule(self, eid: str):
        return self.rule_manager.get(eid=eid) 
    
    def search_rule(self):
        return self.rule_manager.search()
        
    def update_rule(self, eid: str, name: str):
        self.rule_manager.update(eid=eid, name=name)
        
    
    def delete_rule():
        ...
    
    def __del__(self):
        self.node_manager.__del__()
