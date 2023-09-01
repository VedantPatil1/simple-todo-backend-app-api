import pytest
from mongoengine.connection import disconnect

from app import create_app


@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "DEBUG": False,
        'MONGODB_SETTINGS': {
            'db': 'test_db',
            'host': 'localhost',
            'port': 27017,
            'uuidRepresentation': 'standard'
        }}
    app = create_app(test_config=test_config)
    yield app

    disconnect()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def dev_app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    yield app
    disconnect()
