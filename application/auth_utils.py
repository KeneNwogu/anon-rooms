from functools import wraps
from flask import request
import jwt
from application import app


class AuthError(Exception):
    def __init__(self, error, status):
        self.error = error
        self.status = status


def create_token(user):
    payload = user.to_dict()
    token = jwt.encode(payload, app.config.get('SECRET_KEY'), "HS256")
    return token


def get_auth_token_header():
    headers = request.headers.get('Authorization')
    if not headers:
        raise AuthError('No Authorization header found', 401)
    if len(headers.split()) != 2:
        raise AuthError('Invalid token found', 401)
    token_type, token = headers.split()
    if token_type.lower() != 'bearer':
        raise AuthError('Incorrect token type found', 401)
    return token


def verify_token(token):
    pass


def login_required(f):
    @wraps(f)
    def login_required_decorator(*args, **kwargs):
        token = get_auth_token_header()
        payload = jwt.decode(token, app.config.get('SECRET_KEY'), 'HS256')
        return f(payload, *args, **kwargs)
    return login_required_decorator
