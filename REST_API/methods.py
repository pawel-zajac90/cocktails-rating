from flask_restful import Resource
import sqlite3
from authorization.auth import token_required


# Bars management
class Pubs(Resource):
    def __init__(self, pubs_management):
        self.r = pubs_management(sqlite3.connect)

    def get(self):
        return self.r.get_pubs()

    @token_required
    def post(self, pub_name):
        return self.r.post_pub(pub_name)

    @token_required
    def delete(self, id):
        return self.r.delete_pub(id)


# Cocktails management
class Cocktails(Resource):
    def __init__(self, cocktails_management):
        self.r = cocktails_management(sqlite3.connect)

    def get(self, pub_id):
        return self.r.get_cocktails(pub_id)

    @token_required
    def post(self, drink_name, pub_id):
        return self.r.post_cocktail(drink_name, pub_id)

    @token_required
    def delete(self, drink_id):
        return self.r.delete_cocktail(drink_id)


# Rating system
class Rating(Resource):
    def __init__(self, cocktails_rating):
        self.r = cocktails_rating(sqlite3.connect)

    # Get rates of all cocktails in pub if pub_id given
    # or
    # Get rates of single cocktails in all pubs if drink_name given.
    def get(self, pub_id=None, drink_name=None):
        if pub_id is not None:
            return self.r.by_pubs(pub_id)
        elif drink_name is not None:
            return self.r.by_cocktails(drink_name)
        else:
            return self.r.all()

    @token_required
    def patch(self, rate, drink_id):
        return self.r.rate(rate, drink_id)


class Login(Resource):
    def __init__(self, login):
        self.r = login(sqlite3.connect)

    def get(self):
        return self.r.loginto()

    @token_required
    def logout(self):
        pass


class SignUp(Resource):
    def __init__(self, registration):
        self.r = registration(sqlite3.connect)

    def post(self, login, password, email):
        return self.r.new_user(login, password, email)


class Password(Resource):
    def __init__(self, password):
        self.r = password(sqlite3.connect)

    def get(self):
        return "Hello Boss!"

    def patch(self, login, email):
        return self.r.send_new_password(login, email)
