import sqlite3

from src.environments import Env
from src.interfaces import BaseDBWrapper


class BaseSQLiteWrapper(BaseDBWrapper):
    ...



class SQLiteWrapper(BaseSQLiteWrapper):
    def __init__(self, db: str, table_name: str):
        self.table_name = table_name
        self.con = sqlite3.connect(db)
        self.con.row_factory = self.dict_factory

    dict_factory = staticmethod(
        lambda cursor, row: {
            k: v for k, v in zip([c[0] for c in cursor.description], row)
        }
    )

    def insert(self, *columns, commit=False):
        crs = self.con.cursor()
        query = self._make_insert_query(*columns, table=self.table_name)
        crs.execute(query, columns)
        if commit:
            self.con.commit()
            return crs.lastrowid

    @staticmethod
    def _make_insert_query(*columns, table: str):
        values_placeholder = f"({', '.join('?' * len(columns))})"
        query = f"INSERT INTO {table} VALUES {values_placeholder};"
        return query

    def commit(self):
        self.con.commit()

    def fetch(self, token):
        crs = self.con.cursor()
        crs.execute(
            f"SELECT * FROM {self.table_name} WHERE token = (?);", (token,)
        )
        if row := crs.fetchone():
            return row
        else:
            raise Exception

    def delete(self, token, commit=False):
        crs = self.con.cursor()
        crs.execute(
            f"DELETE FROM {self.table_name} WHERE token = (?);", (token,)
        )
        if commit:
            self.con.commit()

    def filter(self):
        crs = self.con.cursor()
        crs.execute(
            f"SELECT rowid, * FROM {self.table_name};"
        )
        if rows := crs.fetchall():
            return rows
        else:
            return []

    def __del__(self):
        self.con.close()
