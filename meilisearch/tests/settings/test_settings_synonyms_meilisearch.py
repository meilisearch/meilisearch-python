
NEW_SYNONYMS = {
    'hp': ['harry potter']
}

def test_get_synonyms_default(empty_index):
    """Tests getting default synonyms"""
    response = empty_index().get_synonyms()
    assert isinstance(response, object)
    assert response == {}

def test_update_synonyms(empty_index):
    """Tests updating synonyms"""
    index = empty_index()
    response = index.update_synonyms(NEW_SYNONYMS)
    assert isinstance(response, object)
    assert 'updateId' in response
    update = index.wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    response = index.get_synonyms()
    assert isinstance(response, object)
    for synonym in NEW_SYNONYMS:
        assert synonym in response

def test_reset_synonyms(empty_index):
    """Tests resetting synonyms"""
    index = empty_index()
    response = index.reset_synonyms()
    assert isinstance(response, object)
    assert 'updateId' in response
    update = index.wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    response = index.get_synonyms()
    assert response == {}
