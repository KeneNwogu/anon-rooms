import socketio

client = socketio.Client()
client.connect('http://127.0.0.1:5000/', namespaces=['/public'])

print(client.get_sid(namespace='/public'))
# client.emit('general_message', data='hello general public')
client.emit('client_connected', data='hmmm', namespace='/public')
message_text = 'Hello World - public message'
client.emit('broadcast_message', {'message': message_text, 'twitter_at': False}, namespace='/public')


def test_connect(messages):
    # socketio.emit emits event to current state
    print('connected to server from client')
    print('connected messages', messages)


def post_message_handler(message):
    print('received messages', message.get('message'))


client.on('client_connected', test_connect, namespace='/public')
client.on('general_message', post_message_handler, namespace='/public')
