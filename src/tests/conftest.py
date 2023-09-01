import pytest
from mongoengine.connection import disconnect
import os

from app import create_app
from app.models import Task


@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "DEBUG": False,
        'MONGODB_SETTINGS': {
            'db': 'test_db',
            'username': os.environ.get("MONGODB_USERNAME"),
            'password': os.environ.get("MONGODB_PASSWORD"),
            'host': os.environ.get("MONGODB_HOSTNAME"),
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
def set_up(app):
    with app.app_context():
        Task.objects.delete()


@pytest.fixture
def dev_app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    yield app
    disconnect()
