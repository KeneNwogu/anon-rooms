import json
from dotenv import load_dotenv

from application.models import Message

load_dotenv()


def test_connection(client):
    assert client.is_connected(namespace='/public') is not False
    assert type(client.get_received('/public')) == list


def test_public_messages():
    message_text = 'Hello World - public message'
    # client.emit('broadcast_message', {'message': message_text, 'twitter_at': False}, namespace='/public')
    # check that message was stored on the db

    message = Message.query.filter_by(text=message_text).all()
    assert len(message) >= 1

    # data = client.get_received(namespace='/public')
    # print(data)
    # assert data.get('message') == message_text


