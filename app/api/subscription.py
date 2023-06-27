from flask import request, current_app, abort, make_response
from flask_jwt_extended import get_jwt
from marshmallow import ValidationError

from app.api import api, ma, token_required
from app.models import insert_or_update
from app.models.subscription import Subscription


class UpdateSubscriptionSchema(ma.SQLAlchemySchema):
    user_id = ma.Integer(required=True)
    duration = ma.Integer(required=True)
    expiration_at = ma.DateTime(required=True)


class AddSubscriptionSchema(UpdateSubscriptionSchema):
    user_email = ma.String(required=True)


@api.route("/subscription", methods=["POST"])
@token_required()
def add_subscription():
    jwt_token_data = get_jwt()

    try:
        new_subscription = AddSubscriptionSchema().load(request.json.get("subscription", None))
    except ValidationError as ex:
        current_app.logger.exception(ex)
        abort(400, ex.messages)

    subscription = Subscription(
        partner_id=jwt_token_data['websites_name'],
        user_id=new_subscription['user_id'],
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
@token_required()
def update_subscription():
    try:
        new_subscription = UpdateSubscriptionSchema().load(request.json.get("subscription", None))
    except ValidationError as ex:
        current_app.logger.exception(ex)
        abort(400, ex.messages)

    subscription = Subscription.query.filter_by(user_id=new_subscription['user_id']).first()
    if not subscription:
        current_app.logger.warning('Subscription for user not found. For user: %s', new_subscription['email'])
        abort(404, 'Subscription for user not found')

    subscription.duration = new_subscription['duration']
    subscription.expiration_at = new_subscription['expiration_at']

    result, response = insert_or_update(subscription)
    if not result:
        abort(500, 'Something went wrong. Our programmers have been notified.')

    subscription = response
    return make_response(str(subscription), 200)
