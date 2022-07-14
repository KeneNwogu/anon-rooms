from flask_socketio import Namespace


class PublicNamespace(Namespace):
    def on_connect(self):
        pass

    def on_personal_message(self, data):
        pass
