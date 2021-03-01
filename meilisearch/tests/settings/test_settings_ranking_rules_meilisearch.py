
NEW_RANKING_RULES = ['typo', 'exactness']
DEFAULT_RANKING_RULES = [
    'typo',
    'words',
    'proximity',
    'attribute',
    'wordsPosition',
    'exactness'
]

def test_get_ranking_rules_default(empty_index):
    """Tests getting the default ranking rules."""
    response = empty_index().get_ranking_rules()
    assert isinstance(response, list)
    for rule in DEFAULT_RANKING_RULES:
        assert rule in response

def test_update_ranking_rules(empty_index):
    """Tests changing the ranking rules."""
    index = empty_index()
    response = index.update_ranking_rules(NEW_RANKING_RULES)
    assert isinstance(response, dict)
    assert 'updateId' in response
    index.wait_for_pending_update(response['updateId'])
    response = index.get_ranking_rules()
    assert isinstance(response, list)
    for rule in NEW_RANKING_RULES:
        assert rule in response

def test_reset_ranking_rules(empty_index):
    """Tests resetting the ranking rules setting to its default value."""
    index = empty_index()
    # Update the settings first
    response = index.update_ranking_rules(NEW_RANKING_RULES)
    update = index.wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    # Check the settings have been correctly updated
    response = index.get_ranking_rules()
    assert isinstance(response, list)
    for rule in NEW_RANKING_RULES:
        assert rule in response
    # Check the reset of the settings
    response = index.reset_ranking_rules()
    assert isinstance(response, dict)
    assert 'updateId' in response
    index.wait_for_pending_update(response['updateId'])
    response = index.get_ranking_rules()
    for rule in DEFAULT_RANKING_RULES:
        assert rule in response
