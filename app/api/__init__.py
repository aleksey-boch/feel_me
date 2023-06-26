from flask import Blueprint
from flask_marshmallow import Marshmallow

api = Blueprint('api', __name__, url_prefix='/api/v1')
ma = Marshmallow()

# This import might seem unconventional, however is required to register your
# routes, which are created under the api folder. As you add more routes,
# you should import them here so the app can pick it up.
from app.api import subscription
from app.api import token
