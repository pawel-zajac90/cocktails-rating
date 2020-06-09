from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class NewPubForm(FlaskForm):
    name = StringField()


class NewCocktailForm(FlaskForm):
    name = StringField()
    pub_id = IntegerField()
    description = StringField()
