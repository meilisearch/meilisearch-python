
NEW_SYNONYMS = {
    'hp': ['harry potter']
}

def test_get_synonyms_default(indexes_sample):
    """Tests getting default synonyms"""
    response = indexes_sample[0].get_synonyms()
    assert isinstance(response, object)
    assert response == {}

def test_update_synonyms(indexes_sample):
    """Tests updating synonyms"""
    response = indexes_sample[0].update_synonyms(NEW_SYNONYMS)
    assert isinstance(response, object)
    assert 'updateId' in response
    update = indexes_sample[0].wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    response = indexes_sample[0].get_synonyms()
    assert isinstance(response, object)
    for synonym in NEW_SYNONYMS:
        assert synonym in response

def test_reset_synonyms(indexes_sample):
    """Tests resetting synonyms"""
    response = indexes_sample[0].reset_synonyms()
    assert isinstance(response, object)
    assert 'updateId' in response
    update = indexes_sample[0].wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    response = indexes_sample[0].get_synonyms()
    assert response == {}
