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
    # check that message was stored on the db
    message = list(Message.query.filter_by(text=message_text))
    assert 1 == len(message)
    del message

    # data = client.get_received(namespace='/public')
    # print(data)
    # assert data.get('message') == message_text


