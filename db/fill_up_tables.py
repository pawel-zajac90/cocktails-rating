import sqlite3
from random import randint
from faker import Faker
from datetime import datetime
from werkzeug.security import generate_password_hash
db_path = 'cocktails.db'


# Fill up tables.
class Fill:
    def __init__(self, cur):
        self.cur = cur

    def fill_pubs(self, pubs_number):
        pubs_list = []
        for i in range(1, pubs_number+1):
            name = 'Pub' + str(i)
            pubs_list.append((None, name))
        self.cur.executemany('''
                        INSERT INTO Pubs (pub_id, pub_name)
                        VALUES (?, ?);
                        ''', pubs_list)

    def fill_cocktails(self, cocktails_number):
        # Create list of all pubs in Pubs table.
        pubs = self.cur.execute('SELECT pub_id FROM Pubs')
        ids = []
        for pub in pubs:
            ids.append(pub['pub_id'])
        # Create cocktails_list.
        cocktails_list = []
        for id in ids:
            for cocktail in range(1, cocktails_number + 1):
                name = 'Cocktail' + str(cocktail)
                cocktails_list.append((None, name, id))
        # Add cocktails from cocktails_list to Cocktails table for each pub.
        self.cur.executemany('''
                            INSERT INTO Cocktails (cocktail_id, cocktail_name, pub_id)
                            VALUES (?, ?, ?);
                            ''', cocktails_list)

    def fill_rates(self):
        ids = self.cur.execute('''
                        SELECT cocktail_id, pub_id
                        FROM Cocktails
                        ''')
        cocktails = []
        for id in ids:
            for _ in range(5):
                rate = randint(1, 5)
                cocktails.append((None, id['cocktail_id'], id['pub_id'], rate))

        self.cur.executemany('''
                    INSERT INTO Rates (rate_id, cocktail_id, pub_id, rate)
                    VALUES (?, ?, ?, ?);
                    ''', cocktails)

    def fill_users(self, users_number):
        fake = Faker()
        users_list = []
        for user in range(users_number):
            profile = fake.profile()
            users_list.append((None, profile['username'], profile['mail'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.cur.executemany('''
                        INSERT INTO Users (user_id, login, email, modified_on)
                        VALUES (?, ?, ?, ?)
                        ''', users_list)

    def fill_passwords(self):
        ids = self.cur.execute('''
                        SELECT user_id
                        FROM Users
                        ''')
        users = []
        for id in ids:
            users.append(id['user_id'])
        result = []
        fake = Faker()
        pass_list = []

        for user in users:
            password = fake.password()
            result.append((user, password))
            hash = generate_password_hash(password)
            pass_list.append((None, user, hash))
        self.cur.executemany('''
                        INSERT INTO Passwords (pass_id, user_id, hash)
                        VALUES (?, ?, ?);
                        ''', pass_list)
        return result


def save_to_file(data):
    con2 = sqlite3.connect('passwords.db')
    cur2 = con2.cursor()
    cur2.execute('''CREATE TABLE IF NOT EXISTS Passwords (user_id INTEGER PRIMARY KEY ASC, password);''')
    ids_in_db = cur2.execute('''
                            SELECT user_id
                            FROM Passwords
                            ''')
    existing_ids = []
    for id in ids_in_db:
        existing_ids.append(id[0])

    to_add = []
    for d in data:
        if d[0] not in existing_ids:
            to_add.append(d)

    cur2.executemany('''
                INSERT INTO Passwords (user_id, password)
                VALUES (?, ?);
                ''', to_add)
    con2.commit()


if __name__ == '__main__':
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    fill = Fill(con.cursor())
    fill.fill_pubs(10)
    fill.fill_cocktails(10)
    fill.fill_rates()
    fill.fill_users(3)
    data = fill.fill_passwords()
    con.commit()
    save_to_file(data)
