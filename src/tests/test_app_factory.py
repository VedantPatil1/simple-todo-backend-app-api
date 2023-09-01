import os


def test_secret_key_set(app):
    with app.app_context():
        assert 'SECRET_KEY' in app.config
        assert app.config['SECRET_KEY'] is not None


def test_client_get_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_client_post_index(client):
    response = client.post('/')
    assert response.status_code == 405  # Method Not Allowed


def test_404_not_found(client):
    response = client.get('/nonexistent-route')
    assert response.status_code == 404


def test_app_creation(app):
    assert app.config['TESTING'] is True


def test_app_client_in_context(client):
    assert client.application.config['TESTING'] is True


def test_dev_app_config(dev_app):
    assert dev_app.config['MONGODB_SETTINGS'] is not None
    assert dev_app.config['MONGODB_SETTINGS'] == {
        'db': os.environ.get("MONGODB_DATABASE"),
        'username': os.environ.get("MONGODB_USERNAME"),
        'password': os.environ.get("MONGODB_PASSWORD"),
        'host': os.environ.get("MONGODB_HOSTNAME"),
        'port': int(os.environ.get("MONGODB_PORT")),
        'uuidRepresentation': 'standard'
    }
