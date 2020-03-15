from unittest.mock import Mock
import sys
from REST_API.methods import *


def test_Pubs():
    management_mock = Mock()
    pubs = Pubs(management_mock)
    management_mock.get.side_effect = True
    pubs.get()
    management_mock.get.assert_called()


test_Pubs()