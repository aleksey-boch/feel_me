from functools import wraps

from flask import Blueprint
from flask import make_response
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request
from flask_marshmallow import Marshmallow

from app.models.partner import Partner
from app.models.token import Token

api = Blueprint('api', __name__, url_prefix='/api/v1')
ma = Marshmallow()


# Here is a custom decorator that verifies the JWT is present in the request,
# as well as insuring that the JWT has a claim indicating that this user is
# an administrator
def token_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            if not all((claims.get('token_id'), claims.get('websites_name'))):
                return make_response('Token not valid', 403)

            token = Token.query.filter_by(id=claims['token_id']).first()
            partner = Partner.query.filter_by(websites_name=claims['websites_name']).first()

            if all((token, partner)) and token.partner_id == partner.id:
                return fn(*args, **kwargs)
            else:
                return make_response('Token not valid', 403)

        return decorator

    return wrapper


# This import might seem unconventional, however is required to register
# routes, which are created under the api folder. As you add more routes,
# you should import them here so the app can pick it up.
from app.api import subscription
from app.api import token
