import os
import multiprocessing
import pytest
from application import app, socket, db
from dotenv import load_dotenv
import socketio

load_dotenv()


def run_server():
    socket.run(app)


def connect_client(client):
    client.connect('http://127.0.0.1:5000/')


@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TEST_DATABASE_URI')
    db.create_all()
    test_client = socket.test_client(app)
    test_client.connect()

    yield test_client
    db.drop_all()
