from datetime import datetime

from flask_socketio import Namespace, emit
from flask import request
from application import db
from application.auth_utils import login_required
from application.models import User, Message


class PrivateNamespace(Namespace):
    namespace = '/private'

    @login_required
    def on_connect(self, payload):
        # store new session id back to logged in user
        user = User.query.get(int(payload.get('user_id')))
        user.session_id = request.sid
        db.session.commit()
        messages = [message.to_dict() for message in user.messages]

        # client event to load messages after connection
        emit('client_connected', messages, namespace=self.namespace, room=user.session_id)

    def on_send_message(self, data):
        # get and load messages to private user
        receiver_username = data.get('username')
        receiver = User.query.filter_by(username=receiver_username).first()
        if receiver:
            text_message = data.get('message')
            twitter_at = data.get('twitter_at')
            message = Message(text=text_message, twitter_at=twitter_at, timestamp=datetime.utcnow())
            db.session.add(message)
            db.session.commit()
            if receiver.session_id:
                emit('received_message', message.to_dict(), room=receiver.session_id)
            else:
                # TODO store in redis cache
                pass
        pass

    def on_disconnect(self):
        session_id = request.sid
        disconnected_user = User.query.filter_by(session_id=session_id).first()
        if disconnected_user:
            # set user as disconnected
            pass
