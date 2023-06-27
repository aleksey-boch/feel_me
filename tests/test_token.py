from werkzeug.security import generate_password_hash

from app.models import insert_or_update
from app.models.partner import Partner


def test_get_token(client, app):
    email = '2@2.com'
    psw = 'vasyaPupkin123'

    partner = Partner(
        email=email,
        psw=generate_password_hash(psw),
        websites_name='One_site',
    )
    with app.app_context():
        insert_or_update(partner)

    response = client.post(
        "/api/v1/token",
        json={
            'user': {
                'email': email,
                'psw': psw,
            }
        },
    )

    assert response.status_code == 200
    assert response.data is not None
