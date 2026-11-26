from meilisearch.models.index import WordPosition

DEFAULT_WORD_POSITION = {"enabled": True}
NEW_WORD_POSITION = {"enabled": False}


def test_get_word_position_settings(empty_index):
    response = empty_index().get_word_position_settings()

    assert isinstance(response, WordPosition)
    assert response.model_dump(by_alias=True) == DEFAULT_WORD_POSITION
    assert response.enabled is True


def test_update_word_position_settings(empty_index):
    index = empty_index()
    response = index.update_word_position_settings(NEW_WORD_POSITION)
    index.wait_for_task(response.task_uid)
    response = index.get_word_position_settings()
    assert response.model_dump(by_alias=True) == NEW_WORD_POSITION
    assert response.enabled is False


def test_reset_word_position_settings(empty_index):
    index = empty_index()
    response = index.update_word_position_settings(NEW_WORD_POSITION)
    index.wait_for_task(response.task_uid)
    response = index.get_word_position_settings()
    assert response.model_dump(by_alias=True) == NEW_WORD_POSITION

    response = index.reset_word_position_settings()
    index.wait_for_task(response.task_uid)
    response = index.get_word_position_settings()
    assert response.model_dump(by_alias=True) == DEFAULT_WORD_POSITION
    assert response.enabled is True
