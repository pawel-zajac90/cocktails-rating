import pytest
import mock
from REST_API.methods import *

m1 = mock.Mock(name='pub_id')
m1.return_value = 2
m2 = mock.Mock(name='drink_name')
m2.return_value = 'Cocktail'

#print(m.some_attribute.return_val ue = 42)

class Resource_test:
    def get_test(self):
        m3 = mock.Mock(name='Rating')
        m3.side_effect = cocktails_rating.Rating()
        r = cocktails_rating.Rating()
        Rating().get(m1)

klasa = Resource_test()
klasa.get_test()
