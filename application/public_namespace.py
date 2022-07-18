import json
from datetime import datetime
from flask import request
from flask_socketio import Namespace, emit

from application import db, redis_db
from application.models import Message, User


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
        # Client event for adding message to

    def on_send_private_message(self, data):
        # get and load messages to private user
        receiver_username = data.get('username')
        receiver = User.query.filter_by(username=receiver_username).first()
        if receiver:
            text_message = data.get('message')
            twitter_at = data.get('twitter_at')
            message = Message(text=text_message, twitter_at=twitter_at, timestamp=datetime.utcnow(),
                              user_id=receiver.id)
            db.session.add(message)
            db.session.commit()
            if receiver.active_now:
                # handle private message in client
                emit('received_private_message', message.to_dict(), room=receiver.session_id, namespace='/private')
            else:
                # TODO store in redis cache
                serialized_message = json.dumps(message.to_dict())
                redis_db.lpush(f'user:{receiver.id}', serialized_message)

        else:
            return False
