from server import secrets


class Config(object):
    BASIC_AUTH_USERNAME = secrets.BASIC_AUTH_USERNAME
    BASIC_AUTH_PASSWORD = secrets.BASIC_AUTH_PASSWORD 
    BASIC_AUTH_FORCE = True
    SECRET_KEY = secrets.SECRET_KEY
