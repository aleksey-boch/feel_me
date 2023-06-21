from flask import request, current_app, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.api import api, ma
from app.models.subscription import Subscription


class SubscriptionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Subscription

    user_id = ma.auto_field()
    user_email = ma.auto_field()
    duration = ma.auto_field()
    expiration_at = ma.auto_field()


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.

@api.route("/subscription", methods=["POST"])
@jwt_required()
def add_subscription():
    # Access the identity of the current user with get_jwt_identity
    partner_websites_name = get_jwt_identity()
    try:
        subscription = SubscriptionSchema().load(request.json.get("subscription", None))
    except ValidationError as ex:
        current_app.logger.exception(ex)
        abort(400, ex.messages)

    return '204'


@api.route("/subscription", methods=["PUT"])
@jwt_required()
def update_subscription():
    # Access the identity of the current user with get_jwt_identity
    partner_websites_name = get_jwt_identity()
    try:
        subscription = SubscriptionSchema().load(request.json.get("subscription", None))
    except ValidationError as ex:
        current_app.logger.exception(ex)
