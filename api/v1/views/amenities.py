#!/usr/bin/python3

"""This module contains the route for our api
"""

from api.v1.views import app_views
from flask import request, abort, jsonify, make_response
from models.amenity import Amenity
from models import storage

classes = {"amenities": Amenity}


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """Get a list of amenity dictionary """
    new_dict = []
    if request.method == 'GET':
        if amenity_id is None:
            data = storage.all(Amenity)
            for obj in data.values():
                new_dict.append(obj.to_dict())
        else:
            data = storage.get(Amenity, amenity_id)
            if data is None:
                abort(404)
            new_dict = data.to_dict()
        return jsonify(new_dict)
    elif request.method == 'DELETE' and amenity_id is not None:
        data = storage.get(Amenity, amenity_id)
        if data is None:
            abort(404)
        else:
            storage.delete(data)
            storage.save()
            return jsonify({}), 200
    elif request.method == 'POST' and amenity_id is None:
        data = request.get_json()

        if data is None:
            return 'Not a JSON', 400
        elif 'name' not in data:
            return 'Missing name', 400

        obj = Amenity(**data)
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201
    elif request.method == 'PUT' and amenity_id is not None:
        data = storage.get(Amenity, amenity_id)
        if data is None:
            abort(404)
        else:
            js = request.get_json()
            if js is None:
                return 'Not a JSON', 400
            for key, value in js.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(data, key, value)
            storage.save()
            return jsonify(data.to_dict()), 200
