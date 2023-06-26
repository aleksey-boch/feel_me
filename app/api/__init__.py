from functools import wraps

from flask import Blueprint
from flask import make_response
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request
from flask_marshmallow import Marshmallow

api = Blueprint('api', __name__, url_prefix='/api/v1')
ma = Marshmallow()

# This import might seem unconventional, however is required to register your
# routes, which are created under the api folder. As you add more routes,
# you should import them here so the app can pick it up.
from app.api import subscription
from app.api import token


# Here is a custom decorator that verifies the JWT is present in the request,
# as well as insuring that the JWT has a claim indicating that this user is
# an administrator
def token_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return make_response(jwt_token, 403)

        return decorator

    return wrapper
