from flask import Flask
from flask_jwt_extended import JWTManager

from app import api
from app.api import ma
from app.models import db

# Setup the Flask-JWT-Extended extension
jwt = JWTManager()


def create_app(config_class=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class or 'config.DevelopmentConfig')

    # Order matters: Initialize SQLAlchemy before Marshmallow
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(api.api)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
