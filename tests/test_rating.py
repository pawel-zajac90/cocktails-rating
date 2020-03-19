import requests
from config import port
import sqlite3


class TestRating:
    def test_get_by_pubs(self):
        con = sqlite3.connect('../db/cocktails.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        endpoint = '/cocktails-rating/v1.0/rating/'
        host = 'localhost:'
        example_pub_id = '1'
        url = 'http://' + host + port + endpoint + example_pub_id

        r = requests.get(url)

        data = r.json()
        result = []
        db_results = []
        for _ in data:
            result.append({'Pub': _['Pub'], 'drink_name': _['drink_name'], 'rating': _['rating']})

        db_cocktails = cur.execute('''
                            SELECT drink_name
                            FROM Cocktails 
                            WHERE pub_id = {};'''.format(example_pub_id))
        db_cocktails_list = []
        for _ in db_cocktails:
            db_cocktails_list.append(_['drink_name'])

        db_name = cur.execute('''
                                SELECT pub_name
                                FROM Pubs
                                WHERE pub_id = {};
                                '''.format(example_pub_id))
        for _ in db_name:
            db_pub_name = _['pub_name']

        for _ in db_cocktails_list:
            avg = cur.execute('''
                                SELECT AVG(rate) 
                                FROM Rating
                                WHERE pub_id = "{}"
                                '''.format(example_pub_id)
                                 )
            for a in avg:
                rate = round(a[0])
            db_results.append({'Pub': db_pub_name, 'drink_name': _, 'rating': rate})
        assert result == db_results


    def test_get_by_cocktails(self):
        con = sqlite3.connect('../db/cocktails.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        endpoint = '/cocktails-rating/v1.0/rating/'
        host = 'localhost:'
        cocktail_name = 'Cocktail1'
        url = 'http://' + host + port + endpoint + cocktail_name

        d = requests.get(url)
        data = d.json()
        result = []
        for _ in data:
            result.append(_)

        r = cur.execute('''
                        SELECT b.pub_name, b.pub_id
                        FROM Cocktails AS c
                        INNER JOIN Pubs AS b
                        ON c.pub_id = b.pub_id
                        WHERE drink_name = "{}"; 
                        '''.format(cocktail_name))
        index = []
        names = []
        for _ in r:
            index.append(_['pub_id'])
            names.append(_['pub_name'])
        rating = []
        for _ in index:
            rate_in_pub = cur.execute('''
                                   SELECT AVG(rate)
                                   FROM Cocktails
                                   WHERE drink_name = "{}" AND pub_id = {}
                                   '''.format(cocktail_name, _))
            for _ in rate_in_pub:
                rating.append(_[0])
        db_result = []
        for i, _ in enumerate(index):
            db_result.append({'drink_name': cocktail_name, 'pub_name': names[i], 'rate': rating[i]})
        assert result == db_result



    def test_get_all(self):
        con = sqlite3.connect('../db/cocktails.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        endpoint = '/cocktails-rating/v1.0/rating'
        host = 'localhost:'
        url = 'http://' + host + port + endpoint

        d = requests.get(url)
        data = d.json()
        result = []
        for _ in data:
            result.append(_)

        db_data = cur.execute('''
                                SELECT c.drink_name, p.pub_name, c.rate
                                FROM Cocktails as c
                                INNER JOIN Pubs AS p
                                ON c.pub_id = p.pub_id;
                                ''')
        db_result = []
        for _ in db_data:
            db_result.append({'drink_name': _['drink_name'], 'pub_name': _['pub_name'], 'rate': _['rate']})
        assert result == db_result

    def test_patch(self):
        con = sqlite3.connect('../db/cocktails.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        endpoint = '/cocktails-rating/v1.0/rating'
        host = 'localhost:'
        cocktail_id = '1'
        rate = '4'
        url = 'http://' + host + port + endpoint + '/' + cocktail_id + '/' + rate
        # Check how much rates we've got.
        nr = cur.execute('''
                            SELECT COUNT(rate)
                            FROM Rating
                            WHERE drink_id = {}
                            '''.format(cocktail_id))
        number_of_ratings_before = []
        for _ in nr:
            number_of_ratings_before.append(_[0])

        d = requests.patch(url)

        nr = cur.execute('''
                            SELECT COUNT(rate)
                            FROM Rating
                            WHERE drink_id = {}
                            '''.format(cocktail_id))
        number_of_ratings_after = []
        for _ in nr:
            number_of_ratings_after.append(_[0])
        assert number_of_ratings_before < number_of_ratings_after
