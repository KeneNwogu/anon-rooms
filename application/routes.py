from flask import request
from application import app, db, socket
from application.models import User, Message
from application.auth_utils import create_token
from flask_socketio import send, emit
import json


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
        user_token = create_token(user)
        return {
            "success": True,
            "token": user_token
        }

# TODO implement two namespaces for general and authenticated rooms
@socket.on('connect')
def verify_connection():
    if request.headers.get('Authorization'):
        # TODO perform auth tasks and place in a special room
        # TODO assign a session id to the db of each authenticated user
        pass
    else:
        session_id = request.sid
        messages = json.dumps(Message.query.all())
        # emit('connected',  messages)


@socket.on('general_message')
def broadcast_message(data):
    # TODO broadcast message and store in db
    pass