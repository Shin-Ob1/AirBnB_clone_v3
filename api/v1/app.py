#!/usr/bin/python3
""" This module covers all the functionalities of out app
"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def app_teardown(self):
    """ method to close storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ returns 404 error in json """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    app.run(host=os.getenv('HBNB_API_HOST') or '0.0.0.0',
            port=os.getenv('HBNB_API_PORT') or 5000,
            threaded=True)
