from . import rating
from .models import Pub, Cocktail, Rating
import json
from .forms import NewPubForm
from cocktails_rating import db
from flask import redirect, request
from flask_sqlalchemy import SQLAlchemy


# Show all pubs on one site
@rating.route('/', methods=['GET'])
def index():
    pubs_list = []
    for pub in Pub.query.all():
        pubs_list.append({'pub_id': pub.id, 'pub_name': pub.name})
    return json.dumps(pubs_list)


# Show pub selected by id
@rating.route('/pub/<int:pub_id>', methods=['GET'])
def pub(pub_id):
    cocktails_list = []
    for cocktail in Cocktail.query.filter_by(pub_id=pub_id).all():
        ratings = 0
        for rating in cocktail.ratings:
            ratings += rating.rating
        avg = ratings/len(cocktail.ratings)
        cocktails_list.append({'cocktail_id': cocktail.id, 'cocktail_name': cocktail.name, 'average_rating': avg})
    return json.dumps(cocktails_list)


# Show cocktail selected by id from pubs list
@rating.route('/cocktail/<int:cocktail_id>', methods=['GET', 'POST'])
def cocktail(cocktail_id):
    if request.method == 'GET':
        record = Cocktail.query.filter_by(id=cocktail_id).first()
        response = {'cocktail_id': record.id, 'cocktail_name': record.name, 'pub_id': record.pub_id,
                    'description': record.description}
        return json.dumps(response)
    elif request.method == 'POST':
        rating = request.json['rating']
        cocktail_id = request.json['cocktail_id']
        if Cocktail.query.filter_by(id=cocktail_id).first() is None:
            return json.dumps({'Status': 'Error, record does not exist.'})
        rating = Rating(cocktail_id=cocktail_id, rating=rating)
        db.session.add(rating)
        db.session.commit()
        return json.dumps({'Status': 'Rating added succesfully.'})


# @rating.route('/add/pub', methods=['GET', 'POST'])
# def moderate():
#     form = NewPubForm()
#     name = form.name.data
#     if Pub.query.filter_by(name=name).first() is not None:
#         return json.dumps({'Status': 'Error, this pub already exist'})
#     pub = Pub(name=name)
#     db.session.add(pub)
#     db.session.commit()
#     return json.dumps({'Status': 'Pub added succesfully.'})



