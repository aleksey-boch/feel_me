from functools import wraps

from flask import Blueprint
from flask import abort, current_app
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request
from flask_marshmallow import Marshmallow

from app.models.partner import Partner
from app.models.token import Token

api = Blueprint('api', __name__, url_prefix='/api/v1')
ma = Marshmallow()


# Here is a custom decorator that verifies the JWT is present in the request,
# as well as insuring that the JWT has a claim indicating that this token is valid
def token_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            if not all((claims.get('token_id'), claims.get('websites_name'))):
                current_app.logger.error('Token not valid: %s', str(claims))
                return abort(403, 'The token is wrong')

            token = Token.query.filter_by(id=claims['token_id']).first()
            partner = Partner.query.filter_by(websites_name=claims['websites_name']).first()

            if all((token, partner)) and token.partner_id == partner.id:
                return fn(*args, **kwargs)
            else:
                current_app.logger.error('Token not valid: %s', str(claims))
                return abort(403, 'Token not valid')

        return decorator

    return wrapper


# This import might seem unconventional, however is required to register
# routes, which are created under the api folder. As you add more routes,
# you should import them here so the app can pick it up.
from app.api import subscription
from app.api import token
