from datetime import datetime

from app.models import db


class Subscription(db.Model):
    """Model for describing a subscription"""
    id = db.Column(db.Integer, primary_key=True)
    # ID of the partner from which this subscription came
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
    # User external ID: To identify the user on the partner website.
    user_id = db.Column(db.Integer, unique=True)
    # User email: This will be used to create an account on portal.feelme.com
    user_email = db.Column(db.String(255))
    # Subscription information: Duration (1 month, 3 months, etc)
    duration = db.Column(db.Integer)
    # subscription expiration date
    expiration_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Subscription {self.id}>"
