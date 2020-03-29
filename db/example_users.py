import sqlite3
from werkzeug.security import generate_password_hash

names = ('first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth')

users_list = []
passwords_list = []

for name in names:
    password = name + 'spassword'
    email = name + '@email.com'
    hash = generate_password_hash(password)
    users_list.append((name, email))
    passwords_list.append((name, hash))
    print(name + '/' + password)

def create_users(cur):
    cur.executemany('''
                INSERT INTO Users (login, email, created_at)
                VALUES (?, ?, datetime('now'));''', users_list)
    
def create_passwords(cur):
    cur.executemany('''
                INSERT INTO Passwords (login, hash)
                VALUES (?, ?);''', passwords_list)


if __name__ == '__main__':
    con = sqlite3.connect('authorization.db')
    con.row_factory = sqlite3.Row
    # create_users(con.cursor())
    create_passwords(con.cursor())
    con.commit()
