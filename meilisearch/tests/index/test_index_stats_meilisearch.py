

def test_get_stats(empty_index):
    """Tests getting stats of an index."""
    response = empty_index().get_stats()
    assert isinstance(response, dict)
    assert 'numberOfDocuments' in response
    assert response['numberOfDocuments'] == 0
    assert 'isIndexing' in response
