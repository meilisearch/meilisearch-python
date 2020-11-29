import pytest

def test_get_documents_default(indexes_sample):
    """Tests getting documents on a clean index"""
    response = indexes_sample[0].get_documents()
    assert isinstance(response, list)
    assert response == []

def test_add_documents(indexes_sample, small_movies):
    """Tests adding new documents to a clean index"""
    response = indexes_sample[0].add_documents(small_movies)
    assert isinstance(response, object)
    assert 'updateId' in response
    assert indexes_sample[0].get_primary_key() == 'id'
    update = indexes_sample[0].wait_for_pending_update(response['updateId'])
    assert update['status'] == 'processed'

def test_get_document(index_with_documents):
    """Tests getting one document on a populated index"""
    response = index_with_documents.get_document('500682')
    assert isinstance(response, object)
    assert 'title' in response
    assert response['title'] == 'The Highwaymen'

def test_get_document_inexistent(indexes_sample):
    """Tests getting one INEXISTENT document on a populated index"""
    with pytest.raises(Exception):
        indexes_sample[0].get_document('123')

def test_get_documents_populated(index_with_documents):
    """Tests getting documents on a populated index"""

    response = index_with_documents.get_documents()
    assert isinstance(response, list)
    assert len(response) == 20

def test_get_documents_offset_optional_params(index_with_documents, small_movies):
    """Tests getting documents on a populated index with optional parameters"""
    # Add movies to the index
    index_with_documents.add_documents(small_movies)

    response = index_with_documents.get_documents()
    assert isinstance(response, list)
    assert len(response) == 20
    response_offset_limit = index_with_documents.get_documents({
        'limit': 3,
        'offset': 1,
        'attributesToRetrieve': 'title'
    })
    assert len(response_offset_limit) == 3
    assert response_offset_limit[0]['title'] == response[1]['title']

def test_update_documents(index_with_documents, small_movies):
    """Tests updating a single document and a set of documents """
    response = index_with_documents.get_documents()
    response[0]['title'] = 'Some title'
    update = index_with_documents.update_documents([response[0]])
    assert isinstance(update, object)
    assert 'updateId' in update
    index_with_documents.wait_for_pending_update(update['updateId'])
    response = index_with_documents.get_documents()
    assert response[0]['title'] == 'Some title'
    update = index_with_documents.update_documents(small_movies)
    index_with_documents.wait_for_pending_update(update['updateId'])
    response = index_with_documents.get_documents()
    assert response[0]['title'] != 'Some title'

def test_delete_document(index_with_documents):
    """Tests deleting a single document"""
    response = index_with_documents.delete_document('500682')
    assert isinstance(response, object)
    assert 'updateId' in response
    index_with_documents.wait_for_pending_update(response['updateId'])
    with pytest.raises(Exception):
        index_with_documents.get_document('500682')

def test_delete_documents(index_with_documents):
    """Tests deleting a set of documents """
    to_delete = ['522681', '450465', '329996']
    response = index_with_documents.delete_documents(to_delete)
    assert isinstance(response, object)
    assert 'updateId' in response
    index_with_documents.wait_for_pending_update(response['updateId'])
    for document in to_delete:
        with pytest.raises(Exception):
            index_with_documents.get_document(document)

def test_delete_all_documents(index_with_documents):
    """Tests updating all the documents in the index"""
    response = index_with_documents.delete_all_documents()
    assert isinstance(response, object)
    assert 'updateId' in response
    index_with_documents.wait_for_pending_update(response['updateId'])
    response = index_with_documents.get_documents()
    assert isinstance(response, list)
    assert response == []
