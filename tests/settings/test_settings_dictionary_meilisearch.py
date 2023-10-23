NEW_DICTIONARY = ["J. R. R. Tolkien", "W. E. B. Du Bois"]


def test_get_dictionary_default(empty_index):
    """Tests getting the default value of user dictionary."""
    dictionary = empty_index().get_dictionary()
    assert dictionary == []


def test_update_dictionary(empty_index):
    """Tests updating the user dictionary."""
    index = empty_index()
    task = index.update_dictionary(NEW_DICTIONARY)
    task = index.wait_for_task(task.task_uid)
    assert task.status == "succeeded"

    dictionary = index.get_dictionary()
    for word in NEW_DICTIONARY:
        assert word in dictionary


def test_reset_dictionary(empty_index):
    """Tests resetting the user dictionary to its default empty list."""
    index = empty_index()
    task = index.update_dictionary(NEW_DICTIONARY)
    task = index.wait_for_task(task.task_uid)
    assert task.status == "succeeded"

    dictionary = index.get_dictionary()
    for word in NEW_DICTIONARY:
        assert word in dictionary

    reset_task = index.reset_dictionary()
    reset_task = index.wait_for_task(reset_task.task_uid)
    assert reset_task.status == "succeeded"

    dictionary = index.get_dictionary()
    assert dictionary == []
