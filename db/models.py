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
    rating = db.Column(db.Integer)
    ratings_quantity = db.Column(db.Integer)

    def __init__(self, cocktail_name, pub_id):
        self.cocktail_name = cocktail_name
        self.pub_id = pub_id
        self.cocktail_id = None


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
    print(result)
    return json.dumps(result)



@app.route('/delete', methods=['DELETE'])
def delete_last_pub():
    data = request.json
    pub_id = data["pub_id"]
    record = PubModel.query.filter_by(pub_id=pub_id).first()
    does_record_exists = bool(db.session.query(PubModel.pub_id).filter_by(pub_id=pub_id).scalar())
    if not does_record_exists:
        return 'False'
    else:
        db.session.query(PubModel).filter_by(pub_id=pub_id).delete()
        db.session.commit()
        return 'True'


@app.route('/add', methods=['POST'])
def add_new_pub():
    data = Pubs('example_name')
    db.session.add(data)
    db.session.commit()
    return 'True'

app.run(debug=True, port=8080)