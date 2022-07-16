from flask_socketio import Namespace, emit
from flask import request
from application import db
from application.auth_utils import login_required
from application.models import User


class PrivateNamespace(Namespace):
    namespace = '/private'

    @login_required
    def on_connect(self, payload):
        # store new session id back to logged in user
        user = User.query.get(int(payload.get('user_id')))
        user.session_id = request.sid
        db.session.commit()
        emit('client_connected', namespace=self.namespace)

    def on_send_message(self, data):
        # get and load messages to private user
        pass

    def on_disconnect(self):
        pass
