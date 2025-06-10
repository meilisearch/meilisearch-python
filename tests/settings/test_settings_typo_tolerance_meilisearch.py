from meilisearch.models.index import TypoTolerance


DEFAULT_TYPO_TOLERANCE = {
    "enabled": True,
    "disableOnNumbers": False,
    "minWordSizeForTypos": {
        "oneTypo": 5,
        "twoTypos": 9,
    },
    "disableOnWords": [],
    "disableOnAttributes": [],
}

NEW_TYPO_TOLERANCE = {
    "enabled": True,
    "disableOnNumbers": False,
    "minWordSizeForTypos": {
        "oneTypo": 6,
        "twoTypos": 10,
    },
    "disableOnWords": [],
    "disableOnAttributes": ["title"],
}


def test_get_typo_tolerance_default(empty_index):
    """Tests getting default typo_tolerance."""
    response = empty_index().get_typo_tolerance()

    assert response.model_dump(by_alias=True) == DEFAULT_TYPO_TOLERANCE


def test_update_typo_tolerance(empty_index):
    """Tests updating typo_tolerance."""
    index = empty_index()
    response_update = index.update_typo_tolerance(NEW_TYPO_TOLERANCE)
    update = index.wait_for_task(response_update.task_uid)
    response_get = index.get_typo_tolerance()

    assert update.status == "succeeded"
    for typo_tolerance in NEW_TYPO_TOLERANCE:  # pylint: disable=consider-using-dict-items
        assert typo_tolerance in response_get.model_dump(by_alias=True)
        assert (
            NEW_TYPO_TOLERANCE[typo_tolerance]
            == response_get.model_dump(by_alias=True)[typo_tolerance]
        )


def test_reset_typo_tolerance(empty_index):
    """Tests resetting the typo_tolerance setting to its default value."""
    index = empty_index()

    # Update the settings
    response_update = index.update_typo_tolerance(NEW_TYPO_TOLERANCE)
    update1 = index.wait_for_task(response_update.task_uid)
    # Get the setting after update
    response_get = index.get_typo_tolerance()
    # Reset the setting
    response_reset = index.reset_typo_tolerance()
    update2 = index.wait_for_task(response_reset.task_uid)
    # Get the setting after reset
    response_last = index.get_typo_tolerance()

    assert update1.status == "succeeded"
    for typo_tolerance in NEW_TYPO_TOLERANCE:  # pylint: disable=consider-using-dict-items
        assert (
            NEW_TYPO_TOLERANCE[typo_tolerance]
            == response_get.model_dump(by_alias=True)[typo_tolerance]
        )
    assert update2.status == "succeeded"
    assert response_last.model_dump(by_alias=True) == DEFAULT_TYPO_TOLERANCE


def test_disable_numbers_true(empty_index):
    index = empty_index()

    # Update settings
    response_update = index.update_typo_tolerance({"disableOnNumbers": True})
    update = index.wait_for_task(response_update.task_uid)
    assert update.status == "succeeded"

    # Fetch updated settings
    tolerance: TypoTolerance = index.get_typo_tolerance()
    assert tolerance.disable_on_numbers
