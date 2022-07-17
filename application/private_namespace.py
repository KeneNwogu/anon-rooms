from datetime import datetime

from flask_socketio import Namespace, emit
from flask import request
from application import db
from application.auth_utils import login_required
from application.models import User, Message


class PrivateNamespace(Namespace):
    namespace = '/private'

    @login_required
    def on_connect(self, **kwargs):
        # store new session id back to logged in user
        payload = kwargs['payload']
        user = User.query.get(int(payload.get('user_id')))
        if user.session_id:
            # TODO if user has logged in before, reset session id and load only recent messages
            messages = []
            pass
        else:
            messages = [message.to_dict() for message in user.messages]

        user.session_id = request.sid
        user.active_now = True
        db.session.commit()
        # client event to load messages after connection
        emit('client_connected', messages, namespace=self.namespace, room=user.session_id)


    def on_disconnect(self):
        session_id = request.sid
        disconnected_user = User.query.filter_by(session_id=session_id).first()
        if disconnected_user:
            disconnected_user.active_now = False
            db.session.commit()
            emit('user_disconnected', disconnected_user.to_dict(), broadcast=True, namespace='/public')