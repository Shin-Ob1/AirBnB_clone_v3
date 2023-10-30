#!/usr/bin/python3
""" This is the initializing module
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
# Import state views here
from api.v1.views.states import *
# Import user views here
from api.v1.views.users import *
# Import amenity views here
from api.v1.views.amenities import *
# Import city views here
from api.v1.views.cities import *
# Import place views here
from api.v1.views.places import *
# Import review views here
from api.v1.views.places_reviews import *
