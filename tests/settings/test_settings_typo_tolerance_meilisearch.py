DEFAULT_TYPO_TOLERANCE =   {
    'enabled': True,
    'minWordSizeForTypos': {
        'oneTypo': 5,
        'twoTypos': 9,
    },
    'disableOnWords': [],
    'disableOnAttributes': [],
}

NEW_TYPO_TOLERANCE =   {
    'enabled': True,
    'minWordSizeForTypos': {
        'oneTypo': 6,
        'twoTypos': 10,
    },
    'disableOnWords': [],
    'disableOnAttributes': ['title'],
}

def test_get_typo_tolerance_default(empty_index):
    """Tests getting default typo_tolerance."""
    response = empty_index().get_typo_tolerance()
    assert isinstance(response, dict)
    assert response == DEFAULT_TYPO_TOLERANCE

def test_update_typo_tolerance(empty_index):
    """Tests updating typo_tolerance."""
    index = empty_index()
    response = index.update_typo_tolerance(NEW_TYPO_TOLERANCE)
    assert isinstance(response, dict)
    assert 'uid' in response
    update = index.wait_for_task(response['uid'])
    assert update['status'] == 'succeeded'
    response = index.get_typo_tolerance()
    assert isinstance(response, dict)
    for typo_tolerance in NEW_TYPO_TOLERANCE:
        assert typo_tolerance in response
        assert NEW_TYPO_TOLERANCE[typo_tolerance] == response[typo_tolerance]

def test_reset_typo_tolerance(empty_index):
    """Tests resetting the typo_tolerance setting to its default value."""
    index = empty_index()
    # Update the settings first
    response = index.update_typo_tolerance(NEW_TYPO_TOLERANCE)
    update = index.wait_for_task(response['uid'])
    assert update['status'] == 'succeeded'
    # Check the settings have been correctly updated
    response = index.get_typo_tolerance()
    assert isinstance(response, dict)
    for typo_tolerance in NEW_TYPO_TOLERANCE:
        assert typo_tolerance in response
        assert NEW_TYPO_TOLERANCE[typo_tolerance] == response[typo_tolerance]
    # Check the reset of the settings
    response = index.reset_typo_tolerance()
    assert isinstance(response, dict)
    assert 'uid' in response
    update = index.wait_for_task(response['uid'])
    assert update['status'] == 'succeeded'
    response = index.get_typo_tolerance()
    assert response == DEFAULT_TYPO_TOLERANCE
