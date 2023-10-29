#!/usr/bin/python3

"""This module contains the route for our api
"""

from api.v1.views import app_views
from flask import request, abort, jsonify, make_response
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/states/', methods=['GET', 'POST'])
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def get_all_state(state_id=None):
    """Get a list of state dictionary """
    new_dict = []
    if request.method == 'GET':
        if state_id is None:
            data = storage.all(State)
            for obj in data.values():
                new_dict.append(obj.to_dict())
        else:
            data = storage.get(State, state_id)
            if data is None:
                abort(404)
            new_dict = data.to_dict()
        return jsonify(new_dict)
    elif request.method == 'DELETE' and state_id is not None:
        data = storage.get(State, state_id)
        if data is None:
            abort(404)
        else:
            storage.delete(data)
            return jsonify({}), 200
    elif request.method == 'POST' and state_id is None:
        data = request.get_json()
        if data is None:
            return 'Not a JSON', 400
        elif data.get('name') is None:
            return 'Missing name', 400
        obj = State(**data)
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201
    elif request.method == 'PUT' and state_id is not None:
        data = storage.get(State, state_id)
        if data is None:
            abort(404)
        else:
            js = request.get_json()
            if js is None:
                return 'Not a JSON', 400
            for key, value in js.items():
                if key != "id" and key != 'created_at' and key != 'updated_at':
                    if hasattr(data, key):
                        setattr(data, key, value)
            storage.save()
            return jsonify(data.to_dict()), 200
