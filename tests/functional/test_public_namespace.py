from dotenv import load_dotenv

from application import db
from application.models import Message

load_dotenv()


def test_connection(public_client):
    assert public_client.is_connected(namespace='/public') is not False
    assert type(public_client.get_received('/public')) == list


def test_public_messages(public_client):
    message_text = 'Hello World - public message'
    public_client.emit('broadcast_message', {'message': message_text, 'twitter_at': False}, namespace='/public')

    data = public_client.get_received(namespace='/public')
    assert data[0].get('args')[0].get('message') == message_text


