DEFAULT_FACET_SEARCH_SETTINGS_STATUS = True
ENABLED_FACET_SEARCH_SETTINGS_STATUS = True
DISABLED_FACET_SEARCH_SETTINGS_STATUS = False


def test_get_facet_search_settings(empty_index):
    response = empty_index().get_facet_search_settings()

    assert DEFAULT_FACET_SEARCH_SETTINGS_STATUS == response


def test_update_facet_search_settings(empty_index):
    index = empty_index()

    response = index.update_facet_search_settings(DISABLED_FACET_SEARCH_SETTINGS_STATUS)
    index.wait_for_task(response.task_uid)
    response = index.get_facet_search_settings()
    assert DISABLED_FACET_SEARCH_SETTINGS_STATUS == response

    response = index.update_facet_search_settings(ENABLED_FACET_SEARCH_SETTINGS_STATUS)
    index.wait_for_task(response.task_uid)
    response = index.get_facet_search_settings()
    assert ENABLED_FACET_SEARCH_SETTINGS_STATUS == response


def test_reset_facet_search_settings(empty_index):
    index = empty_index()

    response = index.update_facet_search_settings(DISABLED_FACET_SEARCH_SETTINGS_STATUS)
    index.wait_for_task(response.task_uid)
    response = index.get_facet_search_settings()
    assert DISABLED_FACET_SEARCH_SETTINGS_STATUS == response
    assert DEFAULT_FACET_SEARCH_SETTINGS_STATUS != response

    response = index.reset_facet_search_settings()
    index.wait_for_task(response.task_uid)
    response = index.get_facet_search_settings()
    assert DEFAULT_FACET_SEARCH_SETTINGS_STATUS == response
