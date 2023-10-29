#!/usr/bin/python3

""" This module contains functions for cities"""

from flask import jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def state_cities(state_id):
    """ Retrieves the list of cities of a state id  """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    ct_list = []
    for ct in state.cities:
        ct_list.append(ct.to_dict())
    return jsonify(ct_list)
