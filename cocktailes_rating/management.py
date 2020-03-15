import sqlite3
from config import db_path
from cocktailes_rating.helpers import check

# Classes for management of Pubs and Cocktails tables.


class PubsManagement:
    def __init__(self):
        self.con = sqlite3.connect(db_path)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    # Get list of all pubs from Pubs table.
    def get_pubs(self):
        r = self.cur.execute('''
                            SELECT *
                            FROM Pubs 
                            ''')
        content = []
        for _ in r:
            content.append({'pub_id': _['pub_id'], 'pub_name': _['pub_name']})
        return content

    # Add new pub into Pubs table.
    def post_pub(self, pub_name):
        # Check if exist.
        if not check(self.cur, column='pub_name', table='Pubs', value1='pub_name', value2= pub_name):
            # Add new pub.
            self.cur.execute('''
                            INSERT INTO Pubs (pub_id, pub_name) 
                            VALUES (?,?);''', (None, pub_name)
                             )
            self.con.commit()
            return {'Status': 'Success'}
        return {'Status': 'Failed', 'Description': 'Pub already exist'}

    # Delete pub from Pubs table.
    def delete_pub(self, id):
        # Check if exist.
        if check(self.cur, column='pub_id', table='Pubs', value1='pub_id', value2=id):
            # Delete pub.
            self.cur.execute('''
                            DELETE FROM Pubs
                            WHERE pub_id = {};'''.format(id)
                             )
            self.con.commit()
            return {'Status': 'Success'}
        return {'Status': 'Failed', 'Description': "Pub doesn't exist."}


class CocktailsManagement:
    def __init__(self):
        self.con = sqlite3.connect(db_path)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    # Get list of cocktails in single pub from Cocktails table.
    def get_cocktails(self, pub_id):
        # Check if exist.
        if check(self.cur, column='pub_id', table='Pubs', value1='pub_id', value2=pub_id):
            # Get list.
            r = self.cur.execute('''SELECT * 
                                FROM Cocktails 
                                WHERE pub_id = {};
                                '''.format(pub_id))
            content = []
            for _ in r:
                content.append({'drink_id': _['drink_id'], 'drink_name': _['drink_name'], 'pub_id': _['pub_id'],
                                'rate': _['rate']})
            return content
        return {'Status': 'Failed', 'Description': "Pub doesn't exist."}

    # Add new cocktail to Cocktails table.
    def post_cocktail(self, drink_name, pub_id):
        # Check if exist.
        if not check(self.cur, column='drink_name', column2='pub_id', table='Cocktails',
                     value1='drink_name', value2=drink_name, value3='pub_id', value4=pub_id):
            # Add new cocktail.
            self.cur.execute("""
                            INSERT INTO Cocktails (drink_id, drink_name, pub_id, rate) 
                            VALUES (?,?,?,?);""", (None, drink_name, pub_id, '')
                            )
            self.con.commit()
            return {'Status': 'Success'}
        return {'Status': 'Failed', 'Description': 'Cocktail already exist in this pub.'}

    # Delete cocktail from Cocktails table.
    def delete_cocktail(self, drink_id):
        # Check if exist.
        if check(self.cur, column='drink_id', table='Cocktails', value1='drink_id', value2=drink_id):
            # Delete cocktail.
            self.cur.execute('''
                            DELETE FROM Cocktails 
                            WHERE drink_id = {};'''.format(drink_id)
                             )
            self.con.commit()
            return {'Status': 'Success'}
        return {'Status': 'Failed', 'Description': "Cocktail doesn't exist in this pub."}


