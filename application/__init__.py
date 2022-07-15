import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO


load_dotenv()

app = Flask(__name__)

# app configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
socket = SocketIO(app)

from application import routes
from application.public_namespace import PublicNamespace

# socket.on_namespace(PublicNamespace('/public'))