from unittest.mock import Mock
from cocktails_rating.helpers import *
import sys

sys.path.append('/home/coristo/PycharmProjects/cocktailes_rating/cocktails_rating/')

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

def test_check(mock_cur):
    lista = ['1']
    cur_mock.execute.side_effect = lista
    result = check(mock_cur, 'pubs', 'pubs', 1, 1)
    assert result is True

cur_mock = Mock()
print(test_check(mock_cur=cur_mock))