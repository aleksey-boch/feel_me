import datetime

from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

from app.models import insert_or_update
from app.models.partner import Partner
from app.models.subscription import Subscription
from app.models.token import Token


def test_index(client):
    """Application Minimum Health Test"""
    response = client.get("/")
    assert b'<!DOCTYPE html>\n<html lang="en"' in response.data


def test_add_subscription(client, app):
    """Test for adding a new subscription"""
    user_id = 69
    user_email = '2@2.com'
    user_psw = generate_password_hash('vasyaPupkin123')

    with app.app_context():
        partner = Partner(
            email=user_email,
            psw=user_psw,
            websites_name='One_site',
        )
        _, partner = insert_or_update(partner)

        token = Token(partner_id=partner.id)
        _, token = insert_or_update(token)

        jwt_token = create_access_token(
            partner.id,
            additional_claims={
                'token_id': token.id,
                'websites_name': partner.websites_name,
            },
        )

    response = client.post(
        "/api/v1/subscription",
        headers={'Authorization': f'Bearer {jwt_token}'},
        json={
            'subscription': {
                'user_id': user_id,
                'user_email': user_email,
                'duration': 111,
                'expiration_at': datetime.datetime.now().isoformat(),
            }
        },
    )

    assert response.data == b'<Subscription 1>'
    assert response.status_code == 200


def test_update_subscription(client, app):
    """Subscription renewal test"""
    user_id = 69
    user_email = '2@2.com'
    user_psw = generate_password_hash('vasyaPupkin123')
    websites_name = 'One_site'

    with app.app_context():
        partner = Partner(
            email=user_email,
            psw=user_psw,
            websites_name=websites_name,
        )
        _, partner = insert_or_update(partner)

        token = Token(partner_id=partner.id)
        _, token = insert_or_update(token)

        jwt_token = create_access_token(
            partner.id,
            additional_claims={
                'token_id': token.id,
                'websites_name': websites_name,
            },
        )

        subscription = Subscription(
            partner_id=partner.id,
            user_id=user_id,
            user_email=user_email,
            duration=111,
            expiration_at=datetime.datetime.now(),
        )
        _, subscription = insert_or_update(subscription)

    response = client.put(
        "/api/v1/subscription",
        headers={'Authorization': f'Bearer {jwt_token}'},
        json={
            'subscription': {
                'user_id': user_id,
                'duration': 112,
                'expiration_at': datetime.datetime.now().isoformat(),
            }
        },
    )

    assert response.data == b'<Subscription 1>'
    assert response.status_code == 200
