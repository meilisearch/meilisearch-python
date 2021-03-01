# pylint: disable=invalid-name

from datetime import datetime
import pytest
from meilisearch.errors import MeiliSearchTimeoutError

def test_wait_for_pending_update_default(index_with_documents):
    """Tests waiting for an update with default parameters."""
    index = index_with_documents()
    response = index.add_documents([{'id': 1, 'title': 'Le Petit Prince'}])
    assert 'updateId' in response
    update = index.wait_for_pending_update(response['updateId'])
    assert isinstance(update, dict)
    assert 'status' in update
    assert update['status'] != 'enqueued'

def test_wait_for_pending_update_timeout(index_with_documents):
    """Tests timeout risen by waiting for an update."""
    with pytest.raises(MeiliSearchTimeoutError):
        index_with_documents().wait_for_pending_update(2, timeout_in_ms=0)

def test_wait_for_pending_update_interval_custom(index_with_documents, small_movies):
    """Tests call to wait for an update with custom interval."""
    index = index_with_documents()
    response = index.add_documents(small_movies)
    assert 'updateId' in response
    start_time = datetime.now()
    wait_update = index.wait_for_pending_update(
        response['updateId'],
        interval_in_ms=1000,
        timeout_in_ms=6000
    )
    time_delta = datetime.now() - start_time
    assert isinstance(wait_update, dict)
    assert 'status' in wait_update
    assert wait_update['status'] != 'enqueued'
    assert time_delta.seconds >= 1

def test_wait_for_pending_update_interval_zero(index_with_documents, small_movies):
    """Tests call to wait for an update with custom interval."""
    index = index_with_documents()
    response = index.add_documents(small_movies)
    assert 'updateId' in response
    wait_update = index.wait_for_pending_update(
        response['updateId'],
        interval_in_ms=0,
        timeout_in_ms=6000
    )
    assert isinstance(wait_update, dict)
    assert 'status' in wait_update
    assert wait_update['status'] != 'enqueued'
