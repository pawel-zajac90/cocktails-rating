import requests
from config import port
import sqlite3


class TestPubs:
    def test_get(self):
        con = sqlite3.connect('../db/cocktails.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        endpoint = '/cocktails-rating/v1.0/pubs'
        host = 'localhost:'
        url = 'http://' + host + port + endpoint

        r = requests.get(url)

        data = r.json()

        result = []
        for _ in data:
            result.append({'pub_id': _['pub_id'], 'pub_name': _['pub_name']})

        db_data = cur.execute('''
                            SELECT * 
                            FROM Pubs''')

        db_result = []
        for _ in db_data:
            db_result.append({'pub_id': _['pub_id'], 'pub_name': _['pub_name']})


        assert result == db_result

    def test_post(self):
        con = sqlite3.connect('../db/cocktails.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        endpoint = '/cocktails-rating/v1.0/pubs'
        host = 'localhost:'
        new_pub_name = 'example'
        url = 'http://' + host + port + endpoint + '/' + new_pub_name

        i = cur.execute('''
                        SELECT pub_id
                        FROM Pubs
                        ''')

        ids = []
        for _ in i:
            ids.append(_['pub_id'])
        self.newest_pub_id = len(ids)

        r = requests.post(url)
        r.json()

        n = cur.execute('''
                        SELECT pub_name 
                        FROM Pubs 
                        WHERE pub_id = {}   
                        '''.format(self.newest_pub_id))
        for _ in n:
            db_newest_pub_name = _['pub_name']
        assert new_pub_name == db_newest_pub_name

    def test_delete(self):
        con = sqlite3.connect('../db/cocktails.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        endpoint = '/cocktails-rating/v1.0/pubs'
        host = 'localhost:'
        pubs_to_delete_id = '6'
        url = 'http://' + host + port + endpoint + '/' + pubs_to_delete_id

        requests.delete(url)

        r = cur.execute('''
                        SELECT 1 
                        WHERE EXISTS 
                        (SELECT {} FROM Pubs)'''.format(pubs_to_delete_id))
        for _ in r:
            result = bool(_[0])

        assert result is True
