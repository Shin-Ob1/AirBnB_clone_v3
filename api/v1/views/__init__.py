#!/usr/bin/python3
""" This is the initializing module
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
# Import state views here
from api.v1.views.states import *
# Import user views here

# Import amenity views here

# Import city views here

# Import place views here

# Import review views here
