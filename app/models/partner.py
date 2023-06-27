from datetime import datetime

from app.models import db


class Partner(db.Model):
    """Model for partner websites."""
    id = db.Column(db.Integer, primary_key=True)
    # Email as login
    email = db.Column(db.String(50), unique=True)
    # password to get the token
    psw = db.Column(db.String(500), nullable=False)
    # partner website address
    websites_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Partner {self.id}>"
