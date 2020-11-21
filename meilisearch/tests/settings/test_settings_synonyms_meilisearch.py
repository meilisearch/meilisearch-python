
NEW_SYNONYMS = {
    'hp': ['harry potter']
}

def test_get_synonyms_default(sample_indexes):
    """Tests getting default synonyms"""
    response = sample_indexes[0].get_synonyms()
    assert isinstance(response, object)
    assert response == {}

def test_update_synonyms(sample_indexes):
    """Tests updating synonyms"""
    response = sample_indexes[0].update_synonyms(NEW_SYNONYMS)
    assert isinstance(response, object)
    assert 'updateId' in response
    update = sample_indexes[0].wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    response = sample_indexes[0].get_synonyms()
    assert isinstance(response, object)
    for synonym in NEW_SYNONYMS:
        assert synonym in response

def test_reset_synonyms(sample_indexes):
    """Tests resetting synonyms"""
    response = sample_indexes[0].reset_synonyms()
    assert isinstance(response, object)
    assert 'updateId' in response
    update = sample_indexes[0].wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    response = sample_indexes[0].get_synonyms()
    assert response == {}
