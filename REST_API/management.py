import sqlite3
from config import db_path


class Management:
    def __init__(self):
        self.con = sqlite3.connect(db_path)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    def get_bars(self):
        r = self.cur.execute('''
                            SELECT *
                            FROM Bars 
                            ''')
        contents = []
        for _ in r:
            contents.append({'bar_id': _['bar_id'], 'bar_name': _['bar_name']})
        return contents

    def post_bar(self, bar_name):
        self.cur.execute('''
                        INSERT INTO Bars (bar_id, bar_name) 
                        VALUES (?,?);''', (None, bar_name)
                         )
        self.con.commit()
        return {'Status': 'Success'}

    def delete_bar(self, id):
        self.cur.execute('''
                        DELETE FROM Bars 
                        WHERE bar_id = {};'''.format(id)
                         )
        self.con.commit()
        return {'Status': 'Success'}

    def get_cocktails(self, bar_id):
        r = self.cur.execute('''SELECT * 
                            FROM Cocktails 
                            WHERE bar_id = {};
                            '''.format(bar_id))
        content = []
        for _ in r:
            content.append({'drink_id': _['drink_id'], 'drink_name': _['drink_name'], 'bar_id': _['bar_id'],
                            'rate': _['rate']})
        return content

    def post_cocktail(self, drink_name, bar_id):
        self.cur.execute("""
                        INSERT INTO Cocktails (drink_id, drink_name, bar_id, rate) 
                        VALUES (?,?,?,?);""", (None, drink_name, bar_id, '')
                        )
        self.con.commit()
        return {'Status': 'Success'}

    def delete_cocktail(self, drink_id):
        self.cur.execute('''
                        DELETE FROM Cocktails 
                        WHERE drink_id = {};'''.format(drink_id)
                         )
        self.con.commit()
        return {'Status': 'Success'}

class Rating:
    def __init__(self):
        self.con = sqlite3.connect(db_path)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    # GET values from one column with one WHERE condition and return as list
    def get_data(self, column, table, value1, value2):
        data = self.cur.execute('''
                                    SELECT {}
                                    FROM {}
                                    WHERE {} = {}
                                    '''.format(column, table, value1, value2)
                                )
        list = []
        for _ in data:
            list.append(_[column])
        return list

    # Get average rating for cocktail
    def averge_rating(self, value1=None, value2=None):
        if value2 == None:
            rating = self.cur.execute('''
                                        SELECT AVG(rate) 
                                        FROM Rating
                                        WHERE bar_id = "{}"
                                        '''.format(value1)
                                      )
        else:
            rating = self.cur.execute('''
                                        SELECT AVG(rate) 
                                        FROM Rating
                                        WHERE drink_id = "{}"
                                        AND bar_id = {};
                                        '''.format(value1, value2)
                                      )
        for _ in rating:
            result = round(_[0])
        return result

    # Check ratings for all cocktails in bar
    def all_from_bar(self, bar_id):
        # Check bar name
        bar_name = (self.get_data("bar_name", "Bars", "bar_id", bar_id)[0])

        # Create drinks list for this bar
        drinks = self.get_data("drink_name", "Cocktails", "bar_id", bar_id)

        # Create dictionary with results
        result = []
        for drink in drinks:
            rate = self.averge_rating(bar_id)
            result.append({'Bar': bar_name, 'drink_name': drink, 'rating': rate})
        return result

    # Check rating for cocktail in all bars
    def one_cocktail(self, drink_name):
        r = self.cur.execute('''
                               SELECT b.bar_name, b.bar_id
                               FROM Cocktails AS c
                               INNER JOIN Bars AS b
                               ON c.bar_id = b.bar_id
                               WHERE drink_name = "{}"; 
                               '''.format(drink_name))

        index = []
        names = []
        for _ in r:
            index.append(_['bar_id'])
            names.append(_['bar_name'])

        rating = []
        for _ in index:
            rate_in_bar = self.cur.execute('''
                                   SELECT AVG(rate)
                                   FROM Rating
                                   WHERE drink_name = "{}" AND bar_id = {}
                                   '''.format(drink_name, _))
            for _ in rate_in_bar:
                rating.append(_[0])
        result = []
        for i, _ in enumerate(index):
            result.append({'drink_name': drink_name, 'bar_name': names[i], 'rate': rating[i]})
        return result

    def rate(self,rate, drink_id):
        self.cur.execute('''
                        INSERT INTO Rating (rate_id, drink_id, bar_id, rate)
                        VALUES (?,?,(SELECT bar_id FROM Cocktails WHERE drink_id = {}),?)
                        '''.format(drink_id), (None, drink_id, rate))
        self.con.commit()
        return {'Status': 'Success'}



