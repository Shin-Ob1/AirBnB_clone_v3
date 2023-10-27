from api.v1.views import app_views
from flask import Flask, jsonify

@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})
