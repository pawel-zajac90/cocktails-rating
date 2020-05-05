from flask_sqlalchemy import SQLAlchemy
from flask import Flask, json, request, current_app
from sqlalchemy import ForeignKey, func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cocktails.db'
db = SQLAlchemy(app)
# db = current_app.config['SQLALCHEMY_DATABASE_URI']


class PubModel(db.Model):
    __tablename__ = 'Pubs'
    pub_id = db.Column('pub_id', db.Integer, primary_key=True)
    pub_name = db.Column('pub_name', db.String, unique=True)

    def __init__(self, pub_name):
        self.pub_id = None
        self.pub_name = pub_name


class CocktailModel(db.Model):
    __tablename__ = 'Cocktails'
    cocktail_id = db.Column(db.Integer, primary_key=True)
    cocktail_name = db.Column(db.String)
    pub_id = db.Column(db.Integer, ForeignKey('pubs.pub_id'))

    def __init__(self, cocktail_name, pub_id):
        self.cocktail_id = None
        self.cocktail_name = cocktail_name
        self.pub_id = pub_id


class RatingModel(db.Model):
    __tablename__ = 'Ratings'
    rate_id = db.Column(db.Integer, primary_key=True)
    cocktail_id = db.Column(db.Integer, ForeignKey('cocktails.cocktail_id'))
    rating = db.Column(db.Integer)

    def __init__(self, cocktail_id, rating):
        self.rate_id = None
        self.cocktail_id = cocktail_id
        self.rating = rating


@app.route('/', methods=['GET'])
def pubs():
    result = {}
    for pub in db.session.query(PubModel).all():
        result.update({pub.pub_id: {'pub_name': pub.pub_name}})
    value = db.session.query(PubModel).filter_by(pub_id=2, pub_name='Pub1').first()
    print(value.pub_name)
    return json.dumps(result)


@app.route('/delete', methods=['DELETE'])
def delete_last_pub():
    data = request.json
    if not data:
        return 'false'
    else: return 'true'

@app.route('/add', methods=['POST'])
def add_new_pub():
    data = RatingModel(2, 7)
    db.session.add(data)
    db.session.commit()
    return 'True'
