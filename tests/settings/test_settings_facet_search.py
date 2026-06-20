DEFAULT_FACET_SEARCH_SETTINGS_STATUS = True
ENABLED_FACET_SEARCH_SETTINGS_STATUS = True
DISABLED_FACET_SEARCH_SETTINGS_STATUS = False
TEST_TASK_TIMEOUT_MS = 30_000


def test_get_facet_search_settings(empty_index):
    response = empty_index().get_facet_search_settings()

    assert DEFAULT_FACET_SEARCH_SETTINGS_STATUS == response


def test_update_facet_search_settings(empty_index):
    index = empty_index()

    response = index.update_facet_search_settings(DISABLED_FACET_SEARCH_SETTINGS_STATUS)
    index.wait_for_task(response.task_uid, timeout_in_ms=TEST_TASK_TIMEOUT_MS)
    response = index.get_facet_search_settings()
    assert DISABLED_FACET_SEARCH_SETTINGS_STATUS == response

    response = index.update_facet_search_settings(ENABLED_FACET_SEARCH_SETTINGS_STATUS)
    index.wait_for_task(response.task_uid, timeout_in_ms=TEST_TASK_TIMEOUT_MS)
    response = index.get_facet_search_settings()
    assert ENABLED_FACET_SEARCH_SETTINGS_STATUS == response


def test_reset_facet_search_settings(empty_index):
    index = empty_index()

    response = index.update_facet_search_settings(DISABLED_FACET_SEARCH_SETTINGS_STATUS)
    index.wait_for_task(response.task_uid, timeout_in_ms=TEST_TASK_TIMEOUT_MS)
    response = index.get_facet_search_settings()
    assert DISABLED_FACET_SEARCH_SETTINGS_STATUS == response
    assert DEFAULT_FACET_SEARCH_SETTINGS_STATUS != response

    response = index.reset_facet_search_settings()
    index.wait_for_task(response.task_uid, timeout_in_ms=TEST_TASK_TIMEOUT_MS)
    response = index.get_facet_search_settings()
    assert DEFAULT_FACET_SEARCH_SETTINGS_STATUS == response
