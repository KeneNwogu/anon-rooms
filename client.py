import socketio

from application import db
from application.auth_utils import create_token
from application.models import User

db.drop_all()
db.create_all()

test_password = 'password'
user = User(username='test_user')
user.set_password(test_password)
db.session.add(user)
db.session.commit()
token = create_token(user)
headers = {'Authorization': f'Bearer {token}'}

client = socketio.Client()
client.connect('http://127.0.0.1:5000/', namespaces=['/private'], headers=headers)

# print(client.get_sid(namespace='/public'))
# client.emit('general_message', data='hello general public')
client.emit('client_connected', data='hmmm', namespace='/private')
message_text = 'Hello World - public message'
# client.emit('broadcast_message', {'message': message_text, 'twitter_at': False}, namespace='/public')
client.emit('send_message', data={"username": "test_user", "message": message_text}, namespace='/private')


def test_connect(messages):
    # socketio.emit emits event to current state
    print('connected to server from client')
    print('connected messages', messages)


def post_message_handler(message):
    print('received messages', message.get('message'))


client.on('client_connected', test_connect, namespace='/private')
client.on('received_message', test_connect, namespace='/private')
# client.on('general_message', post_message_handler, namespace='/public')
