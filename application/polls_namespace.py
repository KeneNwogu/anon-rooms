from flask_socketio import Namespace, emit

from application import db
from application.models import Option, Poll


class PublicPollsNamespace(Namespace):
    def on_connect(self):
        # load polls
        polls = [poll.to_dict() for poll in Poll.query.all()]
        emit('load_votes', polls)  # Client event for loading votes

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

