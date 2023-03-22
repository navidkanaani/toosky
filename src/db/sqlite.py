import sqlite3

from src.environments import Env
from src.interfaces import BaseDBWrapper


class BaseSQLiteWrapper(BaseDBWrapper):
    ...



class NodeSQLiteWrapper(BaseSQLiteWrapper):
    def __init__(self, db: str = None, table_name: str = None):
        self.table_name = table_name or Env.NODE_TABLE_NAME
        self.con = sqlite3.connect(db or Env.DB_NAME)
        self.con.row_factory = self.dict_factory

    dict_factory = staticmethod(
        lambda cursor, row: {
            k: v for k, v in zip([c[0] for c in cursor.description], row)
        }
    )

    def insert(self, name, commit=False):
        crs = self.con.cursor()
        crs.execute(
            f"INSERT INTO {self.table_name} VALUES (?);", (name,)
        )
        if commit:
            self.con.commit()
            return crs.lastrowid

    def commit(self):
        self.con.commit()

    def fetch(self, id_):
        crs = self.con.cursor()
        crs.execute(
            f"SELECT * FROM {self.table_name} WHERE rowid = (?);", (id_,)
        )
        if row := crs.fetchone():
            return row
        else:
            raise Exception