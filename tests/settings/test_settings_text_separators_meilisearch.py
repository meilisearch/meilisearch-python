NEW_SEPARATOR_TOKENS = ["|", "&hellip;"]
NEW_NON_SEPARATOR_TOKENS = ["@", "#"]


def test_get_separator_tokens_default(empty_index):
    """Tests getting the default value of separator tokens."""
    separator_tokens = empty_index().get_separator_tokens()
    assert separator_tokens == []


def test_get_non_separator_tokens_default(empty_index):
    """Tests getting the default value of separator tokens."""
    non_separator_tokens = empty_index().get_separator_tokens()
    assert non_separator_tokens == []


def test_update_separator_tokens(empty_index):
    """Tests updating the separator tokens."""
    index = empty_index()
    task = index.update_separator_tokens(NEW_SEPARATOR_TOKENS)
    task = index.wait_for_task(task.task_uid)
    assert task.status == "succeeded"

    separator_tokens = index.get_separator_tokens()
    for token in NEW_SEPARATOR_TOKENS:
        assert token in separator_tokens


def test_update_non_separator_tokens(empty_index):
    """Tests updating the non separator tokens."""
    index = empty_index()
    task = index.update_non_separator_tokens(NEW_NON_SEPARATOR_TOKENS)
    task = index.wait_for_task(task.task_uid)
    assert task.status == "succeeded"

    non_separator_tokens = index.get_non_separator_tokens()
    for token in NEW_NON_SEPARATOR_TOKENS:
        assert token in non_separator_tokens


def test_reset_separator_tokens(empty_index):
    """Tests resetting the separator tokens to its default empty list."""
    index = empty_index()
    task = index.update_separator_tokens(NEW_SEPARATOR_TOKENS)
    task = index.wait_for_task(task.task_uid)
    assert task.status == "succeeded"

    separator_tokens = index.get_separator_tokens()
    for token in NEW_SEPARATOR_TOKENS:
        assert token in separator_tokens

    reset_task = index.reset_separator_tokens()
    reset_task = index.wait_for_task(reset_task.task_uid)
    assert reset_task.status == "succeeded"

    separator_tokens = index.get_separator_tokens()
    assert separator_tokens == []


def test_non_reset_separator_tokens(empty_index):
    """Tests resetting the separator tokens to its default empty list."""
    index = empty_index()
    task = index.update_non_separator_tokens(NEW_NON_SEPARATOR_TOKENS)
    task = index.wait_for_task(task.task_uid)
    assert task.status == "succeeded"

    non_separator_tokens = index.get_non_separator_tokens()
    for token in NEW_NON_SEPARATOR_TOKENS:
        assert token in non_separator_tokens

    reset_task = index.reset_non_separator_tokens()
    reset_task = index.wait_for_task(reset_task.task_uid)
    assert reset_task.status == "succeeded"

    non_separator_tokens = index.get_non_separator_tokens()
    assert non_separator_tokens == []
