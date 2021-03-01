

NEW_DISTINCT_ATTRIBUTE = 'title'
DEFAULT_DISTINCT_ATTRIBUTE = None

def test_get_distinct_attribute(empty_index):
    """Tests geting the distinct attribute."""
    response = empty_index().get_distinct_attribute()
    assert response == DEFAULT_DISTINCT_ATTRIBUTE

def test_update_distinct_attribute(empty_index):
    """Tests updating a custom distinct attribute."""
    index = empty_index()
    response = index.update_distinct_attribute(NEW_DISTINCT_ATTRIBUTE)
    assert isinstance(response, dict)
    assert 'updateId' in response
    index.wait_for_pending_update(response['updateId'])
    response = index.get_distinct_attribute()
    assert isinstance(response, str)
    assert response == NEW_DISTINCT_ATTRIBUTE

def test_reset_distinct_attribute(empty_index):
    """Tests resetting the distinct attribute setting to its default value."""
    index = empty_index()
    # Update the settings first
    response = index.update_distinct_attribute(NEW_DISTINCT_ATTRIBUTE)
    update = index.wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    # Check the settings have been correctly updated
    response = index.get_distinct_attribute()
    assert isinstance(response, str)
    assert response == NEW_DISTINCT_ATTRIBUTE
    # Check the reset of the settings
    response = index.reset_distinct_attribute()
    assert isinstance(response, dict)
    assert 'updateId' in response
    index.wait_for_pending_update(response['updateId'])
    response = index.get_distinct_attribute()
    assert response == DEFAULT_DISTINCT_ATTRIBUTE
