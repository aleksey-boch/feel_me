from flask import request, current_app, abort, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.api import api, ma
from app.models import insert_or_update
from app.models.subscription import Subscription


class UpdateSubscriptionSchema(ma.SQLAlchemySchema):
    user_id = ma.Integer(required=True)
    duration = ma.Integer(required=True)
    expiration_at = ma.DateTime(required=True)


class AddSubscriptionSchema(UpdateSubscriptionSchema):
    user_email = ma.String(required=True)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.

@api.route("/subscription", methods=["POST"])
@jwt_required()
def add_subscription():
    # Access the identity of the current user with get_jwt_identity
    jwt_token_data = get_jwt_identity()

    try:
        new_subscription = AddSubscriptionSchema().load(request.json.get("subscription", None))
    except ValidationError as ex:
        current_app.logger.exception(ex)
        abort(400, ex.messages)

    subscription = Subscription(
        partner_id=jwt_token_data['websites_name'],
        user_email=new_subscription['user_email'],
        duration=new_subscription['duration'],
        expiration_at=new_subscription['expiration_at'],
    )
    result, response = insert_or_update(subscription)
    if not result:
        abort(500, 'Something went wrong. Our programmers have been notified.')

    subscription = response
    return make_response(str(subscription), 200)


@api.route("/subscription", methods=["PUT"])
@jwt_required()
def update_subscription():
    # Access the identity of the current user with get_jwt_identity
    partner_websites_name = get_jwt_identity()
    try:
        subscription = AddSubscriptionSchema().load(request.json.get("subscription", None))
    except ValidationError as ex:
        current_app.logger.exception(ex)
