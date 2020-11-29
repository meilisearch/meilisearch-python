
NEW_SEARCHABLE_ATTRIBUTES = ['something', 'random']

def test_get_searchable_attributes(indexes_sample, small_movies):
    """Tests getting the searchable attributes on an empty and populated index"""
    response = indexes_sample[0].get_searchable_attributes()
    assert isinstance(response, object)
    assert response == ['*']
    response = indexes_sample[0].add_documents(small_movies, primary_key='id')
    indexes_sample[0].wait_for_pending_update(response['updateId'])
    get_attributes = indexes_sample[0].get_searchable_attributes()
    assert get_attributes == ['*']


def test_update_searchable_attributes(indexes_sample):
    """Tests updating the searchable attributes"""
    response = indexes_sample[0].update_searchable_attributes(NEW_SEARCHABLE_ATTRIBUTES)
    assert isinstance(response, object)
    assert 'updateId' in response
    indexes_sample[0].wait_for_pending_update(response['updateId'])
    response = indexes_sample[0].get_searchable_attributes()
    assert len(response) == len(NEW_SEARCHABLE_ATTRIBUTES)
    for attribute in NEW_SEARCHABLE_ATTRIBUTES:
        assert attribute in response

def test_reset_searchable_attributes(indexes_sample):
    """Tests reseting searchable attributes"""
    response = indexes_sample[0].reset_searchable_attributes()
    assert isinstance(response, object)
    assert 'updateId' in response
    indexes_sample[0].wait_for_pending_update(response['updateId'])
    response = indexes_sample[0].get_searchable_attributes()
    assert response == ['*']
