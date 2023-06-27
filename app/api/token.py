from datetime import datetime

from flask import request, make_response, abort, current_app
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from app.api import api, ma
from app.models import insert_or_update
from app.models.partner import Partner
from app.models.token import Token


class LoginSchema(ma.SQLAlchemySchema):
    email = ma.String(required=True)
    psw = ma.String(required=True)


@api.route("/token", methods=["POST"])
def get_token():
    """Handler for generating a token for a partner site."""
    data = LoginSchema().load(request.json.get("user", None))

    partner = Partner.query.filter_by(email=data['email']).first()
    if not partner or not check_password_hash(partner.psw, data['psw']):
        current_app.logger.warning('Could not generate new token. For user: %s', data['email'])
        abort(401, 'Could not generate new token: user does not exist or wrong password.')

    # revoke the old one - when issuing a new token.
    old_token = Token.query.filter_by(partner_id=partner.id).order_by(Token.created_at.desc()).first()
    if old_token:
        old_token.revoked = partner.id
        old_token.expired_at = datetime.utcnow
        result, response = insert_or_update(old_token)
        if not result:
            abort(500, 'Something went wrong. Our programmers have been notified.')

    token = Token(partner_id=partner.id)
    result, response = insert_or_update(token)
    if not result:
        abort(500, 'Something went wrong. Our programmers have been notified.')

    jwt_token = create_access_token(
        partner.id,
        additional_claims={
            'token_id': token.id,
            'websites_name': partner.websites_name,
        },
    )

    return make_response(jwt_token, 200)
