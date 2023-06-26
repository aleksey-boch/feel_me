import datetime

from flask_jwt_extended import create_access_token


def test_index(client):
    response = client.get("/")
    assert b'<h1>Testing the Flask Application Factory Pattern</h1>' in response.data


def test_login(client):
    response = client.get("/login")
    assert b'<h1>Testing the Flask Application Factory Pattern</h1>' in response.data


def test_add_subscription(client, app):
    with app.app_context():
        token = create_access_token({'websites_name': '2@2.com'})

    response = client.post(
        "/api/v1/subscription",
        headers={'Authorization': f'Bearer {token}'},
        json={
            'subscription': {
                'user_id': 69,
                'user_email': '2@2.com',
                'duration': 111,
                'expiration_at': datetime.datetime.now().isoformat(),
            }
        },
    )

    assert response.data is not None
    assert response.status_code == 200


def test_update_subscription(client):
    response = client.put("/api/v1/subscription")
    assert b'<h1>Testing the Flask Application Factory Pattern</h1>' in response.data
