import sqlite3
from config import db_path
from cocktails_rating.helpers import does_record_exists
from testowy import TestowaKlasa
import json


# Classes for management of Pubs and Cocktails tables.


class PubsManagement:
    # Get list of all pubs from Pubs table.
    def show(self):
        result = []
        for pub in Pubs.query.all():
            result.append({'id': pub.pub_id, 'name': pub.pub_name})
        return json.dumps(result)

    # Add new pub into Pubs table.
    def add(self, pub_name):
        # Check if exist.
        if not does_record_exists(self.cur, 'pub_name', 'Pubs', ('pub_name', pub_name)):
            # Add new pub.
            self.cur.execute('''
                            INSERT INTO Pubs (pub_id, pub_name) 
                            VALUES (?,?);''', (None, pub_name)
                             )
            self.con.commit()
            return {'Status': 'Success'}
        return {'Status': 'Failed', 'Description': 'Pub already exist'}

    # Delete pub from Pubs table.
    def remove(self, id):
        # Check if exist.
        if does_record_exists(self.cur, 'pub_id', 'Pubs', ('pub_id', id)):
            # Delete pub.
            self.cur.execute('''
                            DELETE FROM Pubs
                            WHERE pub_id = {};'''.format(id)
                             )
            self.con.commit()
            return {'Status': 'Success'}
        return {'Status': 'Failed', 'Description': "Pub doesn't exist."}


class CocktailsManagement:
    def __init__(self, con):
        self.con = con(db_path)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    # Get list of cocktails in single pub from Cocktails table.
    def show(self, pub_id):
        # Check if exist.
        if does_record_exists(self.cur, 'pub_id', 'Pubs', ('pub_id', pub_id)):
            # Get list.
            r = self.cur.execute('''SELECT * 
                                FROM Cocktails 
                                WHERE pub_id = {};
                                '''.format(pub_id))
            content = []
            for _ in r:
                content.append({'drink_id': _['drink_id'], 'drink_name': _['drink_name'], 'pub_id': _['pub_id']})
            return content
        return {'Status': 'Failed', 'Description': "Pub doesn't exist."}

    # Add new cocktail to Cocktails table.
    def add(self, drink_name, pub_id):
        # Check if exist.
        if not does_record_exists(self.cur, ('drink_name', 'pub_id'), 'Cocktails', ('drink_name', drink_name), ('pub_id', pub_id)):
            # Add new cocktail.
            self.cur.execute("""
                            INSERT INTO Cocktails (drink_id, drink_name, pub_id, rate) 
                            VALUES (?,?,?,?);""", (None, drink_name, pub_id, '')
                            )
            self.con.commit()
            return {'Status': 'Success'}
        return {'Status': 'Failed', 'Description': 'Cocktail already exist in this pub.'}

    # Delete cocktail from Cocktails table.
    def remove(self, drink_id):
        # Check if exist.
        if does_record_exists(self.cur, 'drink_id', 'Cocktails', ('drink_id', drink_id)):
            # Delete cocktail.
            self.cur.execute('''
                            DELETE FROM Cocktails 
                            WHERE drink_id = {};'''.format(drink_id)
                             )
            self.con.commit()
            return {'Status': 'Success'}
        return {'Status': 'Failed', 'Description': "Cocktail doesn't exist in this pub."}
