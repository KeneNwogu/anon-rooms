def test_connect(private_client):
    assert private_client.is_connected(namespace='/private') is not False


def test_receiving_messages_event(public_client, private_client):
    pass