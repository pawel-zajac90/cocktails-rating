from REST_API import management, rating
from flask_restful import Resource


# Bars maganement
class Pubs(Resource):
    def get(self):
        r = management.Pubs_management()
        content = r.get_pubs()
        return content

    def post(self, pub_name):
        r = management.Pubs_management()
        return r.post_pub(pub_name)

    def delete(self, id):
        r = management.Pubs_management()
        return r.delete_pub(id)


# Cocktails management
class Cocktails(Resource):
    def get(self, id):
        r = management.Cocktails_management()
        return r.get_cocktails(id)

    def post(self, drink_name, pub_id):
        r = management.Cocktails_management()
        return r.post_cocktail(drink_name, pub_id)

    def delete(self, id):
        r = management.Cocktails_management()
        return r.delete_cocktail(id)


# Rating system
class Rating(Resource):
    # Get rates of all cocktails in pub if pub_id given
    # or
    # Get rates of single cocktails in all pubs if drink_name given.
    def get(self, id=None, drink_name=None):
        r = rating.Rating()
        if drink_name == None:
            return r.by_pubs(id)
        else:
            return r.by_cocktails(drink_name)

    def patch(self, rate, drink_id):
        r = rating.Rating()
        return r.rate(rate, drink_id)