from datetime import datetime

from app.models import db


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
    expired_at = db.Column(db.DateTime)
    revoked = db.Column(db.Integer)  # id of the user who revokes this token
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Token {self.id}>"
