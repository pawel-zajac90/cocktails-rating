from unittest.mock import Mock

from cocktails_rating.helpers import check


def test_check():
    cursor_mock = Mock()

    cursor_mock.execute.side_effect = lambda _ : []
    check(cursor_mock, 'pubs', 'pubs', 1, 1)

    cursor_mock.execute.assert_called()
