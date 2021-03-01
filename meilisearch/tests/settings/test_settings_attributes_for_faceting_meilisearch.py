# pylint: disable=invalid-name

ATTRIBUTES_FOR_FACETING = ['title', 'release_date']

def test_get_attributes_for_faceting(empty_index):
    """Tests getting the attributes for faceting."""
    response = empty_index().get_attributes_for_faceting()
    assert isinstance(response, list)
    assert response == []

def test_update_attributes_for_faceting(empty_index):
    """Tests updating the attributes for faceting."""
    index = empty_index()
    response = index.update_attributes_for_faceting(ATTRIBUTES_FOR_FACETING)
    index.wait_for_pending_update(response['updateId'])
    get_attributes_new = index.get_attributes_for_faceting()
    assert len(get_attributes_new) == len(ATTRIBUTES_FOR_FACETING)
    get_attributes = index.get_attributes_for_faceting()
    for attribute in ATTRIBUTES_FOR_FACETING:
        assert attribute in get_attributes

def test_reset_attributes_for_faceting(empty_index):
    """Tests resetting the attributes for faceting setting to its default value"""
    index = empty_index()
    # Update the settings first
    response = index.update_attributes_for_faceting(ATTRIBUTES_FOR_FACETING)
    update = index.wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    # Check the settings have been correctly updated
    get_attributes_new = index.get_attributes_for_faceting()
    assert len(get_attributes_new) == len(ATTRIBUTES_FOR_FACETING)
    get_attributes = index.get_attributes_for_faceting()
    for attribute in ATTRIBUTES_FOR_FACETING:
        assert attribute in get_attributes
    # Check the reset of the settings
    response = index.reset_attributes_for_faceting()
    assert isinstance(response, dict)
    assert 'updateId' in response
    index.wait_for_pending_update(response['updateId'])
    response = index.get_attributes_for_faceting()
    assert isinstance(response, list)
    assert response == []
