from datetime import datetime

from app.models import db


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expired_at = db.Column(db.DateTime, default=datetime.utcnow)
    revoked = db.Column(db.Integer)  # id of the user who revokes this token

    def __repr__(self):
        return f"<partners {self.id}>"
