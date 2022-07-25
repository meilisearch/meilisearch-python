DEFAULT_MAX_TOTAL_HITS = 1000
NEW_MAX_TOTAL_HITS = {'maxTotalHits': 2222}


def test_get_pagination_settings(empty_index):
    response = empty_index().get_pagination_settings()

    assert isinstance(response, dict)
    assert { 'maxTotalHits': DEFAULT_MAX_TOTAL_HITS } == response


def test_update_pagination_settings(empty_index):
    index = empty_index()
    response = index.update_pagination_settings(NEW_MAX_TOTAL_HITS)
    assert isinstance(response, dict)
    assert 'taskUid' in response

    index.wait_for_task(response['taskUid'])
    response = index.get_pagination_settings()
    assert isinstance(response, dict)
    assert NEW_MAX_TOTAL_HITS == response


def test_delete_pagination_settings(empty_index):
    index = empty_index()
    response = index.reset_pagination_settings()

    index.wait_for_task(response['taskUid'])
    response = index.get_pagination_settings()
    assert isinstance(response, dict)
    assert { 'maxTotalHits': DEFAULT_MAX_TOTAL_HITS } == response
