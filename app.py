from cocktails_rating import management, cocktails_rating
from flask import Flask, Blueprint
from flask_restful import Api
from config import port
from REST_API.methods import *
from authorization import auth


app = Flask(__name__)
app.config['secret_key'] = 'thisisthesecretkey'
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
    resource_class_kwargs={'cocktails_management': management.CocktailsManagement}
                )

api.add_resource(
    Rating,
    '/cocktails-rating/v1.0/rating',  # GET all
    '/cocktails-rating/v1.0/rating/<int:pub_id>',
    '/cocktails-rating/v1.0/rating/<string:drink_name>',
    '/cocktails-rating/v1.0/rating/<int:drink_id>/<int:rate>',
    resource_class_kwargs={'cocktails_rating': cocktails_rating.Rating}
                 )

api.add_resource(
    SignUp,
    '/cocktails-rating/v1.0/signup/<string:login>/<string:password>/<string:email>',
    resource_class_kwargs={'registration': auth.Registration}
                )

api.add_resource(
    Login,
    '/cocktails-rating/v1.0/login',
    resource_class_kwargs={'login': auth.Log}
                )

api.add_resource(
    Password,
    '/cocktails-rating/v1.0/forgot-password',
    '/cocktails-rating/v1.0/forgot-password/<string:login>/<string:email>',
    resource_class_kwargs={'password': auth.ForgotPassword}
                )

app.register_blueprint(api_bp)


if __name__ == '__main__':
    app.run(debug=True, port=port)
