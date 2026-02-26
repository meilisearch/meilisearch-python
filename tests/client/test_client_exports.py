import os
import time

import pytest

from tests import common

pytestmark = pytest.mark.skipif(
    not os.getenv("MEILISEARCH_URL_2"),
    reason="Export API tests run only when second server is configured",
)


def test_export_creation(
    client, client2, index_with_documents, enable_vector_search
):  # pylint: disable=unused-argument
    """Tests the creation of a Meilisearch export."""
    index = index_with_documents()
    export_task = client.export(common.BASE_URL_2, api_key=common.MASTER_KEY)
    task_result = client.wait_for_task(export_task.task_uid)
    assert task_result.status == "succeeded"

    index2 = client2.get_index(index.uid)
    assert index2.uid == index.uid
    assert index2.primary_key == index.get_primary_key()
    assert_exported_count(index2, index.get_documents().total)


def test_export_creation_with_index_filter(
    client, client2, index_with_documents, enable_vector_search
):  # pylint: disable=unused-argument
    """Tests the creation of a Meilisearch export with specific index UIDs."""
    index = index_with_documents()

    indexes = {index.uid: {"filter": None}}
    export_task = client.export(common.BASE_URL_2, api_key=common.MASTER_KEY, indexes=indexes)
    task_result = client.wait_for_task(export_task.task_uid)
    assert task_result.status == "succeeded"

    response = client2.get_indexes()
    assert response["total"] == 1
    index2 = client2.get_index(index.uid)
    assert index2.uid == index.uid
    assert index2.primary_key == index.get_primary_key()
    assert_exported_count(index2, index.get_documents().total)


def assert_exported_count(index, expected_count):
    # Wait up to 20 seconds for documents to be imported
    max_attempts = 20
    for attempt in range(max_attempts):
        doc_count = index.get_documents().total
        if doc_count == expected_count:
            return
        if attempt < max_attempts - 1:
            time.sleep(1)

    # Final check with clear failure message
    actual_count = index.get_documents().total
    assert actual_count == expected_count
