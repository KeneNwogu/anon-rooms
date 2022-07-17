def test_connect(private_client):
    assert private_client.is_connected(namespace='/private') is not False