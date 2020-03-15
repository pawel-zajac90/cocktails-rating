from cocktails_rating import management, cocktails_rating
from flask_restful import Resource


# Bars management
class Pubs(Resource):
    def __init__(self, r : management.PubsManagement()):
        self.r = r

    def get(self):
        return self.r.get_pubs()

    def post(self, pub_name):
        return self.r.post_pub(pub_name)

    def delete(self, id):
        return self.r.delete_pub(id)


# Cocktails management
class Cocktails(Resource):
    def __init__(self):
        self.r = management.CocktailsManagement()

    def get(self, id):
        return self.r.get_cocktails(id)

    def post(self, drink_name, pub_id):
        return self.r.post_cocktail(drink_name, pub_id)

    def delete(self, id):
        return self.r.delete_cocktail(id)


# Rating system
class Rating(Resource):
    # Get rates of all cocktails in pub if pub_id given
    # or
    # Get rates of single cocktails in all pubs if drink_name given.
    def get(self, pub_id=None, drink_name=None):
        r = cocktails_rating.Rating()
        if pub_id is not None:
            return r.by_pubs(pub_id)
        elif drink_name is not None:
            return r.by_cocktails(drink_name)
        else:
            return r.all()

    def patch(self, rate, drink_id):
        r = cocktails_rating.Rating()
        return r.rate(rate, drink_id)
