import pytest

from tests.common import INDEX_UID


@pytest.mark.usefixtures("enable_edit_documents_by_function")
def test_update_document_by_function(client, index_with_documents):
    """Delete the document with id and update document title"""
    index_with_documents()
    response = client.update_documents_by_function(
        INDEX_UID,
        {"function": 'if doc.id == "522681" {doc = () } else {doc.title = `* ${doc.title} *`}'},
    )

    assert isinstance(response, dict)
    assert isinstance(response["taskUid"], int)
    assert response["indexUid"] == INDEX_UID
