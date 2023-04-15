DEFAULT_MAX_TOTAL_HITS = 1000
NEW_MAX_TOTAL_HITS = {"maxTotalHits": 2222}


def test_get_pagination_settings(empty_index):
    response = empty_index().get_pagination_settings()

    assert DEFAULT_MAX_TOTAL_HITS == response.max_total_hits


def test_update_pagination_settings(empty_index):
    index = empty_index()
    response = index.update_pagination_settings(NEW_MAX_TOTAL_HITS)
    index.wait_for_task(response.task_uid)
    response = index.get_pagination_settings()
    assert NEW_MAX_TOTAL_HITS["maxTotalHits"] == response.max_total_hits


def test_delete_pagination_settings(empty_index):
    index = empty_index()
    response = index.reset_pagination_settings()

    index.wait_for_task(response.task_uid)
    response = index.get_pagination_settings()
    assert DEFAULT_MAX_TOTAL_HITS == response.max_total_hits
