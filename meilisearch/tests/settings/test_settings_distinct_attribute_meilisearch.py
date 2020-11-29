

NEW_DISTINCT_ATTRIBUTE = 'title'
DEFAULT_DISTINCT_ATTRIBUTE = None

def test_get_distinct_attribute(indexes_sample):
    """Tests geting the distinct attributes"""
    response = indexes_sample[0].get_distinct_attribute()
    assert isinstance(response, object)
    assert response == DEFAULT_DISTINCT_ATTRIBUTE

def test_update_distinct_attribute(indexes_sample):
    """Tests creating a custom distinct attribute and checks it has been set correctly"""
    response = indexes_sample[0].update_distinct_attribute(NEW_DISTINCT_ATTRIBUTE)
    assert isinstance(response, object)
    assert 'updateId' in response
    indexes_sample[0].wait_for_pending_update(response['updateId'])
    response = indexes_sample[0].get_distinct_attribute()
    assert isinstance(response, object)
    assert response == NEW_DISTINCT_ATTRIBUTE

def test_reset_distinct_attribute(indexes_sample):
    """Tests resetting distinct attribute"""
    response = indexes_sample[0].reset_distinct_attribute()
    assert isinstance(response, object)
    assert 'updateId' in response
    indexes_sample[0].wait_for_pending_update(response['updateId'])
    response = indexes_sample[0].get_distinct_attribute()
    assert response == DEFAULT_DISTINCT_ATTRIBUTE
