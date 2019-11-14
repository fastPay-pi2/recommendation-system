from flask import jsonify, Blueprint, request
from flask_cors import CORS

recommendation_blueprint = Blueprint('cart_blueprint',
                                     __name__)
CORS(recommendation_blueprint)

@recommendation_blueprint.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({
        "message": "success"
    }), 200

