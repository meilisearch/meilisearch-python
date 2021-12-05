
def test_get_keys(client):
    """Tests if public and private keys have been generated and can be retrieved."""
    response = client.get_keys()
    assert isinstance(response, dict)
    assert 'public' in response
    assert 'private' in response
    assert response['public'] is not None
    assert response['private'] is not None
