#!/usr/bin/python3

""" This module contains functions for reviews """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ Retrieves the list of all reviews """
    reviews = storage.all('Review')
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    rev_list = []
    for pl in place.reviews:
        rev_list.append(pl.to_dict())
    return jsonify(rev_list)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get review(review_id):
    """ Retrieves a review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())
