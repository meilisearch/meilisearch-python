
def test_health(client):
    """Tests checking the health of the MeiliSearch instance."""
    response = client.health()
    assert response['status'] == 'available'
