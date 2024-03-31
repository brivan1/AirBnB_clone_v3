#!/usr/bin/python3
"""This is a module that contains views for the Places Reviews for this API"""
from flask import abort
from flask import jsonify
from flask import make_response
from flask import request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """This is a function that retrieves all reviews for a place when the
    /places/places_id/reviews route is reached"""
    places = storage.get(Place, place_id)
    if places:
        reviews = []
        for review in places.reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews)
    abort(404)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_one_review(review_id):
    """this is a function that retrieves one review with the specified
    review id when the /reviews/review_id route is reached"""
    reviews = storage.all(Review).values()
    if review_id:
        one_review = list(filter(lambda x: x.id == review_id, reviews))
        if one_review:
            return jsonify(one_review[0].to_dict())
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_one_review(review_id):
    """this is a function that deletes one Review with the specified
    review id when the /reviews/review_id route is reached"""
    result = storage.all(Review).values()
    review = list(filter(lambda x: x.id == review_id, result))
    if review:
        storage.delete(review[0])
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """this is a function that creates one review when the
    /places/<place_id>/reviews route is reached"""
    result = storage.get(Place, place_id)
    if result:
        if request.get_json():
            if 'user_id' in request.get_json():
                data = request.get_json()
                user = storage.get(User, data['user_id'])
                if user:
                    if 'text' in request.get_json():
                        data['place_id'] = place_id
                        review = Review(**data)
                        review.save()
                        return make_response(jsonify(review.to_dict()), 201)
                    abort(400, description="Missing text")
                abort(404)
            abort(400,  description="Missing user_id")
        abort(404, description="Not a JSON")
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_one_review(review_id):
    """this is a function that updates one review with a specified id
    when the /reviews/<review_id> route is reached"""
    result = storage.all(Review).values()
    review = list(filter(lambda x: x.id == review_id, result))
    if review:
        update_request = request.get_json()
        if type(update_request) is dict:
            update = review[0]
            for item, value in update_request.items():
                if item not in ["id", "user_id", "place_id", "created_at",
                                "updated_at"]:
                    setattr(update, item, value)
            update.save()
            return make_response(jsonify(update.to_dict()), 200)
        abort(400, description="Not a JSON")
    abort(404)
