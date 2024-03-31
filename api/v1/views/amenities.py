#!/usr/bin/python3
"""This is a module that contains views for the Cities for this API"""
from flask import jsonify
from flask import request
from flask import abort
from flask import make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """This is a function that retrieves all amenities when the /amenities
    route is reached"""
    amenities = storage.all(Amenity).values()
    al_amenities = list(map(lambda x: x.to_dict(), amenities))
    return jsonify(al_amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_one_amenity(amenity_id):
    """this is a function that retrieves one amenity with the specified
    amenity id when the /amenities/amenity_id route is reached"""
    amenities = storage.all(Amenity).values()
    if amenity_id:
        one_amenity = list(filter(lambda x: x.id == amenity_id, amenities))
        if one_amenity:
            return jsonify(one_amenity[0].to_dict())
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_one_amenity(amenity_id):
    """this is a function that deletes one amenity with the specified
    amenity id when the /amenities/amenity_id route is reached"""
    result = storage.all(Amenity).values()
    amenity = list(filter(lambda x: x.id == amenity_id, result))
    if amenity:
        storage.delete(amenity[0])
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """this is a function that creates one amenity when the
    /amenities route is reached"""
    user_request = request.get_json()
    if type(user_request) is dict:
        if 'name' in user_request:
            amenity = Amenity(**user_request)
            amenity.save()
            return make_response(jsonify(amenity.to_dict()), 201)
        else:
            abort(400, description="Missing name")
    else:
        abort(400, description="Not a JSON")


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_one_amenity(amenity_id):
    """this is a function that updates one amenity with a specified id
    when the /amenities/amenity_id route is reached"""
    result = storage.all(Amenity).values()
    amenity = list(filter(lambda x: x.id == amenity_id, result))
    if amenity:
        update_request = request.get_json()
        if type(update_request) is dict:
            update = amenity[0]
            for item, value in update_request.items():
                if item not in ["id", "created_at", "updated_at"]:
                    setattr(update, item, value)
            update.save()
            return make_response(jsonify(update.to_dict()), 200)
        else:
            abort(400, description="Not a JSON")
    else:
        abort(404)
