from datetime import datetime

from app.models import db


class Token(db.Model):
    """Model for a token"""
    id = db.Column(db.Integer, primary_key=True)
    # ID of the partner to which this token was issued
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
    # token expiration date
    expired_at = db.Column(db.DateTime)
    # id of the user who revokes this token
    revoked = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Token {self.id}>"
