from . import rating
from app.models import Pub, Cocktail, Rating
from cocktails_rating import db
from flask import request
from flask import make_response, redirect, url_for, jsonify
from helpers.errors import does_not_exist, does_exist, no_data
from helpers.average import average


# Show all pubs on one site
@rating.route('/', methods=['GET'])
def index():
    if Pub.query.first() is None:
        return does_not_exist()
    result = [{'pub_id': pub.id, 'pub_name': pub.name} for pub in Pub.query.all()]
    response = make_response(jsonify(pubs=result), 200)
    return response


# Show pub selected by id
@rating.route('/pub', methods=['GET'])
def pub():
    try:
        pub_id = request.json['pub_id']
    except TypeError:
        return no_data()

    if Cocktail.query.filter_by(pub_id=pub_id).first() is None:
        return does_not_exist()

    cocktails_list = []
    for cocktail in Cocktail.query.filter_by(pub_id=pub_id).all():
        sum_of_ratings = sum(rating.rating for rating in cocktail.ratings)
        avg = average(sum_of_ratings, cocktail.ratings)
        cocktails_list.append({'cocktail_id': cocktail.id, 'cocktail_name': cocktail.name,
                               'description': cocktail.description, 'average_rating': avg})
    response = make_response(jsonify(cocktails=cocktails_list), 200)
    return response


# GET list of all cocktails with their avarege rating
# or
# POST new rating.
@rating.route('/rating', methods=['GET', 'POST'])
def cocktails_rating():
    if request.method == 'GET':
        # Check if cocktails table isn't empty.
        if Cocktail.query.first() is None:
            return does_not_exist()

# If cocktail id in request body: return data for only one cocktail.
        try:
            cocktail_id = request.json['cocktail_id']
            record = Cocktail.query.filter_by(id=cocktail_id).first()
            if record is None:
                return does_not_exist()
            else:
                response = make_response(jsonify(cocktail_id=record.id, cocktail_name=record.name, pub_id=record.pub_id,
                                                 description=record.description), 200)
                return response

        except (KeyError, TypeError):
            pass

# Show full rating.
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
            return redirect(url_for('api.cocktails_rating'), 300)
        try:
            rating = request.json['rating']
            cocktail_id = request.json['cocktail_id']
        except (KeyError, ValueError):
            return no_data()

        if Cocktail.query.filter_by(id=cocktail_id).first() is None:
            return does_not_exist

        rate = Rating(cocktail_id=cocktail_id, rating=rating)
        db.session.add(rate)
        db.session.commit()
        return redirect(url_for('api.cocktails_rating'), 300)


# Add new pub to database - moderate or higher permission required.
# New pub name in request body required.
@rating.route('/add/pub', methods=['POST'])
def add_pub():
    try:
        name = request.json['pub_name']
    except TypeError:
        return no_data()

    if Pub.query.filter_by(name=name).first() is not None:
        return does_exist()

    pub = Pub(name=name)
    db.session.add(pub)
    db.session.commit()
    return redirect(url_for('api.index'), 300)


# Add new cocktail to database - moderate or higher permission required
# Cocktail name, pub id and cocktail description in request body required.
@rating.route('/add/cocktail', methods=['POST'])
def add_cocktail():
    try:
        name = request.json['cocktail_name']
        id = request.json['pub_id']
        description = request.json['description']
    except TypeError:
        return no_data()

    if Cocktail.query.filter_by(name=name).first() is not None:
        return does_exist()

    elif Pub.query.filter_by(id=id).first() is None:
        return does_not_exist()

    cocktail = Cocktail(name=name, pub_id=id, description=description)
    db.session.add(cocktail)
    db.session.commit()
    return redirect(url_for('api.index'), 300)
