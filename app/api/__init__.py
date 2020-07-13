from flask import Blueprint

rating = Blueprint('api', __name__)

from . import views
