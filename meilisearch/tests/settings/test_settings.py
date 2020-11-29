
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

def test_get_settings_default(indexes_sample):
    """Tests getting all settings by default"""
    response = indexes_sample[0].get_settings()
    assert isinstance(response, object)
    for rule in DEFAULT_RANKING_RULES:
        assert rule in response['rankingRules']
    assert response['distinctAttribute'] is None
    assert response['searchableAttributes'] == ['*']
    assert response['displayedAttributes'] == ['*']
    assert response['stopWords'] == []
    assert response['synonyms'] == {}

def test_update_settings(indexes_sample):
    """Tests updating some settings"""
    response = indexes_sample[0].update_settings(NEW_SETTINGS)
    assert isinstance(response, object)
    assert 'updateId' in response
    update = indexes_sample[0].wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    response = indexes_sample[0].get_settings()
    for rule in NEW_SETTINGS['rankingRules']:
        assert rule in response['rankingRules']
    assert response['distinctAttribute'] is None
    for attribute in NEW_SETTINGS['searchableAttributes']:
        assert attribute in response['searchableAttributes']
    assert response['displayedAttributes'] == ['*']
    assert response['stopWords'] == []
    assert response['synonyms'] == {}

def test_reset_settings(indexes_sample):
    """Tests resetting default settings"""
    response = indexes_sample[0].reset_settings()
    assert isinstance(response, object)
    assert 'updateId' in response
    update = indexes_sample[0].wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    response = indexes_sample[0].get_settings()
    for rule in DEFAULT_RANKING_RULES:
        assert rule in response['rankingRules']
    assert response['distinctAttribute'] is None
    assert response['displayedAttributes'] == ['*']
    assert response['searchableAttributes'] == ['*']
    assert response['stopWords'] == []
    assert response['synonyms'] == {}
