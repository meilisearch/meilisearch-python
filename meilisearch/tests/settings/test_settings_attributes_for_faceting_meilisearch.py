

def test_get_attributes_for_faceting(sample_indexes):
    """ Tests getting the attributes for faceting """
    response = sample_indexes[0].get_attributes_for_faceting()
    assert isinstance(response, object)
    assert response == []

def test_update_attributes_for_faceting(sample_indexes):
    """Tests updating the attributes for faceting"""
    attributes_for_faceting = ['title', 'release_date']

    response = sample_indexes[0].update_attributes_for_faceting(attributes_for_faceting)
    sample_indexes[0].wait_for_pending_update(response['updateId'])
    get_attributes_new = sample_indexes[0].get_attributes_for_faceting()
    assert len(get_attributes_new) == len(attributes_for_faceting)
    get_attributes = sample_indexes[0].get_attributes_for_faceting()
    for attribute in attributes_for_faceting:
        assert attribute in get_attributes

def test_reset_attributes_for_faceting(sample_indexes):
    """Tests the reset of attributes for faceting to default values (in dataset)"""
    response = sample_indexes[0].reset_attributes_for_faceting()
    assert isinstance(response, object)
    assert 'updateId' in response
    sample_indexes[0].wait_for_pending_update(response['updateId'])
    response = sample_indexes[0].get_attributes_for_faceting()
    assert isinstance(response, object)
    assert response == []
