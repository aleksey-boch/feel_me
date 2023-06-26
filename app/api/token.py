from datetime import datetime

from flask import request, make_response, abort
from flask_jwt_extended import create_access_token

from app.api import api, ma
from app.models import insert_or_update
from app.models.partner import Partner
from app.models.token import Token


class LoginSchema(ma.SQLAlchemySchema):
    email = ma.String(required=True)
    psw = ma.String(required=True)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.

@api.route("/token", methods=["POST"])
def get_token():
    data = LoginSchema().load(request.json.get("user", None))

    partner = Partner.query.filter_by(email=data['email']).first()
    if not partner:
        return make_response(
            'Could not generate new token',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    old_token = Token.query.filter_by(
        partner_id=partner.id
    ).order_by(Token.created_at.desc()).first()
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

    jwt_token = create_access_token({
        'token_id': token.id,
        'websites_name': partner.websites_name,
    })

    return make_response(jwt_token, 200)
