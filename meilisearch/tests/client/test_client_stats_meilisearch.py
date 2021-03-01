import pytest

@pytest.mark.usefixtures("indexes_sample")
def test_get_all_stats(client):
    """Tests getting all stats."""
    response = client.get_all_stats()
    assert isinstance(response, dict)
    assert 'databaseSize' in response
    assert isinstance(response['databaseSize'], int)
    assert 'lastUpdate' in response
    assert 'indexes' in response
    assert 'indexUID' in response['indexes']
    assert 'indexUID2' in response['indexes']
