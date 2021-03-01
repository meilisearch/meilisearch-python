# pylint: disable=invalid-name

import pytest

def test_get_documents_default(empty_index):
    """Tests getting documents on a clean index."""
    response = empty_index().get_documents()
    assert isinstance(response, list)
    assert response == []

def test_add_documents(empty_index, small_movies):
    """Tests adding new documents to a clean index."""
    index = empty_index()
    response = index.add_documents(small_movies)
    assert isinstance(response, dict)
    assert 'updateId' in response
    update = index.wait_for_pending_update(response['updateId'])
    assert index.get_primary_key() == 'id'
    assert update['status'] == 'processed'

def test_get_document(index_with_documents):
    """Tests getting one document from a populated index."""
    response = index_with_documents().get_document('500682')
    assert isinstance(response, dict)
    assert 'title' in response
    assert response['title'] == 'The Highwaymen'

def test_get_document_inexistent(empty_index):
    """Tests getting one inexistent document from a populated index."""
    with pytest.raises(Exception):
        empty_index().get_document('123')

def test_get_documents_populated(index_with_documents):
    """Tests getting documents from a populated index."""
    response = index_with_documents().get_documents()
    assert isinstance(response, list)
    assert len(response) == 20

def test_get_documents_offset_optional_params(index_with_documents):
    """Tests getting documents from a populated index with optional parameters."""
    index = index_with_documents()
    response = index.get_documents()
    assert isinstance(response, list)
    assert len(response) == 20
    response_offset_limit = index.get_documents({
        'limit': 3,
        'offset': 1,
        'attributesToRetrieve': 'title'
    })
    assert len(response_offset_limit) == 3
    assert response_offset_limit[0]['title'] == response[1]['title']

def test_update_documents(index_with_documents, small_movies):
    """Tests updating a single document and a set of documents."""
    index = index_with_documents()
    response = index.get_documents()
    response[0]['title'] = 'Some title'
    update = index.update_documents([response[0]])
    assert isinstance(update, dict)
    assert 'updateId' in update
    index.wait_for_pending_update(update['updateId'])
    response = index.get_documents()
    assert response[0]['title'] == 'Some title'
    update = index.update_documents(small_movies)
    index.wait_for_pending_update(update['updateId'])
    response = index.get_documents()
    assert response[0]['title'] != 'Some title'

def test_delete_document(index_with_documents):
    """Tests deleting a single document."""
    index = index_with_documents()
    response = index.delete_document('500682')
    assert isinstance(response, dict)
    assert 'updateId' in response
    index.wait_for_pending_update(response['updateId'])
    with pytest.raises(Exception):
        index.get_document('500682')

def test_delete_documents(index_with_documents):
    """Tests deleting a set of documents."""
    to_delete = ['522681', '450465', '329996']
    index = index_with_documents()
    response = index.delete_documents(to_delete)
    assert isinstance(response, dict)
    assert 'updateId' in response
    index.wait_for_pending_update(response['updateId'])
    for document in to_delete:
        with pytest.raises(Exception):
            index.get_document(document)

def test_delete_all_documents(index_with_documents):
    """Tests deleting all the documents in the index."""
    index = index_with_documents()
    response = index.delete_all_documents()
    assert isinstance(response, dict)
    assert 'updateId' in response
    index.wait_for_pending_update(response['updateId'])
    response = index.get_documents()
    assert isinstance(response, list)
    assert response == []
