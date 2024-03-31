#!/usr/bin/python3
"""This is a module that contains views for the Places for this API"""
from flask import jsonify
from flask import request
from flask import abort
from flask import make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_city_places(city_id):
    """This is a function that returns places for a city with a specified city
    id when the /cities/city_id/places route is reached"""
    city = storage.get(City, city_id)
    if city:
        places = []
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)
    abort(404)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_one_place(place_id):
    """This is a function that gets a place with a place id when
    /places/place_id route is reached"""
    result = storage.get(Place, place_id)
    if result:
        return jsonify(result.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_one_place(place_id):
    """this is a function that deletes one Place with the specified
    place id when the /places/place_id route is reached"""
    result = storage.all(Place).values()
    place = list(filter(lambda x: x.id == place_id, result))
    if place:
        storage.delete(place[0])
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """This is a function that creates a new place at the
    /cities/city_id/places route's endpoint"""
    result = storage.get(City, city_id)
    if result:
        if request.get_json():
            if 'user_id' in request.get_json():
                data = request.get_json()
                user = storage.get(User, data['user_id'])
                if user:
                    if 'name' in request.get_json():
                        data['city_id'] = city_id
                        place = Place(**data)
                        place.save()
                        return make_response(jsonify(place.to_dict()), 201)
                    abort(400, description="Missing name")
                abort(404)
            abort(400,  description="Missing user_id")
        abort(404, description="Not a JSON")
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_one_place(place_id):
    """this is a function that updates one place with a specified id
    when the /places/place_id route is reached"""
    result = storage.all(Place).values()
    place = list(filter(lambda x: x.id == place_id, result))
    if place:
        update_request = request.get_json()
        if type(update_request) is dict:
            update = place[0]
            for item, value in update_request.items():
                if item not in ["id", "user_id", "city_id", "created_at",
                                "updated_at"]:
                    setattr(update, item, value)
            update.save()
            return make_response(jsonify(update.to_dict()), 200)
        abort(400, description="Not a JSON")
    abort(404)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """This is a function that retrieves all Place objects depending of the
    JSON in the body of the request"""
    if request.get_json():
        data = request.get_json()

        if data and len(data):
            states = data.get('states', None)
            cities = data.get('cities', None)
            amenities = data.get('amenities', None)

        if not data or not len(data) or (
                not states and
                not cities and
                not amenities):
            places = storage.all(Place).values()
            list_places = []
            for place in places:
                list_places.append(place.to_dict())
            return jsonify(list_places)

        list_places = []
        if states:
            states_obj = [storage.get(State, s_id) for s_id in states]
            for state in states_obj:
                if state:
                    for city in state.cities:
                        if city:
                            for place in city.places:
                                list_places.append(place)

        if cities:
            city_obj = [storage.get(City, c_id) for c_id in cities]
            for city in city_obj:
                if city:
                    for place in city.places:
                        if place not in list_places:
                            list_places.append(place)

        if amenities:
            if not list_places:
                list_places = storage.all(Place).values()
            amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
            list_places = [place for place in list_places
                        if all([am in place.amenities
                                for am in amenities_obj])]

        places = []
        for p in list_places:
            d = p.to_dict()
            d.pop('amenities', None)
            places.append(d)

        return jsonify(places)
    abort(400, description="Not a JSON")
