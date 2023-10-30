#!/usr/bin/python3

""" This module contains functions for users"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrives the list of all users """
    users = storage.all(User).values()
    user_list = []
    for us in users:
        user_list.append(us.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ Retrieves a user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a new user """
    body = request.get_json(silent=True)
    if body is None:
        abort(400, description="Not a JSON")
    if 'email' not in body:
        abort(400, description="Missing email")
    if 'password' not in body:
        abort(400, description="Missing password")
    new_user = User(**body)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Updates a User info """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    body = request.get_json(silent=True)
    if body is None:
        abort(400, description="Not a JSON")
    ignore = ['id', 'email', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
