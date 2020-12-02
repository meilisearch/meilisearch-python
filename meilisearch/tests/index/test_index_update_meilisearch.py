# pylint: disable=invalid-name

import pytest

def test_get_all_update_status_default(empty_index):
    """Tests getting the updates list of an empty index."""
    response = empty_index().get_all_update_status()
    assert isinstance(response, list)
    assert response == []

def test_get_all_update_status(empty_index, small_movies):
    """Tests getting the updates list of a populated index."""
    index = empty_index()
    response = index.add_documents(small_movies)
    assert 'updateId' in response
    response = index.add_documents(small_movies)
    assert 'updateId' in response
    response = index.get_all_update_status()
    assert len(response) == 2

def test_get_update(empty_index, small_movies):
    """Tests getting an update of a given operation."""
    index = empty_index()
    response = index.add_documents(small_movies)
    assert 'updateId' in response
    update = index.wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    response = index.get_update_status(response['updateId'])
    assert 'updateId' in response
    assert 'type' in response
    assert 'duration' in response
    assert 'enqueuedAt' in response
    assert 'processedAt' in response

def test_get_update_inexistent(empty_index):
    """Tests getting an update of an inexistent operation."""
    with pytest.raises(Exception):
        empty_index().get_update_status('999')
