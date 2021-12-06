# pylint: disable=invalid-name

FILTERABLE_ATTRIBUTES = ['title', 'release_date']

def test_get_filterable_attributes(empty_index):
    """Tests getting the filterable attributes."""
    response = empty_index().get_filterable_attributes()
    assert isinstance(response, list)
    assert response == []

def test_update_filterable_attributes(empty_index):
    """Tests updating the filterable attributes."""
    index = empty_index()
    response = index.update_filterable_attributes(FILTERABLE_ATTRIBUTES)
    index.wait_for_pending_update(response['updateId'])
    get_attributes = index.get_filterable_attributes()
    assert len(get_attributes) == len(FILTERABLE_ATTRIBUTES)
    for attribute in FILTERABLE_ATTRIBUTES:
        assert attribute in get_attributes

def test_update_filterable_attributes_to_none(empty_index):
    """Tests updating the filterable attributes at null."""
    index = empty_index()
    # Update the settings first
    response = index.update_filterable_attributes(FILTERABLE_ATTRIBUTES)
    update = index.wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    # Check the settings have been correctly updated
    get_attributes = index.get_filterable_attributes()
    for attribute in FILTERABLE_ATTRIBUTES:
        assert attribute in get_attributes
    # Launch test to update at null the setting
    response = index.update_filterable_attributes(None)
    index.wait_for_pending_update(response['updateId'])
    response = index.get_filterable_attributes()
    assert response == []

def test_reset_filterable_attributes(empty_index):
    """Tests resetting the filterable attributes setting to its default value"""
    index = empty_index()
    # Update the settings first
    response = index.update_filterable_attributes(FILTERABLE_ATTRIBUTES)
    update = index.wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    # Check the settings have been correctly updated
    get_attributes = index.get_filterable_attributes()
    assert len(get_attributes) == len(FILTERABLE_ATTRIBUTES)
    for attribute in FILTERABLE_ATTRIBUTES:
        assert attribute in get_attributes
    # Check the reset of the settings
    response = index.reset_filterable_attributes()
    assert isinstance(response, dict)
    assert 'updateId' in response
    index.wait_for_pending_update(response['updateId'])
    response = index.get_filterable_attributes()
    assert isinstance(response, list)
    assert response == []
