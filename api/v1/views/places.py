#!/usr/bin/python3

"""This module contains the route for our api
"""

from api.v1.views import app_views
from flask import request, abort, jsonify, Flask
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_city_place(city_id=None):
    """Retrieve place data of a city"""
    new_dict = []

    if request.method == 'GET':
        if city_id is not None:
            data = storage.get(City, city_id)
            if data is None:
                abort(404)
            for obj in data.places:
                new_dict.append(obj.to_dict())
            return jsonify(new_dict)

    elif request.method == 'POST':
        if city_id is not None:
            data = storage.get(City, city_id)
            if data is None:
                abort(404)
            request_data = request.get_json()
            if request_data is None:
                return 'Not a JSON', 400
            if 'user_id' not in request_data:
                return 'Missing user_id', 400
            get_user = storage.get(User, request_data['user_id'])
            if get_user is None:
                abort(404)
            if 'name' not in request_data:
                return 'Missing name', 400
            request_data['city_id'] = city_id
            d_place = Place(**request_data)
            new_dict = d_place.to_dict()
            storage.new(d_place)
            storage.save()
            return jsonify(new_dict), 201


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_places(place_id=None):
    """Get a list of place dictionary """
    new_dict = []
    if request.method == 'GET':
        if place_id is not None:
            data = storage.get(Place, place_id)
            if data is None:
                abort(404)
            new_dict = data.to_dict()
        return jsonify(new_dict)

    elif request.method == 'DELETE' and place_id is not None:
        data = storage.get(Place, place_id)
        if data is None:
            abort(404)
        else:
            storage.delete(data)
            storage.save()
            return jsonify({}), 200

    elif request.method == 'PUT' and place_id is not None:
        data = storage.get(Place, place_id)
        if data is None:
            abort(404)
        else:
            js = request.get_json()
            if js is None:
                return 'Not a JSON', 400
            for key, value in js.items():
                if key not in ['id', 'created_at',
                               'updated_at', 'user_id', 'city_id']:
                    setattr(data, key, value)
            storage.save()
            return jsonify(data.to_dict()), 200
