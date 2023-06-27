def test_register(client, app):
    email = '2@2.com'
    psw = 'vasyaPupkin123'

    response = client.post(
        "/register",
        data={
            'login': email,
            'password': psw,
            'websites_name': email,
            'email': email,
            'psw': psw,

        },
        headers={'Content-Type': 'multipart/form-data'}
    )

    assert response.status_code == 200
    assert b'<!DOCTYPE html>\n<html lang="en">' in response.data
