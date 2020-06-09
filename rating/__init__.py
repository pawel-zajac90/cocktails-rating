from flask import Blueprint

rating = Blueprint('rating', __name__)

from . import views
