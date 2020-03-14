from flask import Flask, Blueprint
from flask_restful import Api
from config import port
from REST_API.methods import *

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(
    Pubs,
    '/cocktails-rating/v1.0/pubs',
    '/cocktails-rating/v1.0/pubs/<string:pub_name>',
    '/cocktails-rating/v1.0/pubs/<int:id>'
                )
api.add_resource(
    Cocktails,
    '/cocktails-rating/v1.0/cocktails/<int:id>',
    '/cocktails-rating/v1.0/cocktails/<string:drink_name>/<int:pub_id>',
    '/cocktails-rating/v1.0/cocktails/<int:id>/<int:pub_id>'
                )
api.add_resource(
    Rating,
    '/cocktails-rating/v1.0/rating/<int:id>',
    '/cocktails-rating/v1.0/rating/<string:drink_name>',
    '/cocktails-rating/v1.0/rating/<int:drink_id>/<int:rate>'
                 )


app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(port=port)