from app.app import db, ma


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user_email = db.Column(db.String(255))
    duration = db.Column(db.Integer)
    expiration_at = db.Column(db.Integer)


class SubscriptionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Subscription

    user_id = ma.auto_field()
    user_email = ma.auto_field()
    books = ma.auto_field()
