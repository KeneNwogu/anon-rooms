from datetime import datetime

from flask import request
from flask_socketio import emit, Namespace

from application import app, db, socket
from application.auth_utils import create_token
from application.models import User, Message, Poll, Option
from application.polls_namespace import PublicPollsNamespace
from application.private_namespace import PrivateNamespace
from application.public_namespace import PublicNamespace

socket.on_namespace(PrivateNamespace('/private'))
socket.on_namespace(PublicNamespace('/public'))
socket.on_namespace(PublicPollsNamespace('/polls'))


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


@app.route('/poll', methods=['POST'])
def create_poll():
    data = request.get_json(force=True)
    if not data.get('caption'):
        return {"success": False, "message": "Poll must have a name"}
    poll = Poll(caption=data.get('caption'))
    options = data.get('options')
    if type(options) != list:
        return {"success": False, "message": "invalid request format"}

    if len(options) < 2:
        return {"success": False, "message": "a minimum of two options are allowed per poll"}

    if len(options) > 4:
        return {"success": False, "message": "you exceeded the amount of options allowed per poll"}

    db.session.add(poll)
    db.session.flush()
    for o in options:
        if not o.get('name'):
            return {"success": False, "message": "Option must have a name"}
        option = Option(name=o.get('name'))
        option.poll_id = poll.id

    return {"success": True, "message": "successfully created poll"}


@socket.on_error_default
def default_error_handler(e):
    session_id = request.sid
    emit('error', {'error': e.error}, to=session_id)
