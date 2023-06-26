import pytest

from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.from_object('config.TestingConfig')

    # other setup can go here
    # db.

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
