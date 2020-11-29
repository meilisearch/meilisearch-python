# pylint: disable=invalid-name

import pytest

def test_get_all_update_status_default(indexes_sample):
    """Tests getting the updates list of an empty index"""
    response = indexes_sample[0].get_all_update_status()
    assert isinstance(response, list)
    assert response == []

def test_get_all_update_status(indexes_sample, small_movies):
    """Tests getting the updates list of a populated index"""
    response = indexes_sample[0].add_documents(small_movies)
    assert 'updateId' in response
    response = indexes_sample[0].add_documents(small_movies)
    assert 'updateId' in response
    response = indexes_sample[0].get_all_update_status()
    assert len(response) == 2

def test_get_update(indexes_sample, small_movies):
    """Tests getting an update of a given operation"""
    response = indexes_sample[0].add_documents(small_movies)
    assert 'updateId' in response
    update = indexes_sample[0].wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    response = indexes_sample[0].get_update_status(response['updateId'])
    assert 'updateId' in response
    assert 'type' in response
    assert 'duration' in response
    assert 'enqueuedAt' in response
    assert 'processedAt' in response

def test_get_update_inexistent(indexes_sample):
    """Tests getting an update of an INEXISTENT operation"""
    with pytest.raises(Exception):
        indexes_sample[0].get_update_status('999')
