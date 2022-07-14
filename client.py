import socketio

client = socketio.Client()
client.connect('http://127.0.0.1:5000')

print(client.get_sid())
# client.emit('general_message', data='hello general public')
client.emit('client_connected', data='hmmm')
message_text = 'Hello World - public message'
client.emit('post_message', {'message': message_text, 'twitter_at': False})


def test_connect(messages):
    # socketio.emit emits event to current state
    print('connected to server from client')
    print(messages)


def post_message_handler(message):
    print(message.get('message'))


client.on('client_connected', test_connect)
client.on('general_message', post_message_handler)
