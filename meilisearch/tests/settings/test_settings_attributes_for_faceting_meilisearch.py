# pylint: disable=invalid-name

def test_get_attributes_for_faceting(empty_index):
    """ Tests getting the attributes for faceting """
    response = empty_index().get_attributes_for_faceting()
    assert isinstance(response, object)
    assert response == []

def test_update_attributes_for_faceting(empty_index):
    """Tests updating the attributes for faceting"""
    attributes_for_faceting = ['title', 'release_date']
    index = empty_index()
    response = index.update_attributes_for_faceting(attributes_for_faceting)
    index.wait_for_pending_update(response['updateId'])
    get_attributes_new = index.get_attributes_for_faceting()
    assert len(get_attributes_new) == len(attributes_for_faceting)
    get_attributes = index.get_attributes_for_faceting()
    for attribute in attributes_for_faceting:
        assert attribute in get_attributes

def test_reset_attributes_for_faceting(empty_index):
    """Tests the reset of attributes for faceting to default values (in dataset)"""
    index = empty_index()
    response = index.reset_attributes_for_faceting()
    assert isinstance(response, object)
    assert 'updateId' in response
    index.wait_for_pending_update(response['updateId'])
    response = index.get_attributes_for_faceting()
    assert isinstance(response, object)
    assert response == []
