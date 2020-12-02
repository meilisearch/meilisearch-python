# pylint: disable=invalid-name

import pytest
from meilisearch.tests import wait_for_dump_creation
from meilisearch.errors import MeiliSearchApiError

def test_dump_creation(client, index_with_documents):
    """Tests the creation of a MeiliSearch dump."""
    index_with_documents("indexUID-dump-creation")
    dump = client.create_dump()
    assert dump['uid'] is not None
    assert dump['status'] == 'in_progress'
    wait_for_dump_creation(client, dump['uid'])

def test_dump_status_route(client, index_with_documents):
    """Tests the route for getting a MeiliSearch dump status."""
    index_with_documents("indexUID-dump-status")
    dump = client.create_dump()
    assert dump['uid'] is not None
    assert dump['status'] == 'in_progress'
    dump_status = client.get_dump_status(dump['uid'])
    assert dump_status['uid'] is not None
    assert dump_status['status'] is not None
    wait_for_dump_creation(client, dump['uid'])

def test_dump_status_nonexistent_uid_raises_error(client):
    """Tests the route for getting an inexistent dump status."""
    with pytest.raises(MeiliSearchApiError):
        client.get_dump_status('uid_not_exists')
