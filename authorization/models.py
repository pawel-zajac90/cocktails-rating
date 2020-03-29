import crypt
from hmac import compare_digest as compare_hash


class User:
    def __init__(self, login, password, email):
        self.login = login
        self.password = password
        self.email = email

    def profile(self):
        profile = {
                'login': self.login,
                'password': self.password,
                'email': self.email
                }
        return profile
