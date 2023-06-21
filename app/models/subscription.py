from app.models import db


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user_email = db.Column(db.String(255))
    duration = db.Column(db.Integer)
    expiration_at = db.Column(db.DateTime)


