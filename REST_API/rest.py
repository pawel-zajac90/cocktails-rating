from flask import Flask, Blueprint
from flask_restful import Resource, Api
from REST_API import management
from config import port

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)


# Bars maganement
class Bars(Resource):
    def get(self):
        r = management.Management()
        content = r.get_bars()
        return content

    def post(self, bar_name):
        r = management.Management()
        return r.post_bar(bar_name)

    def delete(self, id):
        r = management.Management()
        return r.delete_bar(id)

# Cocktails management
class Cocktails(Resource):
    def get(self, id):
        r = management.Management()
        return r.get_cocktails(id)

    def post(self, drink_name, bar_id):
        r = management.Management()
        return r.post_cocktail(drink_name, bar_id)

    def delete(self, id):
        r = management.Management()
        return r.delete_cocktail(id)

# Rating system
class Rating(Resource):
    # GET average rating of all cocktails in Bar
    def get(self, id=None, drink_name=None):
        if drink_name == None:
            r = management.Rating()
            return r.all_from_bar(id)
        else:
            r = management.Rating()
            return r.one_cocktail(drink_name)

    def patch(self, rate, drink_id):
        r = management.Rating()
        return r.rate(rate, drink_id)



api.add_resource(Bars,
                    '/cocktails-rating/v1.0/bars',
                    '/cocktails-rating/v1.0/bars/<string:bar_name>',
                    '/cocktails-rating/v1.0/bars/<int:id>')
api.add_resource(Cocktails,
                    '/cocktails-rating/v1.0/bars/cocktails/<int:id>',
                    '/cocktails-rating/v1.0/bars/cocktails/<string:drink_name>/<int:bar_id>',
                    '/cocktails-rating/v1.0/bars/cocktails/<int:id>/<int:bar_id>')
api.add_resource(Rating,
                    '/cocktails-rating/v1.0/rating/<int:id>',
                    '/cocktails-rating/v1.0/rating/<string:drink_name>',
                    '/cocktails-rating/v1.0/rating/<int:drink_id>/<int:rate>/')


app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(port=port)