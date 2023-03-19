import sqlite3

con = sqlite3.connect("test.db")

def create_tables(connection):
    with open("schema/tables.sql") as f:
        script = f.read()
    connection.cursor().executescript(
        script
    )

if __name__ == '__main__':
    create_tables(con)