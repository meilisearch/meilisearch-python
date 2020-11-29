
DISPLAYED_ATTRIBUTES = ['id', 'release_date', 'title', 'poster', 'overview', 'genre']


def test_get_displayed_attributes(indexes_sample, small_movies):
    """ Tests getting the displayed attributes before and after indexing a dataset """
    response = indexes_sample[0].get_displayed_attributes()
    assert isinstance(response, object)
    assert response == ['*']
    response = indexes_sample[0].add_documents(small_movies, primary_key='id')
    indexes_sample[0].wait_for_pending_update(response['updateId'])
    get_attributes = indexes_sample[0].get_displayed_attributes()
    assert get_attributes == ['*']

def test_update_displayed_attributes(indexes_sample):
    """Tests updating the displayed attributes"""
    response = indexes_sample[0].update_displayed_attributes(DISPLAYED_ATTRIBUTES)
    indexes_sample[0].wait_for_pending_update(response['updateId'])
    get_attributes_new = indexes_sample[0].get_displayed_attributes()
    assert len(get_attributes_new) == len(DISPLAYED_ATTRIBUTES)
    for attribute in DISPLAYED_ATTRIBUTES:
        assert attribute in get_attributes_new

def test_reset_displayed_attributes(indexes_sample):
    """Tests the reset of displayedAttributes to default values (in dataset)"""
    response = indexes_sample[0].reset_displayed_attributes()
    assert isinstance(response, object)
    assert 'updateId' in response
    indexes_sample[0].wait_for_pending_update(response['updateId'])
    get_attributes = indexes_sample[0].get_displayed_attributes()
    assert get_attributes == ['*']
