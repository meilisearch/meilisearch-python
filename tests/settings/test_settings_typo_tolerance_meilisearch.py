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
    response_update = index.update_typo_tolerance(NEW_TYPO_TOLERANCE)
    update = index.wait_for_task(response_update['taskUid'])
    response_get = index.get_typo_tolerance()

    assert isinstance(response_update, dict)
    assert 'taskUid' in response_update
    assert update['status'] == 'succeeded'
    assert isinstance(response_get, dict)
    for typo_tolerance in NEW_TYPO_TOLERANCE:
        assert typo_tolerance in response_get
        assert NEW_TYPO_TOLERANCE[typo_tolerance] == response_get[typo_tolerance]

def test_reset_typo_tolerance(empty_index):
    """Tests resetting the typo_tolerance setting to its default value."""
    index = empty_index()

    # Update the settings
    response_update = index.update_typo_tolerance(NEW_TYPO_TOLERANCE)
    update1 = index.wait_for_task(response_update['taskUid'])
    # Get the setting after update
    response_get = index.get_typo_tolerance()
    # Reset the setting
    response_reset = index.reset_typo_tolerance()
    update2 = index.wait_for_task(response_reset['taskUid'])
    # Get the setting after reset
    response_last = index.get_typo_tolerance()

    assert update1['status'] == 'succeeded'
    assert isinstance(response_get, dict)
    for typo_tolerance in NEW_TYPO_TOLERANCE:
        assert typo_tolerance in response_get
        assert NEW_TYPO_TOLERANCE[typo_tolerance] == response_get[typo_tolerance]
    assert isinstance(response_reset, dict)
    assert 'taskUid' in response_reset
    assert update2['status'] == 'succeeded'
    assert response_last == DEFAULT_TYPO_TOLERANCE
