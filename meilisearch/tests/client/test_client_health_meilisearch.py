
def test_health(client):
    """Tests checking the health of MeiliSearch instance"""
    response = client.health()
    assert response.status_code >= 200 and response.status_code < 400
