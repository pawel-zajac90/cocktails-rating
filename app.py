from flask import Flask, Blueprint
from flask_restful import Api
from config import port
from REST_API.methods import *

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)


api.add_resource(
    Pubs,
    '/cocktails-rating/v1.0/pubs',  # GET
    '/cocktails-rating/v1.0/pubs/<string:pub_name>',  # POST
    '/cocktails-rating/v1.0/pubs/<int:id>',  # DELETE
    resource_class_kwargs={'pubs_management': management.PubsManagement}
                )
api.add_resource(
    Cocktails,
    '/cocktails-rating/v1.0/cocktails/<int:pub_id>',  # GET
    '/cocktails-rating/v1.0/cocktails/<string:drink_name>/<int:pub_id>',  # POST
    '/cocktails-rating/v1.0/cocktails/<int:drink_id>',  # DELETE
    resource_class_kwargs= {'cocktails_management': management.CocktailsManagement}
                )
api.add_resource(
    Rating,
    '/cocktails-rating/v1.0/rating', # GET all
    '/cocktails-rating/v1.0/rating/<int:pub_id>',
    '/cocktails-rating/v1.0/rating/<string:drink_name>',
    '/cocktails-rating/v1.0/rating/<int:drink_id>/<int:rate>',
    resource_class_kwargs= {'cocktails_rating': cocktails_rating.Rating}
                 )

app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(port=port)