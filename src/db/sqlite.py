import sqlite3

from src.environments import Env
from src.interfaces import BaseDBWrapper


class SQLiteWrapper(BaseDBWrapper):
    def __init__(self, db: str, table_name: str):
        self.table_name = table_name
        self.con = sqlite3.connect(db)
        self.con.execute("PRAGMA foreign_keys = 1")
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
            self.commit()
            return crs.lastrowid

    @staticmethod
    def _make_insert_query(*columns, table: str):
        values_placeholder = f"({', '.join('?' * len(columns))})"
        query = f"INSERT INTO {table} VALUES {values_placeholder};"
        return query

    def commit(self):
        self.con.commit()

    def fetch(self, eid):
        crs = self.con.cursor()
        crs.execute(
            f"SELECT * FROM {self.table_name} WHERE eid = (?);", (eid,)
        )
        if row := crs.fetchone():
            return row
        else:
            raise Exception

    def delete(self, eid, commit=False):
        crs = self.con.cursor()
        crs.execute(
            f"DELETE FROM {self.table_name} WHERE eid = (?);", (eid,)
        )
        if commit:
            self.commit()

    def filter(self, values={}):
        crs = self.con.cursor()
        query = self._make_filter_query(values=values, table=self.table_name)
        crs.execute(
            query, tuple(list(values.values()))
        )
        if rows := crs.fetchall():
            return rows
        else:
            return []

    @staticmethod
    def _make_filter_query(values, table: str):
        values_placeholder = ' AND '.join(f'{k} = ?' for k in values)
        query = f"SELECT rowid, * FROM {table}{' WHERE ' if values else ''}{values_placeholder};"
        return query

    def update(self, eid, values: dict, commit=False):
        crs = self.con.cursor()
        query = self._make_update_query(values, self.table_name)
        crs.execute(
            query, tuple(list(values.values()) + [eid])
        )
        if commit:
            self.commit()

    @staticmethod
    def _make_update_query(values, table: str):
        values_placeholder = f"{', '.join(f'{k} = ?' for k in values)}"
        query = f"UPDATE {table} SET {values_placeholder} WHERE eid = (?);"
        return query


    def __del__(self):
        self.con.close()
