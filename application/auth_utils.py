from functools import wraps
from flask import request


class AuthError(Exception):
    def __init__(self, error, status):
        self.error = error
        self.status = status


def create_token(user):
    pass


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


def login_required():
    def login_required_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_auth_token_header()
            # TODO verify token
            return f(*args, **kwargs)
        return wrapper
    return login_required_decorator
