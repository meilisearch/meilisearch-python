import pytest

from meilisearch.errors import MeilisearchApiError
from tests.common import INDEX_UID
from tests.conftest import index_with_documents

def test_basic_multi_search(client, index_with_documents):
    """Delete the document with id."""
    index_with_documents()
    response = client.update_documents_by_function(
        "indexA", {"function": "if doc.id == \"522681\" {doc = () } else {doc.title = `* ${doc.title} *`}"}
    )

    assert isinstance(response, dict)
    assert response['indexUid'] == INDEX_UID
