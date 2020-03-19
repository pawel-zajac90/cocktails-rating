from cocktails_rating import management, cocktails_rating
from flask_restful import Resource
import sqlite3


# Bars management
class Pubs(Resource):
    def __init__(self, pubs_management):
        self.r = pubs_management(sqlite3.connect)

    def get(self):
        return self.r.get_pubs()

    def post(self, pub_name):
        return self.r.post_pub(pub_name)

    def delete(self, id):
        return self.r.delete_pub(id)


# Cocktails management
class Cocktails(Resource):
    def __init__(self, cocktails_management):
        self.r = cocktails_management(sqlite3.connect)

    def get(self, drink_id):
        return self.r.get_cocktails(drink_id)

    def post(self, drink_name, pub_id):
        return self.r.post_cocktail(drink_name, pub_id)

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

    def patch(self, rate, drink_id):
        return self.r.rate(rate, drink_id)
