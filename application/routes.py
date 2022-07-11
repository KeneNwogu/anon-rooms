from flask import request
from application import app, db, socket
from application.models import User
from flask_socketio import send, emit


@app.route('/register')
def register_user():
    data = request.get_json(force=True)
    if not data.get('username') or not data.get('password'):
        return {'success': False, 'message': 'Incomplete data passed'}, 400
    username = data['username']
    password = data['password']
    if User.query.filter(username):
        return {'success': False, 'message': 'User already exists'}, 400
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()


@app.route('/login')
def login_user():
    data = request.get_json(force=True)
    if not data.get('username') or not data.get('password'):
        return {'success': False, 'message': 'Authentication details were not provided'}, 401
    username = data['username']
    password = data['password']
    user = User.query.filter(username)
    if not user:
        return {'success': False, 'message': 'Authentication details were not provided'}, 401
    if user.check_password(password):
        # TODO implement token auth
        return 'Token'


@socket.on('connect')
def verify_connection(data):
    pass