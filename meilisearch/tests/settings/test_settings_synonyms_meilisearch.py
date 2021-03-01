
NEW_SYNONYMS = {
    'hp': ['harry potter']
}

def test_get_synonyms_default(empty_index):
    """Tests getting default synonyms."""
    response = empty_index().get_synonyms()
    assert isinstance(response, dict)
    assert response == {}

def test_update_synonyms(empty_index):
    """Tests updating synonyms."""
    index = empty_index()
    response = index.update_synonyms(NEW_SYNONYMS)
    assert isinstance(response, dict)
    assert 'updateId' in response
    update = index.wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    response = index.get_synonyms()
    assert isinstance(response, dict)
    for synonym in NEW_SYNONYMS:
        assert synonym in response

def test_reset_synonyms(empty_index):
    """Tests resetting the synonyms setting to its default value."""
    index = empty_index()
    # Update the settings first
    response = index.update_synonyms(NEW_SYNONYMS)
    update = index.wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    # Check the settings have been correctly updated
    response = index.get_synonyms()
    assert isinstance(response, dict)
    for synonym in NEW_SYNONYMS:
        assert synonym in response
    # Check the reset of the settings
    response = index.reset_synonyms()
    assert isinstance(response, dict)
    assert 'updateId' in response
    update = index.wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    response = index.get_synonyms()
    assert response == {}
