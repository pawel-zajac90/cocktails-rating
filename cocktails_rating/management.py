import json
from sqlalchemy import func


class PubsManagement:
    def __init__(self, db):
        self.db = db

    def show_all(self, model):
        result = {}
        for pub in self.db.session.query(model).all():
            result.update({pub.pub_id: {'pub_name': pub.pub_name}})
        return json.dumps(result)

    def show_by_pubs(self, model, model2, pub_id):
        result = {}
        for cocktail in self.db.session.query(model).filter_by(pub_id=pub_id).all():
            avg_rating = self.db.session.query(func.avg(model2.rating)).filter_by(
                                                                    cocktail_id=cocktail.cocktail_id).first()
            ratings_quantity = self.db.session.query(func.count(model2.rating)).filter_by(
                                                                    cocktail_id=cocktail.cocktail_id).first()
            result.update({cocktail.cocktail_id: {'cocktail_name': cocktail.cocktail_name,
                                                'avg_rating': int(avg_rating[0]),
                                                'ratings_quantity': int(ratings_quantity[0])}})
        return json.dumps(result)

    def add(self, pub_name, model):
        if bool(self.db.session.query(model).filter_by(pub_name=pub_name).scalar()):
            return 'False'
        else:
            data = model(pub_name)
            self.db.session.add(data)
            self.db.session.commit()
            return 'True'

    def delete(self, model, pub_id):
        if not self.db.session.query(model).filter_by(pub_id=pub_id).scalar():
            return 'False'
        else:
            self.db.session.query(model).filter_by(pub_id=pub_id).delete()
            self.db.session.commit()
            return 'True'


class CocktailsManagement:
    def __init__(self, db):
        self.db = db

    def show(self, model, model2, cocktail_name):
        result = {}
        for cocktail in self.db.session.query(model).filter_by(cocktail_name=cocktail_name).all():
            avg_rating = self.db.session.query(func.avg(model2.rating)).filter_by(
                cocktail_id=cocktail.cocktail_id).first()
            ratings_quantity = self.db.session.query(func.count(model2.rating)).filter_by(
                cocktail_id=cocktail.cocktail_id).first()
            result.update({cocktail.cocktail_id: {'cocktail_name': cocktail.cocktail_name,
                                                  'pub_id': cocktail.pub_id,
                                                  'avg_rating': int(avg_rating[0]),
                                                  'ratings_quantity': int(ratings_quantity[0])}})
        return json.dumps(result)

    def add(self, model, cocktail_name, pub_id):
        if bool(self.db.session.query(model).filter_by(cocktail_name=cocktail_name, pub_id=pub_id).scalar()):
            return 'False'
        else:
            data = model(cocktail_name, pub_id)
            self.db.session.add(data)
            self.db.session.commit()
            return 'True'

    def delete(self, model, cocktail_id):
        if not self.db.session.query(model).filter_by(cocktail_id=cocktail_id).first().scalar():
            return False
        else:
            self.db.session.query(model).filter_by(cocktail_id=cocktail_id).delete()
            return True
