# pylint: disable=invalid-name

def test_get_attributes_for_faceting(indexes_sample):
    """ Tests getting the attributes for faceting """
    response = indexes_sample[0].get_attributes_for_faceting()
    assert isinstance(response, object)
    assert response == []

def test_update_attributes_for_faceting(indexes_sample):
    """Tests updating the attributes for faceting"""
    attributes_for_faceting = ['title', 'release_date']

    response = indexes_sample[0].update_attributes_for_faceting(attributes_for_faceting)
    indexes_sample[0].wait_for_pending_update(response['updateId'])
    get_attributes_new = indexes_sample[0].get_attributes_for_faceting()
    assert len(get_attributes_new) == len(attributes_for_faceting)
    get_attributes = indexes_sample[0].get_attributes_for_faceting()
    for attribute in attributes_for_faceting:
        assert attribute in get_attributes

def test_reset_attributes_for_faceting(indexes_sample):
    """Tests the reset of attributes for faceting to default values (in dataset)"""
    response = indexes_sample[0].reset_attributes_for_faceting()
    assert isinstance(response, object)
    assert 'updateId' in response
    indexes_sample[0].wait_for_pending_update(response['updateId'])
    response = indexes_sample[0].get_attributes_for_faceting()
    assert isinstance(response, object)
    assert response == []
