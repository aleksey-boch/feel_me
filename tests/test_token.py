from flask_jwt_extended import create_access_token


def test_get_token(client, app):
    # with app.app_context():
    #     token = create_access_token('2@2.com')
    response = client.post(
        "/api/v1/token",
        json={
            'user': {
                'email': '2@2.com',
                'psw': 'vasyaPupkin123',
            }
        }
    )
    assert b'<h1>Testing the Flask Application Factory Pattern</h1>' in response.data

