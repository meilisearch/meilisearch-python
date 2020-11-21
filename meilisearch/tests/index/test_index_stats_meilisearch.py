

def test_get_stats(sample_indexes):
    """Tests getting stats of a single index"""
    response = sample_indexes[0].get_stats()
    assert isinstance(response, object)
    assert 'numberOfDocuments' in response
    assert response['numberOfDocuments'] == 0
    assert 'isIndexing' in response
