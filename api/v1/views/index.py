#!/usr/bin/python3
"""
Module that contains the index view for the API
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status_getter():
    """route /api/status gets the status of the API"""
    return jsonify(status='OK')


@app_views.route('/stats')
def statistics():
    """This is a route /api/stats that displays the statistical count for each
    object"""
    all_models = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    for item, val in all_models.items():
        all_models[item] = storage.count(val)
    return jsonify(all_models)
