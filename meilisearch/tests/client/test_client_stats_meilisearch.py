

def test_get_all_stats(client, sample_indexes):
    """Tests getting all stats after creating two indexes"""
    response = client.get_all_stats()
    assert isinstance(response, object)
    assert 'databaseSize' in response
    assert isinstance(response['databaseSize'], int)
    assert 'lastUpdate' in response
    assert 'indexes' in response
    assert 'indexUID' in response['indexes']
    assert 'indexUID2' in response['indexes']
