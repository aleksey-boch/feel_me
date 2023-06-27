from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from app import api
from app.api import ma
from app.models import db
from config import config_dict

# Setup the Flask-JWT-Extended extension
jwt = JWTManager()
# For database migrations
migrate = Migrate()


def create_app(config_key=None):
    app = Flask(__name__, instance_relative_config=True)

    config_class = config_dict[config_key or 'develop']
    app.config.from_object(config_class)
    config_class.init_app(app)

    # Order matters: Initialize SQLAlchemy before Marshmallow
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    # migrate.init_app(app, db)

    app.register_blueprint(api.api)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
