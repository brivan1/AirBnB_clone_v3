#!/usr/bin/python3
"""This is a module that contains views for the Users for this API"""
from flask import jsonify
from flask import request
from flask import abort
from flask import make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """This is a function that retrieves all users when the /users
    route is reached"""
    users = storage.all(User).values()
    all_users = list(map(lambda x: x.to_dict(), users))
    return jsonify(all_users)


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def get_one_user(user_id):
    """this is a function that retrieves one user with the specified
    user id when the /users/user_id route is reached"""
    users = storage.all(User).values()
    if user_id:
        one_user = list(filter(lambda x: x.id == user_id, users))
        if one_user:
            return jsonify(one_user[0].to_dict())
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_one_user(user_id):
    """this is a function that deletes one User with the specified
    user id when the /users/user_id route is reached"""
    result = storage.all(User).values()
    user = list(filter(lambda x: x.id == user_id, result))
    if user:
        storage.delete(user[0])
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """this is a function that creates one user when the
    /users route is reached"""
    user_request = request.get_json()
    if type(user_request) is dict:
        if 'email' not in user_request:
            abort(400, description="Missing email")
        if 'password' not in user_request:
            abort(400, description="Missing password")
        user = User(**user_request)
        user.save()
        return make_response(jsonify(user.to_dict()), 201)
    else:
        abort(400, description="Not a JSON")


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_one_user(user_id):
    """this is a function that updates one user with a specified id
    when the /users/user_id route is reached"""
    result = storage.all(User).values()
    user = list(filter(lambda x: x.id == user_id, result))
    if user:
        update_request = request.get_json()
        if type(update_request) is dict:
            update = user[0]
            for item, value in update_request.items():
                if item not in ["id", "email", "created_at", "updated_at"]:
                    setattr(update, item, value)
            update.save()
            return make_response(jsonify(update.to_dict()), 200)
        else:
            abort(400, description="Not a JSON")
    else:
        abort(404)
