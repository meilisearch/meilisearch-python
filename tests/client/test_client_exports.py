import os

import pytest

from tests import common

pytestmark = pytest.mark.skipif(
    not os.getenv("MEILISEARCH_URL_2"),
    reason="Export API tests run only when second server is configured",
)


def test_export_creation(client, client2, index_with_documents):
    """Tests the creation of a Meilisearch export."""
    index = index_with_documents()
    export_task = client.export(common.BASE_URL_2, api_key=common.MASTER_KEY)
    task_result = client.wait_for_task(export_task.task_uid)
    assert task_result.status == "succeeded"

    index2 = client2.get_index(index.uid)
    assert index2.uid == index.uid
    assert index2.primary_key == index.get_primary_key()
    assert index2.get_documents().total == index.get_documents().total


def test_export_creation_with_index_filter(client, client2, index_with_documents):
    """Tests the creation of a Meilisearch export with specific index UIDs."""
    index_with_documents()
    index = index_with_documents(common.INDEX_UID2)

    indexes = {common.INDEX_UID2: {"filter": None}}
    export_task = client.export(common.BASE_URL_2, api_key=common.MASTER_KEY, indexes=indexes)
    task_result = client.wait_for_task(export_task.task_uid)
    assert task_result.status == "succeeded"

    response = client2.get_indexes()
    assert response["total"] == 1
    index2 = client2.get_index(common.INDEX_UID2)

    assert index2.uid == index.uid
    assert index2.primary_key == index.get_primary_key()
    assert index.get_documents().total == index2.get_documents().total
