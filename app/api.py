from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError

import app
from app.models import SubscriptionSchema


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/api/v1/subscription", methods=["POST"])
@jwt_required()
def add_subscription():
    # Access the identity of the current user with get_jwt_identity
    partner_websites_name = get_jwt_identity()
    try:
        subscription = SubscriptionSchema().load(request.json.get("subscription", None))
    except ValidationError as ex:
        app.logger.exception(ex)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'
