#!/usr/bin/python3

"""This module contains the route for our api
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', methods=['GET'])
def status():
    """ returns status in json """
    return jsonify({"status": "OK"})


@app_views.route('stats', methods=['GET'])
def stats():
    """Return the stats in dict format"""
    new_dict = {}
    for key, value in classes.items():
        count = storage.count(value)
        new_dict[key] = count
    return jsonify(new_dict)
