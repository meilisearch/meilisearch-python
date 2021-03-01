# pylint: disable=invalid-name

NEW_SEARCHABLE_ATTRIBUTES = ['something', 'random']

def test_get_searchable_attributes(empty_index, small_movies):
    """Tests getting the searchable attributes on an empty and populated index."""
    index = empty_index()
    response = index.get_searchable_attributes()
    assert isinstance(response, list)
    assert response == ['*']
    response = index.add_documents(small_movies, primary_key='id')
    index.wait_for_pending_update(response['updateId'])
    get_attributes = index.get_searchable_attributes()
    assert get_attributes == ['*']


def test_update_searchable_attributes(empty_index):
    """Tests updating the searchable attributes."""
    index = empty_index()
    response = index.update_searchable_attributes(NEW_SEARCHABLE_ATTRIBUTES)
    assert isinstance(response, dict)
    assert 'updateId' in response
    index.wait_for_pending_update(response['updateId'])
    response = index.get_searchable_attributes()
    assert len(response) == len(NEW_SEARCHABLE_ATTRIBUTES)
    for attribute in NEW_SEARCHABLE_ATTRIBUTES:
        assert attribute in response

def test_reset_searchable_attributes(empty_index):
    """Tests resetting the searchable attributes setting to its default value."""
    index = empty_index()
    # Update the settings first
    response = index.update_searchable_attributes(NEW_SEARCHABLE_ATTRIBUTES)
    update = index.wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    # Check the settings have been correctly updated
    response = index.get_searchable_attributes()
    assert len(response) == len(NEW_SEARCHABLE_ATTRIBUTES)
    for attribute in NEW_SEARCHABLE_ATTRIBUTES:
        assert attribute in response
    # Check the reset of the settings
    response = index.reset_searchable_attributes()
    assert isinstance(response, dict)
    assert 'updateId' in response
    index.wait_for_pending_update(response['updateId'])
    response = index.get_searchable_attributes()
    assert response == ['*']
