

def test_get_stats(indexes_sample):
    """Tests getting stats of a single index"""
    response = indexes_sample[0].get_stats()
    assert isinstance(response, object)
    assert 'numberOfDocuments' in response
    assert response['numberOfDocuments'] == 0
    assert 'isIndexing' in response
