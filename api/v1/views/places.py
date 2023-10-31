#!/usr/bin/python3

"""This module contains the route for our api
"""

from api.v1.views import app_views
from flask import request, abort, jsonify, Flask
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_city_place(city_id):
    """Retrieve place data of a city"""
    new_dict = []

    if request.method == 'GET':
        data = storage.get(City, city_id)
        if data is None:
            abort(404)
        for obj in data.places:
            new_dict.append(obj.to_dict())
        return jsonify(new_dict)

    elif request.method == 'POST':
        data = storage.get(City, city_id)
        if data is None:
            abort(404)
        request_data = request.get_json(silent=True)
        if request_data is None:
            return 'Not a JSON', 400
        if 'user_id' not in request_data:
            return 'Missing user_id', 400
        if 'name' not in request_data:
            return 'Missing name', 400
        get_user = storage.get(User, request_data['user_id'])
        if get_user is None:
            abort(404)
        request_data['city_id'] = city_id
        d_place = Place(**request_data)
        new_dict = d_place.to_dict()
        storage.new(d_place)
        storage.save()
        return jsonify(new_dict), 201


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_places(place_id):
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

        storage.delete(data)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT' and place_id is not None:
        data = storage.get(Place, place_id)
        if data is None:
            abort(404)

        js = request.get_json(silent=True)
        if js is None:
            return 'Not a JSON', 400
        for key, value in js.items():
            if key not in ['id', 'created_at',
                           'updated_at', 'user_id', 'city_id']:
                setattr(data, key, value)
        storage.save()
        return jsonify(data.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """search places more effectively"""
    new_dict = []
    data = request.get_json(silent=True)
    if data is None:
        return 'Not a JSON', 400

    state = data.get('states', [])
    city = data.get('cities', [])
    amenity = data.get('amenities', [])

    if not any([state, city, amenity]):
        obj = storage.all(Place).values()
        for e_obj in obj:
            new_dict.append(e_obj.to_dict())
        return jsonify(new_dict)

    if state:
        for id_s in state:
            a_state = storage.get(State, id_s)
            if a_state:
                for each_city in a_state.cities:
                    for each_place in each_city.places:
                        if each_place not in new_dict:
                            new_dict.append(each_place.to_dict())
    if city:
        for id_c in city:
            a_city = storage.get(City, id_c)
            if a_city and a_city not in new_dict:
                for each_place in a_city.places:
                    if each_place not in new_dict:
                        new_dict.append(each_place.to_dict())

    if amenity:
        filtered_place = []
        for place in new_dict:
            if all(s_amenity in Place(**place).amenities
                   for s_amenity in amenity):
                filtered_place.append(place)
        new_dict = filtered_place
    return jsonify(new_dict)
