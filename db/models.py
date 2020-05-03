from flask_sqlalchemy import SQLAlchemy
from flask import Flask, json, request
from sqlalchemy import ForeignKey


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cocktails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Pubs(db.Model):
    pub_id = db.Column('pub_id', db.Integer, primary_key=True)
    pub_name = db.Column('pub_name', db.String, unique=True)

    def __init__(self, pub_id, name):
        self.pub_id = pub_id
        self.pub_name = name


class Cocktails(db.Model):
    cocktail_id = db.Column(db.Integer, primary_key=True)
    cocktail_name = db.Column(db.String)
    pub_id = db.Column(db.Integer, ForeignKey('pubs.pub_id'))


class Rates(db.Model):
    rate_id = db.Column(db.Integer, primary_key=True)
    pub_id = db.Column(db.Integer, ForeignKey('pubs.pub_id'))
    cocktail_id = db.Column(db.Integer, ForeignKey('cocktails.cocktail_id'))


@app.route('/', methods=['GET'])
def pubs():
    result = []
    for pub in Pubs.query.all():
        result.append({'pub_id': pub.pub_id, 'name': pub.pub_name})
    print(result)
    return json.dumps(result)


@app.route('/delete', methods=['DELETE'])
def delete_last_pub():
    data = request.json
    pub_id = data["pub_id"]
    print(pub_id)
    does_record_exists = bool(Pubs.query.filter_by(pub_id=pub_id).first())
    if not does_record_exists:
        return 'False'
    else:
        Pubs.query.filter(Pubs.pub_id == 10).delete()
        db.session.commit()
        return 'True'


@app.route('/add', methods=['POST'])
def add_new_pub():
    data = Pubs(None, 'example_name')
    print(data)
    db.session.add(data)
    # db.session.commit()
    return 'True'


app.run(port=8080, debug=True)
