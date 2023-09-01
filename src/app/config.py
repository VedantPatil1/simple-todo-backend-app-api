import os


class Config:
    MONGODB_SETTINGS = {
        'db': os.environ.get("MONGODB_DATABASE"),
        'username': os.environ.get("MONGODB_USERNAME"),
        'password': os.environ.get("MONGODB_PASSWORD"),
        'host': os.environ.get("MONGODB_HOSTNAME"),
        'port': int(os.environ.get("MONGODB_PORT")),
        'uuidRepresentation': 'standard'
    }
