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
def get_review(review_id):
    """ Retrieves a review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a new review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    body = request.get_json(silent=True)
    if body is None:
        abort(404, description="Not a JSON")
    if user_id not in body:
        abort(404, description="Missing user_id")
    text = body.get('text')
    if text is None:
        abort(404, "Missing text")
    user = storage.get(User, body['user_id'])
    if user is None:
        abort(404)
    body['place_id'] = place_id
    rev = Review(**body)
    rev.save()
    return jsonify(rev.to_dict()), 201
