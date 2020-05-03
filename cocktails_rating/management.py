import json


class PubsManagement:
    def show_all(self, db, model):
        result = {}
        for pub in db.session.query(model).all():
            result.update({pub.pub_id: {'pub_name': pub.pub_name}})
        return json.dumps(result)

    def show_by_pubs(self, db, model, pub_id):
        result = {}
        for pub in db.session.query(model).filter_by(pub_id=pub_id).all():
            result.update({pub.pub_id: {'pub_name': pub.pub_name}})
        return json.dumps(result)

    def add(self, db, pub_name, model):
        if bool(db.session.query(model).filter_by(pub_name=pub_name).scalar()):
            return False
        else:
            data = model(pub_name)
            db.session.query.add(data)
            db.session.commit()
            return True

    def delete(self, db, model, pub_id):
        if not db.session.query(model).filter_by(pub_id=pub_id).scalar():
            return False
        else:
            db.session.query(model).filter_by(pub_id=pub_id).delete()
            db.session.commit()
            return True

class CocktailsManagement:
    pass
