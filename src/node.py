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

    def update(self, eid, name, description, parent_eid):
        values = {}
        if name:
            values['node_name'] = name
        if description:
            values['description'] = description
        if parent_eid:
            if self._is_cyclic_relation(child_eid=eid, parent_eid=parent_eid):
                raise ValueError(
                    f"Can't connect {eid} to {parent_eid}."
                )
            self._connect_nodes(child_eid=eid, parent_eid=parent_eid)
        elif parent_eid == '':
            if current_parent_eid := self.get(eid=eid)['parent_eid']:
                self.node_db_wrapper.update(eid, values={'parent_eid': None}, commit=False)
                self._disconnect_nodes(
                    child_eid=eid, 
                    parent_eid=current_parent_eid
                )
        if values:
            self.node_db_wrapper.update(eid, values=values, commit=False)
        self.node_db_wrapper.commit()


    def _connect_nodes(self, child_eid, parent_eid):
        if self._is_cyclic_relation(child_eid=child_eid, parent_eid=parent_eid):
            raise ValueError(
                    f"Can't connect {child_eid} to {parent_eid}."
            )

        child = self.get(eid=child_eid)
        if child['parent_eid']:
            self._disconnect_nodes(child_eid=child_eid, parent_eid=child['parent_eid'])

        self.node_db_wrapper.update(eid=child_eid, values={'parent_eid': parent_eid}, commit=True)

        # fixing levels:
        parent = self.get(eid=parent_eid)
        parent_level = parent['level']
        self.increment_nodes_level(node_eid=child_eid, step=parent_level + 1)
        self.node_db_wrapper.commit()

    def _disconnect_nodes(self, child_eid, parent_eid):
        self.node_db_wrapper.update(eid=child_eid, values={'parent_eid': None}, commit=True)

        # fixing levels:
        parent = self.get(eid=parent_eid)
        parent_level = parent['level']
        self.increment_nodes_level(node_eid=child_eid, step=-(parent_level + 1))
        self.node_db_wrapper.commit()

    def increment_nodes_level(self, node_eid, step=1, commit=False):
        self._increment_nodes_level(node_eid=node_eid, step=step)
        if commit:
            self.node_db_wrapper.commit()

    def _increment_nodes_level(self, node_eid, step):
        node_level = self.get(eid=node_eid)['level']
        self._set_level(node_eid=node_eid, level=node_level + step)
        children = self.get_node_children(eid=node_eid)
        for child in children:
            self._increment_nodes_level(node_eid=child['eid'], step=step)


    def _set_level(self, node_eid, level, commit=False):
        self.node_db_wrapper.update(eid=node_eid, values={'level': level}, commit=commit)

    def _is_cyclic_relation(self, child_eid, parent_eid) -> bool:
        if not (children := self.get_node_children(eid=child_eid)):
            return False
        children_eid = [child['eid'] for child in children]
        return (parent_eid in children_eid) or any(
            self._is_cyclic_relation(child_eid=eid, parent_eid=parent_eid)
            for eid in children_eid
        )

    def get_node_children(self, eid):
        return self.node_db_wrapper.filter(values={"parent_eid":eid})

    def __del__(self):
        self.node_db_wrapper.__del__()

