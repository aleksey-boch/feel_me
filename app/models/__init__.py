from flask import current_app

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()


def db_persist(func):
    """Decorator for database operations."""
    def persist(*args, **kwargs):
        response = func(*args, **kwargs)
        try:
            db.session.commit()
            current_app.logger.debug("success calling db func: " + func.__name__)
            return True, response

        except SQLAlchemyError as e:
            current_app.logger.error(e.args)
            db.session.rollback()
            return False, response

    return persist


@db_persist
def insert_or_update(table_object):
    """The operation of inserting/updating a record in a table."""
    return db.session.merge(table_object)
