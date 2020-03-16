from unittest.mock import Mock
import sys
from REST_API.methods import Pubs


def test_pubs_get_method():
    management_mock = Mock()
    test_pub = Mock()

    pubs = Pubs(management_mock)
    management_mock.get_pubs.side_effect = lambda : test_pub

    pub = pubs.get()

    assert pub == test_pub
    management_mock.get_pubs.assert_called()
