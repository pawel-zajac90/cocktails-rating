from flask import Flask, request
from flask_restful import Api
from config import port
from flask_sqlalchemy import SQLAlchemy
from cocktails_rating.management import PubsManagement, CocktailsManagement
from db.models import PubModel, CocktailModel, RatingModel

app = Flask(__name__)
app.config['secret_key'] = 'thisisthesecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/cocktails.db'
db = SQLAlchemy(app)


@app.route('/pubs', methods = ['GET', 'POST', 'DELETE'])
def pubs():
    if request.method == 'GET':
        data = request.json
        if not data:
            return PubsManagement(db).show_all(model=PubModel)
        else:
            pub_id = data['pub_id']
            return PubsManagement(db).show_by_pubs(model=CocktailModel, model2=RatingModel, pub_id=pub_id)

    elif request.method == 'POST':
        pub_name = request.json['pub_name']
        return PubsManagement(db).add(model=PubModel, pub_name=pub_name)

    elif request.method == 'DELETE':
        pub_id = request.json['pub_id']
        return PubsManagement(db).delete(model=PubModel, pub_id=pub_id)

@app.route('/cocktails', methods = ['GET', 'POST', 'DELETE'])
def cocktails():
    if request.method == 'GET':
        data = request.json
        if not data:
            return 'False'
        else:
            cocktail_name = data["cocktail_name"]
            return CocktailsManagement(db).show(model=CocktailModel, model2=RatingModel, cocktail_name=cocktail_name)

    elif request.method == 'POST':
        data = request.json
        if not data:
            return 'False'
        else:
            cocktail_name = request.json['cocktail_name']
            pub_id = request.json['pub_id']
            return CocktailsManagement(db).add(model=CocktailModel,
                                               cocktail_name=cocktail_name,
                                               pub_id=pub_id)

    elif request.method == 'DELETE':
        pub_id = request.json['pub_id']
        return PubsManagement(db).delete(model=PubModel, pub_id=pub_id)



# api.add_resource(
#     Pubs,
#     '/cocktails-rating/v1.0/pubs',  # GET
#     '/cocktails-rating/v1.0/pubs/<string:pub_name>',  # POST
#     '/cocktails-rating/v1.0/pubs/<int:id>',  # DELETE
#     resource_class_kwargs={'pubs_management': management.PubsManagement}
#                 )
# api.add_resource(
#     Cocktails,
#     '/cocktails-rating/v1.0/cocktails/<int:pub_id>',  # GET
#     '/cocktails-rating/v1.0/cocktails/<string:drink_name>/<int:pub_id>',  # POST
#     '/cocktails-rating/v1.0/cocktails/<int:drink_id>',  # DELETE
#     resource_class_kwargs={'cocktails_management': management.CocktailsManagement}
#                 )
#
# api.add_resource(
#     Rating,
#     '/cocktails-rating/v1.0/rating',  # GET all
#     '/cocktails-rating/v1.0/rating/<int:pub_id>',
#     '/cocktails-rating/v1.0/rating/<string:drink_name>',
#     '/cocktails-rating/v1.0/rating/<int:drink_id>/<int:rate>',
#     resource_class_kwargs={'cocktails_rating': cocktails_rating.Rating}
#                  )
#
# api.add_resource(
#     SignUp,
#     '/cocktails-rating/v1.0/signup/<string:login>/<string:password>/<string:email>',
#     resource_class_kwargs={'registration': auth.Registration}
#                 )
#
# api.add_resource(
#     Login,
#     '/cocktails-rating/v1.0/login',
#     resource_class_kwargs={'login': auth.Log}
#                 )
#
# api.add_resource(
#     Password,
#     '/cocktails-rating/v1.0/forgot-password',
#     '/cocktails-rating/v1.0/forgot-password/<string:login>/<string:email>',
#     resource_class_kwargs={'password': auth.ForgotPassword}
#                 )
#
# app.register_blueprint(api_bp)


if __name__ == '__main__':
    app.run(debug=True, port=5555)
