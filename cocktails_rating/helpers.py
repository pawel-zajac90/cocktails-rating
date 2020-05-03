# Helpers for management.py and rating.py.


# Check if is record exist and return 1 if True.
def does_record_exists(cur, column, table, *fields):
    """
        values : tuple with following content (name, value)
    """

    fields_query = ' AND '.join(['{} = "{}"'.format(name, value) for name, value in fields])
    result = cur.execute('''SELECT COUNT ({}) 
                         FROM {} WHERE {}
                        '''.format(column, table, fields_query))

    for r in result:
        return bool(r[0])


# GET values from one column with one WHERE condition and return as list.
def get_data(cur, column, table, value1, value2):
    data = cur.execute('''
                            SELECT {}
                            FROM {}
                            WHERE {} = {}
                            '''.format(column, table, value1, value2)
                            )
    list = []
    for _ in data:
        list.append(_[column])
    return list


# Get average rating.
def average_rating(cur, value1):
    rating = cur.execute('''
                        SELECT AVG(rate) 
                        FROM Rating
                        WHERE pub_id = "{}"
                        '''.format(value1)
                        )
    for _ in rating:
        result = round(float(_[0]))
    return result


# Update average rating in Cocktails table using Rating table.
def update_rate(cur, con, drink_id):
    v = cur.execute('''
                   SELECT AVG(rate) 
                   FROM Rating 
                   WHERE drink_id = {};
                   '''.format(drink_id)
                   )
    for _ in v:
        avg = round(float(_[0]))
    cur.execute('''
                 UPDATE Cocktails 
                 SET rate = {} 
                 WHERE drink_id = "{}"
                 '''.format(avg, drink_id))
    con.commit()
    return True
