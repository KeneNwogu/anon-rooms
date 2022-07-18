from flask_socketio import Namespace, emit

from application import db
from application.models import Option, Poll


class PublicPollsNamespace(Namespace):
    namespace = "/polls"

    def on_connect(self):
        # load polls
        polls = [poll.to_dict() for poll in Poll.query.all()]
        emit('load_votes', polls, namespace=self.namespace)  # Client event for loading votes

    def create_vote(self, data):
        options = data.get('options')

        if type(options) != list:
            # TODO create socket error event
            return

        if len(options) > 4:
            # TODO create socket error event
            return

        poll_name = data.get('caption')
        with db.session.begin():
            if not poll_name:
                # TODO create socket error event
                return
            poll = Poll(caption=poll_name)
            db.session.add(poll)
            db.session.flush()
            poll_id = poll.id
            for o in options:
                # TODO upload image
                image_url = None
                if not o.get('name'):
                    # TODO create socket error event
                    return
                try:
                    option = Option(name=o.get('name'), poll_id=poll_id, image_url=image_url)
                    db.session.add(option)
                except Exception:
                    # TODO create socket error event
                    return
            db.session.commit()
            vote = Poll.query.get(int(poll_id))
            emit('new_vote', vote.to_dict(), namespace=self.namespace)

    def on_vote(self, data):
        poll_id = data.get('poll_id')
        option_id = data.get('option_id')
        option = Option.query.get(int(option_id))
        if option:
            option.votes += 1
            db.session.commit()
            vote = Poll.query.get(int(poll_id))
            emit('vote_update', vote.to_dict(), broadcast=True)  # Client event for updating votes
        else:
            return False

