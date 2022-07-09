from datetime import datetime
from application import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), nullable=False)
    session_id = db.Column(db.String(50), nullable=True)
    messages = db.relationship('Message', backref='receiver', lazy=True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
