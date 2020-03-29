import sqlite3


def create_users(cur):
    cur.executescript('''
                CREATE TABLE IF NOT EXISTS Users ( 
                user_id INTEGER PRIMARY KEY ASC,
                login varchar (24),
                email varchar (35),
                created_at varchar (19))
                ''')

def create_passwords(cur):
    cur.execute('''
                CREATE TABLE IF NOT EXISTS Passwords (
                pass_id INTEGER PRIMARY KEY ASC,
                login varchar(24),
                hash varchar(250)
                )
                ''')

if __name__ == '__main__':
    con = sqlite3.connect('authorization.db')
    con.row_factory = sqlite3.Row
    create_users(con.cursor())
    create_passwords(con.cursor())
