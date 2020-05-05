from flask_sqlalchemy import SQLAlchemy
from unittest import mock
import requests
import pytest

@pytest.fixture
def url():
    url = 'http://localhost:5555/pubs'
    return url


class TestPubs:
    def test_get_all(self, url):
        r = requests.get(url)
        assert r

    def test_get_by_pubs(self, url):
        data = {"pub_id": "1"}
        r = requests.get(url, json=data)
        assert r

    def test_post(self, url):
        data = {"pub_name": "test_pub"}
        r = requests.post(url, data=data)
        assert r

    def test_post(self, url):
        data = {"pub_id": "7"}
        assert requests.delete(url, json=data)


