
NEW_SETTINGS = {
    'rankingRules': ['typo', 'words'],
    'searchableAttributes': ['title', 'overview']
}

DEFAULT_RANKING_RULES = [
    'typo',
    'words',
    'proximity',
    'attribute',
    'wordsPosition',
    'exactness'
]

def test_get_settings_default(sample_indexes):
    """Tests getting all settings by default"""
    response = sample_indexes[0].get_settings()
    assert isinstance(response, object)
    for rule in DEFAULT_RANKING_RULES:
        assert rule in response['rankingRules']
    assert response['distinctAttribute'] is None
    assert response['searchableAttributes'] == ['*']
    assert response['displayedAttributes'] == ['*']
    assert response['stopWords'] == []
    assert response['synonyms'] == {}

def test_update_settings(sample_indexes):
    """Tests updating some settings"""
    response = sample_indexes[0].update_settings(NEW_SETTINGS)
    assert isinstance(response, object)
    assert 'updateId' in response
    update = sample_indexes[0].wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    response = sample_indexes[0].get_settings()
    for rule in NEW_SETTINGS['rankingRules']:
        assert rule in response['rankingRules']
    assert response['distinctAttribute'] is None
    for attribute in NEW_SETTINGS['searchableAttributes']:
        assert attribute in response['searchableAttributes']
    assert response['displayedAttributes'] == ['*']
    assert response['stopWords'] == []
    assert response['synonyms'] == {}

def test_reset_settings(sample_indexes):
    """Tests resetting default settings"""
    response = sample_indexes[0].reset_settings()
    assert isinstance(response, object)
    assert 'updateId' in response
    update = sample_indexes[0].wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    response = sample_indexes[0].get_settings()
    for rule in DEFAULT_RANKING_RULES:
        assert rule in response['rankingRules']
    assert response['distinctAttribute'] is None
    assert response['displayedAttributes'] == ['*']
    assert response['searchableAttributes'] == ['*']
    assert response['stopWords'] == []
    assert response['synonyms'] == {}
