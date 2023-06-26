import datetime

from flask_jwt_extended import create_access_token

from app.models import insert_or_update
from app.models.partner import Partner
from app.models.token import Token


def test_index(client):
    response = client.get("/")
    assert b'<h1>Testing the Flask Application Factory Pattern</h1>' in response.data


def test_add_subscription(client, app):
    user_id = 69

    with app.app_context():
        partner = Partner(
            email='2@2.com',
            psw='vasyaPupkin123',
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
            }
        )

    response = client.post(
        "/api/v1/subscription",
        headers={'Authorization': f'Bearer {jwt_token}'},
        json={
            'subscription': {
                'user_id': user_id,
                'user_email': '2@2.com',
                'duration': 111,
                'expiration_at': datetime.datetime.now().isoformat(),
            }
        },
    )

    assert response.data == b'<Subscription 1>'
    assert response.status_code == 200


def test_update_subscription(client, app):
    user_id = 69

    with app.app_context():
        partner = Partner(
            email='2@2.com',
            psw='vasyaPupkin123',
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
            }
        )

    response = client.post(
        "/api/v1/subscription",
        headers={'Authorization': f'Bearer {jwt_token}'},
        json={
            'subscription': {
                'user_id': user_id,
                'user_email': '2@2.com',
                'duration': 111,
                'expiration_at': datetime.datetime.now().isoformat(),
            }
        },
    )
    assert response.status_code == 200

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
