import sqlite3
from config import db_path
from cocktails_rating.helpers import *


# Rating system.
class Rating:
    def __init__(self, con):
        self.con = con(db_path)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    # Check ratings for all cocktails in pub.
    def by_pubs(self, pub_id):
        # Check if exist.
        if does_record_exists(self.cur, 'pub_id', 'Pubs', ('pub_id', pub_id)):
            # Check bar name
            pub_name = (get_data(self.cur, "pub_name", "Pubs", "pub_id", pub_id)[0])

            # Create drinks list for this pub.
            drinks = get_data(self.cur, "drink_name", "Cocktails", "pub_id", pub_id)

            # Create dictionary with results.
            result = []
            for drink in drinks:
                rate = average_rating(self.cur, pub_id)
                result.append({'Pub': pub_name, 'drink_name': drink, 'rating': rate})
            return result
        return {'Status': 'Failed', 'Description': "Pub doesn't exist."}

    # Check rating for cocktail in all bars.
    def by_cocktails(self, drink_name):
        # Check if exists.
        if does_record_exists(self.cur, 'drink_name', 'Cocktails', ('drink_name', drink_name)):
            # Create a list of pubs name and id.
            r = self.cur.execute('''
                                   SELECT b.pub_name, b.pub_id
                                   FROM Cocktails AS c
                                   INNER JOIN Pubs AS b
                                   ON c.pub_id = b.pub_id
                                   WHERE drink_name = "{}"; 
                                   '''.format(drink_name))

            index = []
            names = []
            for _ in r:
                index.append(_['pub_id'])
                names.append(_['pub_name'])

            # Check the rates for cocktails in each pub.
            rating = []
            for _ in index:
                rate_in_pub = self.cur.execute('''
                                       SELECT AVG(rate)
                                       FROM Cocktails
                                       WHERE drink_name = "{}" AND pub_id = {}
                                       '''.format(drink_name, _))
                for _ in rate_in_pub:
                    rating.append(_[0])
            result = []
            for i, _ in enumerate(index):
                result.append({'drink_name': drink_name, 'pub_name': names[i], 'rate': rating[i]})
            return result
        return {'Status': 'Failed', 'Description': "Cocktail doesn't exist."}

    # Show all Cocktails with pubs and rates.
    def all(self):
        a = self.cur.execute('''
                        SELECT c.drink_name, p.pub_name, c.rate
                        FROM Cocktails as c
                        INNER JOIN Pubs AS p
                        ON c.pub_id = p.pub_id;
                        ''')
        result = []
        for _ in a:
            result.append({'drink_name': _['drink_name'], 'pub_name': _['pub_name'], 'rate': _['rate']})
        return result

    # Add new rate for cocktail.
    def rate(self, rate, drink_id):
        # Check if rate is between 1 and 5.
        if rate < 1 or rate > 5:
            return {'Status': 'Failed', 'Description': "Rate need to be between 1 and 5"}
        # Check if exist.
        if does_record_exists(self.cur, 'drink_id', 'Cocktails', ('drink_id', drink_id)):
            # Add new rate to Rating table.
            self.cur.execute('''
                            INSERT INTO Rating (rate_id, drink_id, pub_id, rate)
                            VALUES (?,?,(SELECT pub_id FROM Cocktails WHERE drink_id = {}),?)
                            '''.format(drink_id), (None, drink_id, rate))
            self.con.commit()
            # Update average rate in Cocktails table.
            update_rate(self.cur, self.con, drink_id)
            return {'Status': 'Success'}
        return {'Status': 'Failed', 'Description': "Cocktail doesn't exist."}
