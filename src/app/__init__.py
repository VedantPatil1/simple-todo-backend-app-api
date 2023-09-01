import os
import warnings
from flask import Flask
from flask_mongoengine import MongoEngine

from app.config import Config


db = MongoEngine()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    # Flask-MongoEngine has not been updated to resolve flask json deprecation
    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        module="flask.json")

    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        message="'app.json_encoder' is deprecated and will be removed in Flask 2.3."  # noqa
    )

    @app.route('/', methods=['GET'])
    def hello():
        return 'Hello, World!'

    # Configuration for chosing test_config while testing.
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)

    return app
