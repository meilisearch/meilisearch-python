# pylint: disable=invalid-name

import pytest
from tests import wait_for_dump_creation
from meilisearch.errors import MeiliSearchApiError

def test_dump_creation(client, index_with_documents):
    """Tests the creation of a Meilisearch dump."""
    index_with_documents("indexUID-dump-creation")
    dump = client.create_dump()
    assert dump['taskUid'] is not None
    client.wait_for_task(dump['taskUid'])
