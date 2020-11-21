import pytest

def test_get_all_update_status_default(sample_indexes):
    """Tests getting the updates list of an empty index"""
    response = sample_indexes[0].get_all_update_status()
    assert isinstance(response, list)
    assert response == []

def test_get_all_update_status(sample_indexes, small_movies):
    """Tests getting the updates list of a populated index"""
    response = sample_indexes[0].add_documents(small_movies)
    assert 'updateId' in response
    response = sample_indexes[0].add_documents(small_movies)
    assert 'updateId' in response
    response = sample_indexes[0].get_all_update_status()
    assert len(response) == 2

def test_get_update(sample_indexes, small_movies):
    """Tests getting an update of a given operation"""
    response = sample_indexes[0].add_documents(small_movies)
    assert 'updateId' in response
    update = sample_indexes[0].wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'
    response = sample_indexes[0].get_update_status(response['updateId'])
    assert 'updateId' in response
    assert 'type' in response
    assert 'duration' in response
    assert 'enqueuedAt' in response
    assert 'processedAt' in response

def test_get_update_inexistent(sample_indexes):
    """Tests getting an update of an INEXISTENT operation"""
    with pytest.raises(Exception):
        sample_indexes[0].get_update_status('999')
