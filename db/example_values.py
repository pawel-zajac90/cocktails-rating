import sqlite3
from config import db_path
from random import randint
from cocktails_rating.helpers import update_rate

con = sqlite3.connect(db_path)
con.row_factory = sqlite3.Row
cur = con.cursor()


class FillTables:
    # Add pubs from pub_list to Pubs table.
    def add_pubs(self, pubs_number):
        pub_list = []
        for _ in range(1, pubs_number+1):
            name = 'Pub' + str(_)
            pub_list.append((None, name))
        cur.executemany('''
                    INSERT INTO Pubs (pub_id, pub_name) VALUES (?,?);''', pub_list)

    # Add cocktails from cocktails_list to Cocktails table for each pub from Pubs.
    def add_cocktails(self, cocktails_number):
        # Create list of all pubs in Pubs table.
        c = cur.execute('SELECT pub_id FROM Pubs')
        ids = []
        for _ in c:
            ids.append(_['pub_id'])
        # Create cocktails_list.
        cocktails_list = []
        for id in ids:
            for cocktail in range(1, cocktails_number+1):
                name = 'Cocktail' + str(cocktail)
                cocktails_list.append((None, name, id, 0))
        # Add cocktails from cocktails_list to Cocktails table for each pub.
        cur.executemany('''
                    INSERT INTO Cocktails (drink_id, drink_name, pub_id, rate)
                    VALUES (?, ?, ?, ?);
                    ''', cocktails_list)

    # Add rating for each cocktail from Cocktails into Rating table.
    def add_rates(self):
        c = cur.execute('''
                        SELECT drink_id, pub_id
                        FROM Cocktails
                        ''')
        cocktails = []
        for _ in c:
            rate = randint(1, 5)
            cocktails.append((None, _['drink_id'], _['pub_id'], rate))

        cur.executemany('''
                    INSERT INTO Rating (rate_id, drink_id, pub_id, rate)
                    VALUES (?, ?, ?, ?);
                    ''', cocktails)

    # Update rates in Cocktails from rates in Rating using helpers module.
    def update(self):
        i = cur.execute('''
                        SELECT drink_id
                        FROM Cocktails
                        ''')
        ids = []
        for _ in i:
            ids.append(_['drink_id'])
        for _ in ids:
            update_rate(cur, con, _)


if __name__ == '__main__':
    fill = FillTables()
    fill.add_pubs(5) # Set pubs number
    fill.add_cocktails(10) # Set cocktails number
    fill.add_rates()
    fill.update()
    con.commit()
