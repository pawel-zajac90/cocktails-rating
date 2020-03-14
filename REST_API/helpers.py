# Helpers for management.py and rating.py.


# Check if is record exist and return 1 if True.
def check(cur, column, table, value1, value2, column2=None, value3=None, value4=None):
    # Check for one condition.
    if value3 == None:
        r = cur.execute('''SELECT 1
                        WHERE EXISTS
                        (SELECT {} FROM {} WHERE {} = "{}")
                        '''.format(column, table, value1, value2)
                        )
    # Check for two conditions.
    else:
        r = cur.execute('''SELECT 1
                        WHERE EXISTS
                        (SELECT {} {} FROM {} WHERE {} = "{}" AND {} = "{}")
                        '''.format(column, column2, table, value1, value2, value3, value4)
                        )
    for _ in r:
        return True if (_[0]) else False

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
        result = round(_[0])
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
        avg = round(_[0])
    cur.execute('''
                 UPDATE Cocktails 
                 SET rate = {} 
                 WHERE drink_id = "{}"
                 '''.format(avg, drink_id))
    con.commit()
    return
