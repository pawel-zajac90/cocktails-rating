import sqlite3
from config import db_path


# Create tables
def create(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Pubs (
        pub_id INTEGER PRIMARY KEY ASC,
        pub_name varchar(25) NOT NULL);
        """)

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Cocktails (
        drink_id INTEGER PRIMARY KEY ASC,
        drink_name varchar(25),
        pub_id int,
        rate int(5));
        ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Rating (
        rate_id INTEGER PRIMARY KEY ASC,
        drink_id int,
        pub_id int NOT NULL,
        rate int(5));
        ''')
    return True


if __name__ == '__main__':
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    create(con.cursor())
