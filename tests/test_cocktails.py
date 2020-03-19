import requests
from config import port
import sqlite3


class TestCocktails:
    def test_get(self):
        con = sqlite3.connect('../db/cocktails.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        endpoint = '/cocktails-rating/v1.0/cocktails/'
        host = 'localhost:'
        example_pub_id = '1'
        url = 'http://' + host + port + endpoint + example_pub_id

        r = requests.get(url)

        data = r.json()

        result = []
        for _ in data:
            result.append({'drink_id': _['drink_id'], 'drink_name': _['drink_name'], 'pub_id': _['pub_id'],
             'rate': _['rate']})

        db_data = cur.execute('''
                            SELECT * 
                            FROM Cocktails
                            WHERE pub_id = {}'''.format(example_pub_id))

        db_result = []
        for _ in db_data:
            db_result.append({'drink_id': _['drink_id'], 'drink_name': _['drink_name'], 'pub_id': _['pub_id'],
                           'rate': _['rate']})


        assert result == db_result

    def test_post(self):
        con = sqlite3.connect('../db/cocktails.db')
        cur = con.cursor()

        endpoint = '/cocktails-rating/v1.0/pubs'
        host = 'localhost:'
        new_cocktail_name = 'example_cocktail'
        pub_id = '1'
        url = 'http://' + host + port + endpoint + '/' + new_cocktail_name + '/' + pub_id

        i = cur.execute('''
                        SELECT drink_id
                        FROM Cocktails
                        ''')

        ids = []
        for _ in i:
            ids.append(_[0])
        self.newest_cocktail_id = len(ids)

        r = requests.post(url)
        r.json()

        n = cur.execute('''
                        SELECT drink_name 
                        FROM Cocktails
                        WHERE drink_id = {}   
                        '''.format(self.newest_cocktail_id))
        for _ in n:
            db_newest_cocktail_name = _[0]
        assert new_cocktail_name == db_newest_cocktail_name

    def test_delete(self):
        con = sqlite3.connect('../db/cocktails.db')
        cur = con.cursor()

        endpoint = '/cocktails-rating/v1.0/cocktails'
        host = 'localhost:'
        cocktails_to_delete_id = '6'
        url = 'http://' + host + port + endpoint + '/' + cocktails_to_delete_id

        requests.delete(url)

        r = cur.execute('''
                        SELECT 1 
                        WHERE EXISTS 
                        (SELECT {} FROM Cocktails)'''.format(cocktails_to_delete_id))
        for _ in r:
            result = bool(_[0])

        assert result is True

test = TestCocktails()
test.test_get()