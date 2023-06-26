from flask import request, make_response
from flask_jwt_extended import create_access_token

from app.api import api, ma
from app.models.partner import Partner


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

    token = create_access_token(
        identity={
            'websites_name': partner.websites_name,
        }
    )

    return make_response(token, 200)
