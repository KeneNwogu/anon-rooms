from datetime import datetime

from flask import request
from flask_socketio import Namespace, emit

from application import db, socket
from application.models import Message


class PublicNamespace(Namespace):
    namespace = '/public'

    def on_connect(self):
        messages = [message.to_dict() for message in Message.query.all()]
        emit('client_connected', messages, namespace=self.namespace)

    def on_broadcast_message(self, data):
        text_message = data.get('message')
        twitter_at = data.get('twitter_at')
        message = Message(text=text_message, twitter_at=twitter_at, timestamp=datetime.utcnow())
        db.session.add(message)
        db.session.commit()

        emit('general_message', message.to_dict(), broadcast=True, namespace=self.namespace)
        # Client event for adding message to stack