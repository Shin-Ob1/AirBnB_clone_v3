#!/usr/bin/python3

""" This module contains functions for cities"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def state_cities(state_id):
    """ Retrieves the list of cities of a state id  """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    ct_list = []
    for ct in state.cities:
        ct_list.append(ct.to_dict())
    return jsonify(ct_list)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """ retrieves a city object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a city object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a new city in a state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    body = request.get_json(silent=True)
    if body is None:
        abort(400, description="Not a JSON")
    if 'name' not in body:
        abort(400, description="Missing name")
    body['state_id'] = state_id
    new_city = City(**body)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """ Updates values of an existing city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    body = request.get_json(silent=True)
    if body is None:
        abort(400, description="Not a JSON")
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
