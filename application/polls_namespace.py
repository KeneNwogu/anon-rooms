from flask_socketio import Namespace


class PollsNamespace(Namespace):
    def on_connect(self):
        pass

    def on_vote(self, data):
        poll_id = data.get('poll_id')
        option_id = data.get('option_id')

