# pylint: disable=invalid-name

SORTABLE_ATTRIBUTES = ['title', 'release_date']

def test_get_sortable_attributes(empty_index):
    """Tests getting the sortable attributes."""
    response = empty_index().get_sortable_attributes()
    assert isinstance(response, list)
    assert response == []

def test_update_sortable_attributes(empty_index):
    """Tests updating the sortable attributes."""
    index = empty_index()
    response = index.update_sortable_attributes(SORTABLE_ATTRIBUTES)
    index.wait_for_pending_update(response['updateId'])
    get_attributes = index.get_sortable_attributes()
    assert len(get_attributes) == len(SORTABLE_ATTRIBUTES)
    for attribute in SORTABLE_ATTRIBUTES:
        assert attribute in get_attributes

def test_update_sortable_attributes_to_none(empty_index):
    """Tests updating the sortable attributes at null."""
    index = empty_index()
    # Update the settings first
    response = index.update_sortable_attributes(SORTABLE_ATTRIBUTES)
    update = index.wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    # Check the settings have been correctly updated
    get_attributes = index.get_sortable_attributes()
    for attribute in SORTABLE_ATTRIBUTES:
        assert attribute in get_attributes
    # Launch test to update at null the setting
    response = index.update_sortable_attributes(None)
    index.wait_for_pending_update(response['updateId'])
    response = index.get_sortable_attributes()
    assert response == []

def test_reset_sortable_attributes(empty_index):
    """Tests resetting the sortable attributes setting to its default value"""
    index = empty_index()
    # Update the settings first
    response = index.update_sortable_attributes(SORTABLE_ATTRIBUTES)
    update = index.wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    # Check the settings have been correctly updated
    get_attributes = index.get_sortable_attributes()
    assert len(get_attributes) == len(SORTABLE_ATTRIBUTES)
    for attribute in SORTABLE_ATTRIBUTES:
        assert attribute in get_attributes
    # Check the reset of the settings
    response = index.reset_sortable_attributes()
    assert isinstance(response, dict)
    assert 'updateId' in response
    index.wait_for_pending_update(response['updateId'])
    response = index.get_sortable_attributes()
    assert isinstance(response, list)
    assert response == []
