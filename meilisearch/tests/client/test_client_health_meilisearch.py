import meilisearch

def test_health(client):
    """Tests checking the health of the MeiliSearch instance."""
    response = client.health()
    assert response['status'] == 'available'

def test_is_healthy(client):
    """Tests checking if is_healthy return true when MeiliSearch instance is available."""
    response = client.is_healthy()
    assert response is True

def test_is_healthy_bad_route():
    """Tests checking if is_healthy returns false when trying to reach a bad URL."""
    client = meilisearch.Client("http://wrongurl:1234")
    response = client.is_healthy()
    assert response is False
