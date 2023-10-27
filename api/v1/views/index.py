from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """ returns status in json """
    return jsonify({"status": "OK"})
