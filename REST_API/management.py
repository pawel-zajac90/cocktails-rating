import sqlite3
from config import db_path


def check(cur, column, table, value1, value2, column2=None, value3=None, value4=None):
    if value3 == None:
        r = cur.execute('''SELECT 1
                        WHERE EXISTS
                        (SELECT {} FROM {} WHERE {} = "{}")
                        '''.format(column, table, value1, value2)
                        )
    else:
        r = cur.execute('''SELECT 1
                        WHERE EXISTS
                        (SELECT {} {} FROM {} WHERE {} = "{}" AND {} = "{}")
                        '''.format(column, column2, table, value1, value2, value3, value4)
                        )
    for _ in r:
        return True if (_[0]) else False

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
        content = []
        for _ in r:
            content.append({'bar_id': _['bar_id'], 'bar_name': _['bar_name']})
        return content

    def post_bar(self, bar_name):
        if not check(self.cur, column='bar_name', table='Bars', value1='bar_name', value2=bar_name):
            self.cur.execute('''
                            INSERT INTO Bars (bar_id, bar_name) 
                            VALUES (?,?);''', (None, bar_name)
                             )
            self.con.commit()
            return {'Status': 'Success'}
        return {'Status': 'Failed', 'Description': 'Pub already exist'}

    def delete_bar(self, id):
        if check(self.cur, column='bar_id', table='Bars', value1='bar_id', value2=id):
            self.cur.execute('''
                            DELETE FROM Bars 
                            WHERE bar_id = {};'''.format(id)
                             )
            self.con.commit()
            return {'Status': 'Success'}
        return {'Status': 'Failed', 'Description': "Pub doesn't exist."}

    def get_cocktails(self, bar_id):
        if check(self.cur, column='bar_id', table='Bars', value1='bar_id', value2=bar_id):
            r = self.cur.execute('''SELECT * 
                                FROM Cocktails 
                                WHERE bar_id = {};
                                '''.format(bar_id))
            content = []
            for _ in r:
                content.append({'drink_id': _['drink_id'], 'drink_name': _['drink_name'], 'bar_id': _['bar_id'],
                                'rate': _['rate']})
            return content
        return {'Status': 'Failed', 'Description': "Pub doesn't exist."}

    def post_cocktail(self, drink_name, bar_id):
        if not check(self.cur, column='drink_name',column2='bar_id', table='Cocktails',
                          value1='drink_name', value2=drink_name, value3='bar_id', value4=bar_id):
            self.cur.execute("""
                            INSERT INTO Cocktails (drink_id, drink_name, bar_id, rate) 
                            VALUES (?,?,?,?);""", (None, drink_name, bar_id, '')
                            )
            self.con.commit()
            return {'Status': 'Success'}
        return {'Status': 'Failed', 'Description': 'Cocktail already exist in this pub.'}

    def delete_cocktail(self, drink_id):
        if check(self.cur, column='drink_id', table='Cocktails', value1='drink_id', value2=drink_id):
            self.cur.execute('''
                            DELETE FROM Cocktails 
                            WHERE drink_id = {};'''.format(drink_id)
                             )
            self.con.commit()
            return {'Status': 'Success'}
        return {'Status': 'Failed', 'Description': "Cocktail doesn't exist in this pub."}


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
        if check(self.cur, column='bar_id', table='Bars', value1='bar_id', value2=bar_id):
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
        return {'Status': 'Failed', 'Description': "Pub doesn't exist."}

    # Check rating for cocktail in all bars
    def one_cocktail(self, drink_name):
        if check(self.cur, column='drink_name', table='Cocktails', value1='drink_name', value2=drink_name):
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
        return {'Status': 'Failed', 'Description': "Cocktail doesn't exist."}

    def rate(self,rate, drink_id):
        if check(self.cur, column='drink_id', table='Cocktails', value1='drink_id', value2=drink_id):
            self.cur.execute('''
                            INSERT INTO Rating (rate_id, drink_id, bar_id, rate)
                            VALUES (?,?,(SELECT bar_id FROM Cocktails WHERE drink_id = {}),?)
                            '''.format(drink_id), (None, drink_id, rate))
            self.con.commit()
            return {'Status': 'Success'}
        return {'Status': 'Failed', 'Description': "Cocktail doesn't exist."}


