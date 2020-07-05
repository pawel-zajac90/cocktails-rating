from flask import make_response
from flask import jsonify


def does_not_exist():
    return make_response(jsonify(status='No content to display, probably record does not exist.'), 204)


def does_exist():
    response = make_response(jsonify(status='Cannot add this record, probably record already exist.'), 210)
    return response
