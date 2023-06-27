import pytest

from app import create_app, db


@pytest.fixture()
def app():
    """Application Initialization Fixture"""

    app = create_app(config_key='testing')

    # other setup can go here
    with app.app_context():
        db.create_all()

    yield app

    # clean up / reset resources here
    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    """Fixture REST API client"""
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
