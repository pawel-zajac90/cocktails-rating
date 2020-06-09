from flask_login import UserMixin, AnonymousUserMixin
from cocktails_rating import db


class Pub(db.Model):
    __tablename__ = 'pubs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    cocktails = db.relationship('Cocktail', backref='pubs')


class Cocktail(db.Model):
    __tablename__ = 'cocktails'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    pub_id = db.Column(db.Integer, db.ForeignKey('pubs.id'))
    description = db.Column(db.Text)
    ratings = db.relationship('Rating', backref='cocktails')


class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    cocktail_id = db.Column(db.Integer, db.ForeignKey('cocktails.id'))
    rating = db.Column(db.Integer)


class Permission:
    SHOW = 1
    RATE = 2
    MODERATE = 4
    ADMIN = 8


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

