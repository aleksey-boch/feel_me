"""This file is the main module which contains the app, where all the good
stuff happens. You will always want to point your applications like Gunicorn
to this file, which will pick up the app to run their servers.
"""
from flask_migrate import Migrate, upgrade

from app import create_app, db

app = create_app()
migrate = Migrate(app, db)


# More custom commands can be added to flasks CLI here(for running tests and
# other stuff)


@app.cli.command()
def deploy():
    """Run deployment tasks"""
    # Migrate database to latest revision
    upgrade()
