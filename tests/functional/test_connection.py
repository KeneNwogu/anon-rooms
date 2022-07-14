import json
from dotenv import load_dotenv

from application.models import Message

load_dotenv()


def test_connection(client):
    assert client.is_connected() is not False
    assert type(client.get_received()) == list


def test_public_messages(client):
    message_text = 'Hello World - public message'
    client.emit('post_message', {'message': message_text, 'twitter_at': False})
    # check that message was stored on the db
    message = Message.query.filter_by(text=message_text).all()[0]
    assert len(message) >= 1

    data = client.get_received()
    print(data)
    assert data.get('message') == message_text


