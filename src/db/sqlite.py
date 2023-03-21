import sqlite3

from src.environments import Env
from src.interfaces import BaseDBWrapper


class BaseSQLiteWrapper(BaseDBWrapper):
    ...



class NodeSQLiteWrapper(BaseSQLiteWrapper):
    def __init__(self, db: str = None, table_name: str = None):
        self.table_name = table_name or Env.NODE_TABLE_NAME
        self.con = sqlite3.connect(db or Env.DB_NAME)

    def insert(self, name, commit=False):
        crs = self.con.cursor()
        crs.execute(
            f"INSERT INTO {self.table_name} VALUES (?);", (name,)
        )
        if commit:
            self.con.commit()

    def commit(self):
        self.con.commit()

    def fetch(self, id_):
        ...
