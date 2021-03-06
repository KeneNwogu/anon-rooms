from datetime import datetime
from application import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), nullable=False, unique=True)
    session_id = db.Column(db.String(50), nullable=True)
    messages = db.relationship('Message', backref='receiver', lazy=True)
    password_hash = db.Column(db.String(120), nullable=False)
    active_now = db.Column(db.Boolean, nullable=False, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "user_id": self.id,
            "username": self.username,
            "session_id": self.session_id,
            "active_now": self.active_now
        }


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=True)
    twitter_at = db.Column(db.Boolean, nullable=True)

    def to_dict(self):
        return {
            "message": self.text,
            "timestamp": self.timestamp.strftime('%d/%m/%Y, %H:%M:%S'),
            "twitter_at": True if self.twitter_at else False
        }


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.Text)
    options = db.relationship('Option', backref='poll', lazy=True)

    @property
    def total_votes(self):
        return sum([o.votes for o in self.options])

    def to_dict(self):
        return {
            'vote_id': self.id,
            'options': [o.to_dict() for o in self.options]
        }


class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
    votes = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'option_id': self.id,
            'votes': self.votes
        }
