TYPO_TOLERANCE =   {
    'enabled': 'true',
    'minWordLengthForTypo': {
        'oneTypo': 5,
        'twoTypos': 9,
    },
    'disableOnWords': [],
    'disableOnAttributes': [],
}

def test_get_typo_tolerance_default(empty_index):
    """Tests getting default typo_tolerance."""
    response = empty_index().get_typo_tolerance()
    assert isinstance(response, dict)
    assert response == {}

def test_update_typo_tolerance(empty_index):
    """Tests updating typo_tolerance."""
    index = empty_index()
    response = index.update_typo_tolerance(TYPO_TOLERANCE)
    assert isinstance(response, dict)
    assert 'uid' in response
    update = index.wait_for_task(response['uid'])
    assert update['status'] == 'succeeded'
    response = index.get_typo_tolerance()
    assert isinstance(response, dict)
    for typo_tolerance in TYPO_TOLERANCE:
        assert typo_tolerance in response

def test_reset_typo_tolerance(empty_index):
    """Tests resetting the typo_tolerance setting to its default value."""
    index = empty_index()
    # Update the settings first
    response = index.update_typo_tolerance(TYPO_TOLERANCE)
    update = index.wait_for_task(response['uid'])
    assert update['status'] == 'succeeded'
    # Check the settings have been correctly updated
    response = index.get_typo_tolerance()
    assert isinstance(response, dict)
    for typo_tolerance in TYPO_TOLERANCE:
        assert typo_tolerance in response
    # Check the reset of the settings
    response = index.reset_typo_tolerance()
    assert isinstance(response, dict)
    assert 'uid' in response
    update = index.wait_for_task(response['uid'])
    assert update['status'] == 'succeeded'
    response = index.get_typo_tolerance()
    assert response == {}
