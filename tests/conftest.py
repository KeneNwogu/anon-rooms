import os
import multiprocessing
import pytest
from application import app, socket, db
from dotenv import load_dotenv
import socketio

from application.auth_utils import create_token
from application.models import User

load_dotenv()

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TEST_DATABASE_URI')


@pytest.fixture(scope='module')
def public_client():
    db.drop_all()
    db.create_all()
    public_test_client = socket.test_client(app, namespace='/public')  # PublicNamespace client
    yield public_test_client
    public_test_client.disconnect(namespace='/public')
    db.drop_all()


@pytest.fixture(scope='module')
def private_client():
    db.drop_all()
    db.create_all()
    # create test user
    test_password = 'password'
    user = User(username='test_user')
    user.set_password(test_password)
    db.session.add(user)
    db.session.commit()
    token = create_token(user)
    headers = {'Authorization': f'Bearer {token}'}
    private_test_client = socket.test_client(app, namespace='/private', headers=headers)  # PrivateNamespace client
    yield private_test_client
    private_test_client.disconnect(namespace='/private')
    db.drop_all()