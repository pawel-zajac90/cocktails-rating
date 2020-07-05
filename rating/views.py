from . import rating
from .models import Pub, Cocktail, Rating
from .forms import NewPubForm, NewCocktailForm
from cocktails_rating import db
from flask import redirect, request
from flask import make_response, redirect, url_for, jsonify
from helpers.does_record_exist import does_not_exist, does_exist


# Show all pubs on one site
@rating.route('/', methods=['GET'])
def index():
    if Pub.query.first() is None:
        return does_not_exist

    pubs_list = []
    for pub in Pub.query.all():
        pubs_list.append({'pub_id': pub.id, 'pub_name': pub.name})
    response = make_response(jsonify(pubs=pubs_list), 200)
    return response


# Show pub selected by id
@rating.route('/pub', methods=['GET'])
def pub():
    pub_id = request.json['pub_id']
    record = Cocktail.query.filter_by(pub_id=pub_id).first()
    if record is None:
        return does_not_exist

    cocktails_list = []
    for cocktail in Cocktail.query.filter_by(pub_id=pub_id).all():
        ratings = 0
        for rating in cocktail.ratings:
            ratings += rating.rating
        avg = ratings/len(cocktail.ratings)
        cocktails_list.append({'cocktail_id': cocktail.id, 'cocktail_name': cocktail.name,
                               'description': cocktail.description, 'average_rating': avg})
    response = make_response(jsonify(cocktails=cocktails_list), 200)
    return response


# Show cocktail selected by id from pubs list
@rating.route('/pub/cocktail', methods=['GET'])
def cocktail():
    cocktail_id = request.json['cocktail_id']
    record = Cocktail.query.filter_by(id=cocktail_id).first()

    if record is None:
        return does_not_exist

    response = make_response(jsonify(cocktail_id=record.id, cocktail_name=record.name, pub_id=record.pub_id,
                                     description=record.description), 200)
    return response


# GET list of all cocktails with their avarege rating
# or
# POST new rating.
@rating.route('/rating', methods=['GET', 'POST'])
def cocktails_rating():
    if request.method == 'GET':
        if Cocktail.query.first() is None:
            return does_not_exist()

        cocktails_list = []
        for cocktail in Cocktail.query.all():
            sum_of_ratings = 0
            for rating in cocktail.ratings:
                sum_of_ratings += rating.rating
            try:
                avg = sum_of_ratings / len(cocktail.ratings)
            except ZeroDivisionError:
                avg = 0
            cocktails_list.append(
                {'cocktail_id': cocktail.id, 'cocktail_name': cocktail.name, 'description': cocktail.description,
                 'average_rating': avg})
        response = make_response(jsonify(cocktails_list), 200)
        return response
# To add new rating 'rating' and 'cocktail_id' in request body required.
    elif request.method == 'POST':
        if request.json is None:
            return redirect(url_for('rating.rating'), 400)

        rating = request.json['rating']
        cocktail_id = request.json['cocktail_id']
        record = Cocktail.query.filter_by(id=cocktail_id).first()
        if record is None:
            return does_not_exist

        rate = Rating(cocktail_id=cocktail_id, rating=rating)
        db.session.add(rate)
        db.session.commit()
        return redirect(url_for('rating.rating'), 200)


# Add new pub to database - moderate or higher permission required.
# Request need to contain data in forms.
@rating.route('/add/pub', methods=['POST'])
def add_pub():
    form = NewPubForm()
    name = form.name.data
    if Pub.query.filter_by(name=name).first() is not None:
        return does_exist()
    pub = Pub(name=name)
    db.session.add(pub)
    db.session.commit()
    return redirect(url_for('rating.index'), 300)


# Add new cocktail to database - moderate or higher permission required
# Request need to contain data in forms.
@rating.route('/add/cocktail', methods=['POST'])
def add_cocktail():
    form = NewCocktailForm()
    name = form.name.data
    id = form.pub_id.data
    description = form.description.data
    if Cocktail.query.filter_by(name=name).first() is not None:
        return does_exist()

    elif Pub.query.filter_by(id=id).first() is None:
        return does_not_exist()

    cocktail = Cocktail(name=name, pub_id=id, description=description)
    db.session.add(cocktail)
    db.session.commit()
    return redirect(url_for('rating.index'), 300)



